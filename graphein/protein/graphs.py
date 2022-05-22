"""Functions for working with Protein Structure Graphs."""
# %%
# Graphein
# Author: Arian Jamasb <arian@jamasb.io>, Eric Ma, Charlie Harris
# License: MIT
# Project Website: https://github.com/a-r-j/graphein
# Code Repository: https://github.com/a-r-j/graphein
from __future__ import annotations

import logging
import traceback
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import networkx as nx
import numpy as np
import pandas as pd
from Bio.PDB.Polypeptide import three_to_one
from biopandas.pdb import PandasPdb
from tqdm.contrib.concurrent import process_map

from graphein.protein.config import (
    DSSPConfig,
    GetContactsConfig,
    ProteinGraphConfig,
)
from graphein.protein.edges.distance import compute_distmat
from graphein.protein.resi_atoms import BACKBONE_ATOMS, RESI_THREE_TO_1
from graphein.protein.subgraphs import extract_subgraph_from_chains
from graphein.protein.utils import (
    ProteinGraphConfigurationError,
    compute_rgroup_dataframe,
    filter_dataframe,
    get_protein_name_from_filename,
    three_to_one_with_mods,
)
from graphein.utils.utils import (
    annotate_edge_metadata,
    annotate_graph_metadata,
    annotate_node_metadata,
    compute_edges,
)

logging.basicConfig(level="DEBUG")
log = logging.getLogger(__name__)


def read_pdb_to_dataframe(
    pdb_path: Optional[str] = None,
    pdb_code: Optional[str] = None,
    verbose: bool = False,
    granularity: str = "CA",
) -> pd.DataFrame:
    """
    Reads PDB file to ``PandasPDB`` object.

    Returns ``atomic_df``, which is a dataframe enumerating all atoms and their cartesian coordinates in 3D space. Also
    contains associated metadata from the PDB file.

    :param pdb_path: path to PDB file. Defaults to None.
    :type pdb_path: str, optional
    :param pdb_code: 4-character PDB accession. Defaults to None.
    :type pdb_code: str, optional
    :param verbose: print dataframe?
    :type verbose: bool
    :param granularity: Specifies granularity of dataframe. See :class:`~graphein.protein.config.ProteinGraphConfig` for further
        details.
    :type granularity: str
    :returns: ``pd.DataFrame`` containing protein structure
    :rtype: pd.DataFrame
    """

    assert (pdb_code and not pdb_path) or (not pdb_code and pdb_path), (
        "Either a PDB ID or a path to a local PDB file"
        " must be specified to read a PDB"
    )

    atomic_df = (
        PandasPdb().read_pdb(pdb_path)
        if pdb_path is not None
        else PandasPdb().fetch_pdb(pdb_code)
    )

    # Assign Node IDs to dataframes
    atomic_df.df["ATOM"]["node_id"] = (
        atomic_df.df["ATOM"]["chain_id"].apply(str)
        + ":"
        + atomic_df.df["ATOM"]["residue_name"]
        + ":"
        + atomic_df.df["ATOM"]["residue_number"].apply(str)
    )
    if granularity == "atom":
        atomic_df.df["ATOM"]["node_id"] = (
            atomic_df.df["ATOM"]["node_id"]
            + ":"
            + atomic_df.df["ATOM"]["atom_name"]
        )
    if verbose:
        print(atomic_df)
    return atomic_df


def deprotonate_structure(df: pd.DataFrame) -> pd.DataFrame:
    """Remove protons from PDB dataframe.

    :param df: Atomic dataframe.
    :type df: pd.DataFrame
    :returns: Atomic dataframe with all ``atom_name == "H"`` removed.
    :rtype: pd.DataFrame
    """
    log.debug(
        "Deprotonating protein. This removes H atoms from the pdb_df dataframe"
    )
    return filter_dataframe(
        df, by_column="atom_name", list_of_values=["H"], boolean=False
    )


def convert_structure_to_centroids(df: pd.DataFrame) -> pd.DataFrame:
    """Overwrite existing ``(x, y, z)`` coordinates with centroids of the amino acids.

    :param df: Pandas Dataframe protein structure to convert into a dataframe of centroid positions.
    :type df: pd.DataFrame
    :return: pd.DataFrame with atoms/residues positions converted into centroid positions.
    :rtype: pd.DataFrame
    """
    log.debug(
        "Converting dataframe to centroids. This averages XYZ coords of the atoms in a residue"
    )

    centroids = calculate_centroid_positions(df)
    df = df.loc[df["atom_name"] == "CA"].reset_index(drop=True)
    df["x_coord"] = centroids["x_coord"]
    df["y_coord"] = centroids["y_coord"]
    df["z_coord"] = centroids["z_coord"]

    return df


def subset_structure_to_atom_type(
    df: pd.DataFrame, granularity: str
) -> pd.DataFrame:
    """
    Return a subset of atomic dataframe that contains only certain atom names.

    :param df: Protein Structure dataframe to subset.
    :type df: pd.DataFrame
    :returns: Subsetted protein structure dataframe.
    :rtype: pd.DataFrame
    """
    return filter_dataframe(
        df, by_column="atom_name", list_of_values=[granularity], boolean=True
    )


def remove_insertions(df: pd.DataFrame, keep: str = "first") -> pd.DataFrame:
    """
    This function removes insertions from PDB dataframes.

    :param df: Protein Structure dataframe to remove insertions from.
    :type df: pd.DataFrame
    :param keep: Specifies which insertion to keep. Options are ``"first"`` or ``"last"``.
        Default is ``"first"``
    :type keep: str
    :return: Protein structure dataframe with insertions removed
    :rtype: pd.DataFrame
    """
    # Catches unnamed insertions
    duplicates = df.duplicated(
        subset=["chain_id", "residue_number", "atom_name"], keep=keep
    )
    df = df[~duplicates]

    # Catches explicit insertions
    df = filter_dataframe(
        df, by_column="insertion", list_of_values=[""], boolean=True
    )

    # Remove alt_locs
    df = filter_dataframe(
        df, by_column="alt_loc", list_of_values=["", "A"], boolean=True
    )

    return df


def filter_hetatms(
    df: pd.DataFrame, keep_hets: List[str]
) -> List[pd.DataFrame]:
    """Return hetatms of interest.

    :param df: Protein Structure dataframe to filter hetatoms from.
    :type df: pd.DataFrame
    :param keep_hets: List of hetero atom names to keep.
    :returns: Protein structure dataframe with heteroatoms removed
    :rtype pd.DataFrame
    """
    return [df.loc[df["residue_name"] == hetatm] for hetatm in keep_hets]


def process_dataframe(
    protein_df: pd.DataFrame,
    atom_df_processing_funcs: Optional[List[Callable]] = None,
    hetatom_df_processing_funcs: Optional[List[Callable]] = None,
    granularity: str = "centroids",
    chain_selection: str = "all",
    insertions: bool = False,
    deprotonate: bool = True,
    keep_hets: List[str] = [],
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Process ATOM and HETATM dataframes to produce singular dataframe used for graph construction.

    :param protein_df: Dataframe to process.
        Should be the object returned from :func:`~graphein.protein.graphs.read_pdb_to_dataframe`.
    :type protein_df: pd.DataFrame
    :param atom_df_processing_funcs: List of functions to process dataframe. These must take in a dataframe and return a
        dataframe. Defaults to None.
    :type atom_df_processing_funcs: List[Callable], optional
    :param hetatom_df_processing_funcs: List of functions to process the hetatom dataframe. These must take in a dataframe and return a dataframe
    :type hetatom_df_processing_funcs: List[Callable], optional
    :param granularity: The level of granularity for the graph. This determines the node definition.
        Acceptable values include: ``"centroids"``, ``"atoms"``,
        any of the atom_names in the PDB file (e.g. ``"CA"``, ``"CB"``, ``"OG"``, etc.).
        See: :const:`~graphein.protein.config.GRAPH_ATOMS` and :const:`~graphein.protein.config.GRANULARITY_OPTS`.
    :type granularity: str
    :param insertions: Whether or not to keep insertions.
    :param insertions: bool
    :param deprotonate: Whether or not to remove hydrogen atoms (i.e. deprotonation).
    :type deprotonate: bool
    :param keep_hets: Hetatoms to keep. Defaults to an empty list.
        To keep a hetatom, pass it inside a list of hetatom names to keep.
    :type keep_hets: List[str]
    :param verbose: Verbosity level.
    :type verbose: bool
    :param chain_selection: Which protein chain to select. Defaults to ``"all"``. Eg can use ``"ACF"``
        to select 3 chains (``A``, ``C`` & ``F``)
    :type chain_selection: str
    :return: A protein dataframe that can be consumed by
        other graph construction functions.
    :rtype: pd.DataFrame
    """
    # TODO: Need to properly define what "granularity" is supposed to do.
    atoms = protein_df.df["ATOM"]
    hetatms = protein_df.df["HETATM"]

    # This block enables processing via a list of supplied functions operating on the atom and hetatom dataframes
    # If these are provided, the dataframe returned will be computed only from these and the default workflow
    # below this block will not execute.
    if atom_df_processing_funcs is not None:
        for func in atom_df_processing_funcs:
            atoms = func(atoms)
        if hetatom_df_processing_funcs is None:
            return atoms

    if hetatom_df_processing_funcs is not None:
        for func in hetatom_df_processing_funcs:
            hetatms = func(hetatms)
        return pd.concat([atoms, hetatms])

    # Deprotonate structure by removing H atoms
    if deprotonate:
        atoms = deprotonate_structure(atoms)

    # Restrict DF to desired granularity
    if granularity == "atom":
        pass
    elif granularity == "centroids":
        atoms = convert_structure_to_centroids(atoms)
    else:
        atoms = subset_structure_to_atom_type(atoms, granularity)

    protein_df = atoms

    if keep_hets:
        hetatms_to_keep = filter_hetatms(atoms, keep_hets)
        protein_df = pd.concat([atoms, hetatms_to_keep])

    # Remove alt_loc residues
    if not insertions:
        protein_df = remove_insertions(protein_df)

    # perform chain selection
    protein_df = select_chains(
        protein_df, chain_selection=chain_selection, verbose=verbose
    )

    log.debug(f"Detected {len(protein_df)} total nodes")

    return protein_df


def assign_node_id_to_dataframe(
    protein_df: pd.DataFrame, granularity: str
) -> pd.DataFrame:
    """
    Assigns the node ID back to the ``pdb_df`` dataframe

    :param protein_df: Structure Dataframe
    :type protein_df: pd.DataFrame
    :param granularity: Granularity of graph. Atom-level,
        residue (e.g. ``CA``) or ``centroids``.
        See: :const:`~graphein.protein.config.GRAPH_ATOMS`
        and :const:`~graphein.protein.config.GRANULARITY_OPTS`.
    :type granularity: str
    :return: Returns dataframe with added ``node_ids``
    :rtype: pd.DataFrame
    """
    protein_df["node_id"] = (
        protein_df["chain_id"].apply(str)
        + ":"
        + protein_df["residue_name"]
        + ":"
        + protein_df["residue_number"].apply(str)
    )
    if granularity == "atom":
        protein_df[
            "node_id"
        ] = f'{protein_df["node_id"]}:{protein_df["atom_name"]}'


def select_chains(
    protein_df: pd.DataFrame, chain_selection: str, verbose: bool = False
) -> pd.DataFrame:
    """
    Extracts relevant chains from ``protein_df``.

    :param protein_df: pandas dataframe of PDB subsetted to relevant atoms
        (``CA``, ``CB``).
    :type protein_df: pd.DataFrame
    :param chain_selection: Specifies chains that should be extracted from
        the larger complexed structure.
    :type chain_selection: str
    :param verbose: Print dataframe?
    :type verbose: bool
    :return: Protein structure dataframe containing only entries in the
        chain selection.
    :rtype: pd.DataFrame
    """
    if chain_selection != "all":
        protein_df = filter_dataframe(
            protein_df,
            by_column="chain_id",
            list_of_values=list(chain_selection),
            boolean=True,
        )

    return protein_df


def initialise_graph_with_metadata(
    protein_df: pd.DataFrame,
    raw_pdb_df: pd.DataFrame,
    granularity: str,
    name: Optional[str] = None,
    pdb_code: Optional[str] = None,
    pdb_path: Optional[str] = None,
) -> nx.Graph:
    """
    Initializes the nx Graph object with initial metadata.

    :param protein_df: Processed Dataframe of protein structure.
    :type protein_df: pd.DataFrame
    :param raw_pdb_df: Unprocessed dataframe of protein structure for comparison and traceability downstream.
    :type raw_pdb_df: pd.DataFrame
    :param granularity: Granularity of the graph (eg ``"atom"``, ``"CA"``, ``"CB"`` etc or ``"centroid"``).
        See: :const:`~graphein.protein.config.GRAPH_ATOMS` and :const:`~graphein.protein.config.GRANULARITY_OPTS`.
    :type granularity: str
    :param name: specified given name for the graph. If None, the PDB code or the file name will be used to name the graph.
    :type name: Optional[str], defaults to ``None``
    :param pdb_code: PDB ID / Accession code, if the PDB is available on the PDB database.
    :type pdb_code: Optional[str], defaults to ``None``
    :param pdb_path: path to local PDB file, if constructing a graph from a local file.
    :type pdb_path: Optional[str], defaults to ``None``
    :return: Returns initial protein structure graph with metadata.
    :rtype: nx.Graph
    """

    assert (pdb_code and not pdb_path) or (not pdb_code and pdb_path), (
        "Either a PDB ID or a path to a local PDB file"
        " must be specified to read a PDB"
    )

    # Get name for graph if no name was provided
    if not name:
        if pdb_path:
            name = get_protein_name_from_filename(pdb_path)
        else:
            name = pdb_code

    G = nx.Graph(
        name=name,
        pdb_code=pdb_code,
        pdb_path=pdb_path,
        chain_ids=list(protein_df["chain_id"].unique()),
        pdb_df=protein_df,
        raw_pdb_df=raw_pdb_df,
        rgroup_df=compute_rgroup_dataframe(remove_insertions(raw_pdb_df)),
        coords=np.asarray(protein_df[["x_coord", "y_coord", "z_coord"]]),
    )

    # Create graph and assign intrinsic graph-level metadata
    G.graph["node_type"] = granularity

    # Add Sequences to graph metadata
    for c in G.graph["chain_ids"]:
        G.graph[f"sequence_{c}"] = (
            protein_df.loc[protein_df["chain_id"] == c]["residue_name"]
            .apply(three_to_one_with_mods)
            .str.cat()
        )
    return G


def add_nodes_to_graph(
    G: nx.Graph,
    protein_df: Optional[pd.DataFrame] = None,
    verbose: bool = False,
) -> nx.Graph:
    """Add nodes into protein graph.

    :param G: ``nx.Graph`` with metadata to populate with nodes.
    :type G: nx.Graph
    :protein_df: DataFrame of protein structure containing nodes & initial node metadata to add to the graph.
    :type protein_df: pd.DataFrame, optional
    :param verbose: Controls verbosity of this step.
    :type verbose: bool
    :returns: nx.Graph with nodes added.
    :rtype: nx.Graph
    """

    # If no protein dataframe is supplied, use the one stored in the Graph object
    if protein_df is None:
        protein_df = G.graph["pdb_df"]
    # Assign intrinsic node attributes
    chain_id = protein_df["chain_id"].apply(str)
    residue_name = protein_df["residue_name"]
    residue_number = protein_df["residue_number"]  # .apply(str)
    coords = np.asarray(protein_df[["x_coord", "y_coord", "z_coord"]])
    b_factor = protein_df["b_factor"]
    atom_type = protein_df["atom_name"]
    nodes = protein_df["node_id"]
    element_symbol = protein_df["element_symbol"]
    G.add_nodes_from(nodes)

    # Set intrinsic node attributes
    nx.set_node_attributes(G, dict(zip(nodes, chain_id)), "chain_id")
    nx.set_node_attributes(G, dict(zip(nodes, residue_name)), "residue_name")
    nx.set_node_attributes(
        G, dict(zip(nodes, residue_number)), "residue_number"
    )
    nx.set_node_attributes(G, dict(zip(nodes, atom_type)), "atom_type")
    nx.set_node_attributes(
        G, dict(zip(nodes, element_symbol)), "element_symbol"
    )
    nx.set_node_attributes(G, dict(zip(nodes, coords)), "coords")
    nx.set_node_attributes(G, dict(zip(nodes, b_factor)), "b_factor")

    # TODO: include charge, line_idx for traceability?
    if verbose:
        print(nx.info(G))
        print(G.nodes())

    return G


def calculate_centroid_positions(
    atoms: pd.DataFrame, verbose: bool = False
) -> pd.DataFrame:
    """
    Calculates position of sidechain centroids.

    :param atoms: ATOM df of protein structure.
    :type atoms: pd.DataFrame
    :param verbose: bool controlling verbosity.
    :type verbose: bool
    :return: centroids (df).
    :rtype: pd.DataFrame
    """
    centroids = (
        atoms.groupby("residue_number")
        .mean()[["x_coord", "y_coord", "z_coord"]]
        .reset_index()
    )
    if verbose:
        print(f"Calculated {len(centroids)} centroid nodes")
    log.debug(f"Calculated {len(centroids)} centroid nodes")
    return centroids


def compute_edges(
    G: nx.Graph,
    funcs: List[Callable],
    get_contacts_config: Optional[GetContactsConfig] = None,
) -> nx.Graph:
    """
    Computes edges for the protein structure graph. Will compute a pairwise
    distance matrix between nodes which is
    added to the graph metadata to facilitate some edge computations.

    :param G: nx.Graph with nodes to add edges to.
    :type G: nx.Graph
    :param funcs: List of edge construction functions.
    :type funcs: List[Callable]
    :param get_contacts_config: Config object for ``GetContacts`` if
        intramolecular edges are being used.
    :type get_contacts_config: graphein.protein.config.GetContactsConfig
    :return: Graph with added edges.
    :rtype: nx.Graph
    """
    # This control flow prevents unnecessary computation of the distance matrices
    if "config" in G.graph:
        if G.graph["config"].granularity == "atom":
            G.graph["atomic_dist_mat"] = compute_distmat(G.graph["raw_pdb_df"])
        else:
            G.graph["dist_mat"] = compute_distmat(G.graph["pdb_df"])

    for func in funcs:
        func(G)

    return G


def construct_graph(
    config: Optional[ProteinGraphConfig] = None,
    name: Optional[str] = None,
    pdb_path: Optional[str] = None,
    pdb_code: Optional[str] = None,
    chain_selection: str = "all",
    df_processing_funcs: Optional[List[Callable]] = None,
    edge_construction_funcs: Optional[List[Callable]] = None,
    edge_annotation_funcs: Optional[List[Callable]] = None,
    node_annotation_funcs: Optional[List[Callable]] = None,
    graph_annotation_funcs: Optional[List[Callable]] = None,
) -> nx.Graph:
    """
    Constructs protein structure graph from a ``pdb_code`` or ``pdb_path``.

    Users can provide a :class:`~graphein.protein.config.ProteinGraphConfig`
    object to specify construction parameters.

    However, config parameters can be overridden by passing arguments directly to the function.

    :param config: :class:`~graphein.protein.config.ProteinGraphConfig` object. If None, defaults to config in ``graphein.protein.config``.
    :type config: graphein.protein.config.ProteinGraphConfig, optional
    :param name: an optional given name for the graph. the PDB ID or PDB file name will be used if not specified.
    :type name: str, optional
    :param pdb_path: Path to ``pdb_file`` when constructing a graph from a local pdb file. Default is ``None``.
    :type pdb_path: Optional[str], defaults to ``None``
    :param pdb_code: A 4-character PDB ID / accession to be used to construct the graph, if available. Default is ``None``.
    :type pdb_code: Optional[str], defaults to ``None``
    :param chain_selection: String of polypeptide chains to include in graph. E.g ``"ABDF"`` or ``"all"``. Default is ``"all"``.
    :type chain_selection: str
    :param df_processing_funcs: List of dataframe processing functions. Default is ``None``.
    :type df_processing_funcs: List[Callable], optional
    :param edge_construction_funcs: List of edge construction functions. Default is ``None``.
    :type edge_construction_funcs: List[Callable], optional
    :param edge_annotation_funcs: List of edge annotation functions. Default is ``None``.
    :type edge_annotation_funcs: List[Callable], optional
    :param node_annotation_funcs: List of node annotation functions. Default is ``None``.
    :type node_annotation_funcs: List[Callable], optional
    :param graph_annotation_funcs: List of graph annotation function. Default is ``None``.
    :type graph_annotation_funcs: List[Callable]
    :return: Protein Structure Graph
    :type: nx.Graph
    """

    assert (pdb_code and not pdb_path) or (not pdb_code and pdb_path), (
        "Either a PDB ID or a path to a local PDB file"
        " must be specified to construct a graph"
    )

    # If no config is provided, use default
    if config is None:
        config = ProteinGraphConfig()

    # If config params are provided, overwrite them
    config.protein_df_processing_functions = (
        df_processing_funcs
        if config.protein_df_processing_functions is None
        else config.protein_df_processing_functions
    )
    config.edge_construction_functions = (
        edge_construction_funcs
        if config.edge_construction_functions is None
        else config.edge_construction_functions
    )
    config.node_metadata_functions = (
        node_annotation_funcs
        if config.node_metadata_functions is None
        else config.node_metadata_functions
    )
    config.graph_metadata_functions = (
        graph_annotation_funcs
        if config.graph_metadata_functions is None
        else config.graph_metadata_functions
    )
    config.edge_metadata_functions = (
        edge_annotation_funcs
        if config.edge_metadata_functions is None
        else config.edge_metadata_functions
    )

    raw_df = read_pdb_to_dataframe(
        pdb_path,
        pdb_code,
        verbose=config.verbose,
        granularity=config.granularity,
    )
    protein_df = process_dataframe(
        raw_df,
        chain_selection=chain_selection,
        granularity=config.granularity,
        insertions=config.insertions,
    )

    # Initialise graph with metadata
    g = initialise_graph_with_metadata(
        protein_df=protein_df,
        raw_pdb_df=raw_df.df["ATOM"],
        name=name,
        pdb_code=pdb_code,
        pdb_path=pdb_path,
        granularity=config.granularity,
    )
    # Add nodes to graph
    g = add_nodes_to_graph(g)

    # Add config to graph
    g.graph["config"] = config

    # Annotate additional node metadata
    if config.node_metadata_functions is not None:
        g = annotate_node_metadata(g, config.node_metadata_functions)

    # Compute graph edges
    g = compute_edges(
        g,
        funcs=config.edge_construction_functions,
        get_contacts_config=None,
    )

    # Annotate additional graph metadata
    if config.graph_metadata_functions is not None:
        g = annotate_graph_metadata(g, config.graph_metadata_functions)

    # Annotate additional edge metadata
    if config.edge_metadata_functions is not None:
        g = annotate_edge_metadata(g, config.edge_metadata_functions)

    return g


def _mp_graph_constructor(
    args: Tuple[str, str], use_pdb_code: bool, config: ProteinGraphConfig
) -> nx.Graph:
    """
    Protein graph constructor for use in multiprocessing several protein structure graphs.

    :param args: Tuple of pdb code/path and the chain selection for that PDB
    :type args: Tuple[str, str]
    :param use_pdb_code: Whether or not we are using pdb codes or paths
    :type use_pdb_code: bool
    :param config: Protein structure graph construction config
    :type config: ProteinGraphConfig
    :return: Protein structure graph
    :rtype: nx.Graph
    """
    log.info(f"Constructing graph for: {args[0]}. Chain selection: {args[1]}")
    func = partial(construct_graph, config=config)
    try:
        return (
            func(pdb_code=args[0], chain_selection=args[1])
            if use_pdb_code
            else func(pdb_path=args[0], chain_selection=args[1])
        )

    except Exception as ex:
        log.info(
            f"Graph construction error (PDB={args[0]})! {traceback.format_exc()}"
        )
        log.info(ex)
        return None


def construct_graphs_mp(
    pdb_code_it: Optional[List[str]] = None,
    pdb_path_it: Optional[List[str]] = None,
    chain_selections: Optional[list[str]] = None,
    config: ProteinGraphConfig = ProteinGraphConfig(),
    num_cores: int = 16,
    return_dict: bool = True,
    out_path: Optional[str] = None,
) -> Union[List[nx.Graph], Dict[str, nx.Graph]]:
    """
    Constructs protein graphs for a list of pdb codes or pdb paths using multiprocessing.

    :param pdb_code_it: List of pdb codes to use for protein graph construction
    :type pdb_code_it: Optional[List[str]], defaults to ``None``
    :param pdb_path_it: List of paths to PDB files to use for protein graph construction
    :type pdb_path_it: Optional[List[str]], defaults to ``None``
    :param chain_selections: List of chains to select from the protein structures (e.g. ``["ABC", "A", "L", "CD"...]``)
    :type chain_selections: Optional[List[str]], defaults to ``None``
    :param config: ProteinGraphConfig to use.
    :type config: graphein.protein.config.ProteinGraphConfig, defaults to default config params
    :param num_cores: Number of cores to use for multiprocessing. The more the merrier
    :type num_cores: int, defaults to ``16``
    :param return_dict: Whether or not to return a dictionary (indexed by pdb codes/paths) or a list of graphs.
    :type return_dict: bool, default to ``True``
    :param out_path: Path to save the graphs to. If None, graphs are not saved.
    :type out_path: Optional[str], defaults to ``None``
    :return: Iterable of protein graphs. None values indicate there was a problem in constructing the graph for this particular pdb
    :rtype: Union[List[nx.Graph], Dict[str, nx.Graph]]
    """
    assert (
        pdb_code_it is not None or pdb_path_it is not None
    ), "Iterable of pdb codes OR pdb paths required."

    if pdb_code_it is not None:
        pdbs = pdb_code_it
        use_pdb_code = True

    if pdb_path_it is not None:
        pdbs = pdb_path_it
        use_pdb_code = False

    if chain_selections is None:
        chain_selections = ["all"] * len(pdbs)

    constructor = partial(
        _mp_graph_constructor, use_pdb_code=use_pdb_code, config=config
    )

    graphs = list(
        process_map(
            constructor,
            [(pdb, chain_selections[i]) for i, pdb in enumerate(pdbs)],
            max_workers=num_cores,
        )
    )
    if out_path is not None:
        [
            nx.write_gpickle(
                g, str(f"{out_path}/" + f"{g.graph['name']}.pickle")
            )
            for g in graphs
        ]

    if return_dict:
        graphs = {pdb: graphs[i] for i, pdb in enumerate(pdbs)}

    return graphs


def compute_chain_graph(
    g: nx.Graph,
    chain_list: Optional[List[str]] = None,
    remove_self_loops: bool = False,
    return_weighted_graph: bool = False,
) -> Union[nx.Graph, nx.MultiGraph]:
    """Computes a chain-level graph from a protein structure graph.

    This graph features nodes as individual chains in a complex and edges as
    the interactions between constituent nodes in each chain. You have the
    option of returning an unweighted graph (multigraph,
    ``return_weighted_graph=False``) or a weighted graph
    (``return_weighted_graph=True``). The difference between these is the
    unweighted graph features and edge for each interaction between chains
    (ie the number of edges will be equal to the number of edges in the input
    protein structure graph), while the weighted graph sums these interactions
    to a single edge between chains with the counts stored as features.

    :param g: A protein structure graph to compute the chain graph of.
    :type g: nx.Graph
    :param chain_list: A list of chains to extract from the input graph.
        If ``None``, all chains will be used. This is provided as input to
        ``extract_subgraph_from_chains``. Default is ``None``.
    :type chain_list: Optional[List[str]]
    :param remove_self_loops: Whether to remove self-loops from the graph.
        Default is False.
    :type remove_self_loops: bool
    :return: A chain-level graph.
    :rtype: Union[nx.Graph, nx.MultiGraph]
    """
    # If we are extracting specific chains, do it here.
    if chain_list is not None:
        g = extract_subgraph_from_chains(g, chain_list)

    # Initialise new graph with Metadata
    h = nx.MultiGraph()
    h.graph = g.graph
    h.graph["node_type"] = "chain"

    # Set nodes
    nodes_per_chain = {chain: 0 for chain in g.graph["chain_ids"]}
    sequences = {chain: "" for chain in g.graph["chain_ids"]}
    for n, d in g.nodes(data=True):
        nodes_per_chain[d["chain_id"]] += 1
        sequences[d["chain_id"]] += RESI_THREE_TO_1[d["residue_name"]]

    h.add_nodes_from(g.graph["chain_ids"])

    for n, d in h.nodes(data=True):
        d["num_residues"] = nodes_per_chain[n]
        d["sequence"] = sequences[n]

    # Add edges
    for u, v, d in g.edges(data=True):
        h.add_edge(
            g.nodes[u]["chain_id"], g.nodes[v]["chain_id"], kind=d["kind"]
        )
    # Remove self-loops if necessary. Checks for equality between nodes in a given edge.
    if remove_self_loops:
        edges_to_remove: List[Tuple[str]] = [
            (u, v) for u, v in h.edges() if u == v
        ]
        h.remove_edges_from(edges_to_remove)

    # Compute a weighted graph if required.
    if return_weighted_graph:
        return compute_weighted_graph_from_multigraph(h)
    return h


def compute_weighted_graph_from_multigraph(g: nx.MultiGraph) -> nx.Graph:
    """Computes a weighted graph from a multigraph.

    This function is used to convert a multigraph to a weighted graph. The
    weights of the edges are the number of interactions between the nodes.

    :param g: A multigraph.
    :type g: nx.MultiGraph
    :return: A weighted graph.
    :rtype: nx.Graph
    """
    H = nx.Graph()
    H.graph = g.graph
    H.add_nodes_from(g.nodes(data=True))
    for u, v, d in g.edges(data=True):
        if H.has_edge(u, v):
            H[u][v]["weight"] += len(d["kind"])
            H[u][v]["kind"].update(d["kind"])
            for kind in list(d["kind"]):
                try:
                    H[u][v][kind] += 1
                except KeyError:
                    H[u][v][kind] = 1
        else:
            H.add_edge(u, v, weight=len(d["kind"]), kind=d["kind"])
            for kind in list(d["kind"]):
                H[u][v][kind] = 1
    return H


def number_groups_of_runs(list_of_values: List[Any]) -> List[str]:
    """Numbers groups of runs in a list of values.

    E.g. ``["A", "A", "B", "A", "A", "A", "B", "B"] ->
    ["A1", "A1", "B1", "A2", "A2", "A2", "B2", "B2"]``

    :param list_of_values: List of values to number.
    :type list_of_values: List[Any]
    :return: List of numbered values.
    :rtype: List[str]
    """
    df = pd.DataFrame({"val": list_of_values})
    df["idx"] = df["val"].shift() != df["val"]
    df["sum"] = df.groupby("val")["idx"].cumsum()
    return list(df["val"].astype(str) + df["sum"].astype(str))


def compute_secondary_structure_graph(
    g: nx.Graph,
    allowable_ss_elements: Optional[List[str]] = None,
    remove_non_ss: bool = True,
    remove_self_loops: bool = False,
    return_weighted_graph: bool = False,
) -> Union[nx.Graph, nx.MultiGraph]:
    """Computes a secondary structure graph from a protein structure graph.

    :param g: A protein structure graph to compute the secondary structure
        graph of.
    :type g: nx.Graph
    :param remove_non_ss: Whether to remove non-secondary structure nodes from
        the graph. These are denoted as ``"-"`` by DSSP. Default is True.
    :type remove_non_ss: bool
    :param remove_self_loops: Whether to remove self-loops from the graph.
        Default is ``False``.
    :type remove_self_loops: bool
    :param return_weighted_graph: Whether to return a weighted graph.
        Default is False.
    :type return_weighted_graph: bool
    :raises ProteinGraphConfigurationError: If the protein structure graph is
        not configured correctly with secondary structure assignments on all
        nodes.
    :return: A secondary structure graph.
    :rtype: Union[nx.Graph, nx.MultiGraph]
    """
    # Initialise list of secondary structure elements we use to build the graph
    ss_list: List[str] = []

    # Check nodes have secondary structure assignment & store them in list
    for _, d in g.nodes(data=True):
        if "ss" not in d.keys():
            raise ProteinGraphConfigurationError(
                "Secondary structure not defined for all nodes."
            )
        ss_list.append(d["ss"])

    # Number SS elements
    ss_list = pd.Series(number_groups_of_runs(ss_list))
    ss_list.index = list(g.nodes())

    # Remove unstructured elements if necessary
    if remove_non_ss:
        ss_list = ss_list[~ss_list.str.contains("-")]
    # Subset to only allowable SS elements if necessary
    if allowable_ss_elements:
        ss_list = ss_list[
            ss_list.str.contains("|".join(allowable_ss_elements))
        ]

    constituent_residues: Dict[str, List[str]] = ss_list.index.groupby(
        ss_list.values
    )
    constituent_residues = {
        k: list(v) for k, v in constituent_residues.items()
    }
    residue_counts: Dict[str, int] = ss_list.groupby(ss_list).count().to_dict()

    # Add Nodes from secondary structure list
    h = nx.MultiGraph()
    h.add_nodes_from(ss_list)
    nx.set_node_attributes(h, residue_counts, "residue_counts")
    nx.set_node_attributes(h, constituent_residues, "constituent_residues")
    # Assign ss
    for n, d in h.nodes(data=True):
        d["ss"] = n[0]

    # Add graph-level metadata
    h.graph = g.graph
    h.graph["node_type"] = "secondary_structure"

    # Iterate over edges in source graph and add SS-SS edges to new graph.
    for u, v, d in g.edges(data=True):
        try:
            h.add_edge(
                ss_list[u], ss_list[v], kind=d["kind"], source=f"{u}_{v}"
            )
        except KeyError as e:
            log.debug(
                f"Edge {u}-{v} not added to secondary structure graph. \
                Reason: {e} not in graph"
            )

    # Remove self-loops if necessary.
    # Checks for equality between nodes in a given edge.
    if remove_self_loops:
        edges_to_remove: List[Tuple[str]] = [
            (u, v) for u, v in h.edges() if u == v
        ]
        h.remove_edges_from(edges_to_remove)

    # Create weighted graph from h
    if return_weighted_graph:
        return compute_weighted_graph_from_multigraph(h)
    return h
