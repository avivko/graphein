"""
Author: Eric J. Ma, Arian Jamasb
Purpose: This is a set of utility variables and functions that can be used
across the Graphein project.
"""

from typing import Dict, List

import numpy as np
from sklearn.preprocessing import StandardScaler

BACKBONE_ATOMS: List[str] = ["N", "CA", "C", "O"]


BASE_AMINO_ACIDS: List[str] = [
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
]

STANDARD_AMINO_ACIDS: List[str] = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

NON_STANDARD_AMINO_ACIDS: List[str] = ["O", "U"]

AMINO_ACIDS: List[str] = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

NON_STANDARD_AMINO_ACID_MAPPING_3_TO_1: Dict[str, str] = {
    "SEC": "U",
    "PYL": "O",
}

BOND_TYPES: List[str] = [
    "hydrophobic",
    "disulfide",
    "hbond",
    "ionic",
    "aromatic",
    "aromatic_sulphur",
    "cation_pi",
    "backbone",
    "delaunay",
]

STANDARD_RESI_NAMES: List[str] = [
    "ALA",
    "ASX",
    "CYS",
    "ASP",
    "GLU",
    "PHE",
    "GLY",
    "HIS",
    "ILE",
    "LYS",
    "LEU",
    "MET",
    "ASN",
    "PRO",
    "GLN",
    "ARG",
    "SER",
    "THR",
    "VAL",
    "TRP",
    "TYR",
    "GLX",
    "UNK",
]

NON_STANDARD_RESI_NAMES: List[str] = [
    "CSD",
    "HYP",
    "BMT",
    "5HP",
    "ACE",
    "ABA",
    "AIB",
    "NH2",
    "CBX",
    "CSW",
    "OCS",
    "DAL",
    "DAR",
    "DSG",
    "DSP",
    "DCY",
    "CRO",
    "DGL",
    "DGN",
    "DHI",
    "DIL",
    "DIV",
    "DLE",
    "DLY",
    "DPN",
    "DPR",
    "DSN",
    "DTH",
    "DTR",
    "DTY",
    "DVA",
    "FOR",
    "CGU",
    "IVA",
    "KCX",
    "LLP",
    "CXM",
    "FME",
    "MLE",
    "MVA",
    "NLE",
    "PTR",
    "ORN",
    "SEP",
    "SEC",
    "TPO",
    "PCA",
    "PVL",
    "PYL",
    "SAR",
    "CEA",
    "CSO",
    "CSS",
    "CSX",
    "CME",
    "TYS",
    "BOC",
    "TPQ",
    "STY",
]

RESI_NAMES: List[str] = [
    "ALA",
    "ASX",
    "CYS",
    "ASP",
    "GLU",
    "PHE",
    "GLY",
    "HIS",
    "ILE",
    "LYS",
    "LEU",
    "MET",
    "ASN",
    "PRO",
    "GLN",
    "ARG",
    "SER",
    "THR",
    "VAL",
    "TRP",
    "TYR",
    "GLX",
    "CSD",
    "HYP",
    "BMT",
    "5HP",
    "ACE",
    "ABA",
    "AIB",
    "NH2",
    "CBX",
    "CSW",
    "OCS",
    "DAL",
    "DAR",
    "DSG",
    "DSP",
    "DCY",
    "CRO",
    "DGL",
    "DGN",
    "DHI",
    "DIL",
    "DIV",
    "DLE",
    "DLY",
    "DPN",
    "DPR",
    "DSN",
    "DTH",
    "DTR",
    "DTY",
    "DVA",
    "FOR",
    "CGU",
    "IVA",
    "KCX",
    "LLP",
    "CXM",
    "FME",
    "MLE",
    "MVA",
    "NLE",
    "PTR",
    "ORN",
    "SEP",
    "SEC",
    "TPO",
    "PCA",
    "PVL",
    "PYL",
    "SAR",
    "CEA",
    "CSO",
    "CSS",
    "CSX",
    "CME",
    "TYS",
    "BOC",
    "TPQ",
    "STY",
    "UNK",
]

# https://www.ebi.ac.uk/pdbe-srv/pdbechem/chemicalCompound
RESI_THREE_TO_1: Dict[str, str] = {
    "ALA": "A",
    "ASX": "B",
    "CYS": "C",
    "ASP": "D",
    "GLU": "E",
    "PHE": "F",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LYS": "K",
    "LEU": "L",
    "MET": "M",
    "ASN": "N",
    "PRO": "P",
    "GLN": "Q",
    "ARG": "R",
    "SER": "S",
    "THR": "T",
    "VAL": "V",
    "TRP": "W",
    "TYR": "Y",
    "GLX": "Z",
    "CSD": "C",
    "HYP": "P",
    "BMT": "T",
    "3HP": "X",
    "4HP": "X",
    "5HP": "Q",
    "ACE": "X",
    "ABA": "A",
    "AIB": "A",
    "NH2": "X",
    "CBX": "X",
    "CSW": "C",
    "OCS": "C",
    "DAL": "A",
    "DAR": "R",
    "DSG": "N",
    "DSP": "D",
    "DCY": "C",
    "CRO": "TYG",
    "DGL": "E",
    "DGN": "Q",
    "DHI": "H",
    "DIL": "I",
    "DIV": "V",
    "DLE": "L",
    "DLY": "K",
    "DPN": "F",
    "DPR": "P",
    "DSN": "S",
    "DTH": "T",
    "DTR": "W",
    "DTY": "Y",
    "DVA": "V",
    "FOR": "X",
    "CGU": "E",
    "IVA": "X",
    "KCX": "K",
    "LLP": "K",
    "CXM": "M",
    "FME": "M",
    "MLE": "L",
    "MVA": "V",
    "NLE": "L",
    "PTR": "Y",
    "ORN": "A",
    "SEP": "S",
    "SEC": "U",
    "TPO": "T",
    "PCA": "Q",
    "PVL": "X",
    "PYL": "O",
    "SAR": "G",
    "CEA": "C",
    "CSO": "C",
    "CSS": "C",
    "CSX": "C",
    "CME": "C",
    "TYS": "Y",
    "BOC": "X",
    "TPQ": "Y",
    "STY": "Y",
    "UNK": "X",
}


# Non-standard residue info taken from: https://www.globalphasing.com/buster/manual/maketnt/manual/lib_val/library_validation.html
# PYL (pyrolysine) and SEC are added

NON_STANDARD_RESIS_NAME: List[str] = [
    "3-SULFINOALANINE",
    "4-HYDROXYPROLINE",
    "4-METHYL-4-[(E)-2-BUTENYL]-4,N-METHYL-THREONINE",
    "5-HYDROXYPROLINE",
    "ACETYL_GROUP",
    "ALPHA-AMINOBUTYRIC_ACID",
    "ALPHA-AMINOISOBUTYRIC_ACID",
    "AMINO_GROUP",
    "CARBOXY_GROUP",
    "CYSTEINE-S-DIOXIDE",
    "CYSTEINESULFONIC_ACID",
    "D-ALANINE",
    "D-ARGININE",
    "D-ASPARAGINE",
    "D-ASPARTATE",
    "D-CYSTEINE",
    "DECARBOXY(PARAHYDROXYBENZYLIDENE-IMIDAZOLIDINONE)THREONINE",
    "D-GLUTAMATE",
    "D-GLUTAMINE",
    "D-HISTIDINE",
    "D-ISOLEUCINE",
    "D-ISOVALINE",
    "D-LEUCINE",
    "D-LYSINE",
    "D-PHENYLALANINE",
    "D-PROLINE",
    "D-SERINE",
    "D-THREONINE",
    "D-TRYPTOPHANE",
    "D-TYROSINE",
    "D-VALINE",
    "FORMYL_GROUP",
    "GAMMA-CARBOXY-GLUTAMIC_ACID",
    "ISOVALERIC_ACID",
    "LYSINE_NZ-CARBOXYLIC_ACID",
    "LYSINE-PYRIDOXAL-5'-PHOSPHATE",
    "N-CARBOXYMETHIONINE",
    "N-FORMYLMETHIONINE",
    "N-METHYLLEUCINE",
    "N-METHYLVALINE",
    "NORLEUCINE",
    "O-PHOSPHOTYROSINE",
    "ORNITHINE",
    "PHOSPHOSERINE",
    "PHOSPHOTHREONINE",
    "PYROGLUTAMIC_ACID",
    "PYRUVOYL_GROUP",
    "SARCOSINE",
    "S-HYDROXY-CYSTEINE",
    "S-HYDROXYCYSTEINE",
    "S-MERCAPTOCYSTEINE",
    "S-OXY_CYSTEINE",
    "S,S-(2-HYDROXYETHYL)THIOCYSTEINE",
    "SULFONATED_TYROSINE",
    "TERT-BUTYLOXYCARBONYL_GROUP",
    "TOPO-QUINONE",
    "TYROSINE-O-SULPHONIC_ACID",
]

NON_STANDARD_RESIS_PARENT: Dict[str, str] = {
    "CSD": "CYS",
    "HYP": "PRO",
    "BMT": "THR",
    "5HP": "GLU",
    "ACE": "-",
    "ABA": "ALA",
    "AIB": "ALA",
    "NH2": "-",
    "CBX": "-",
    "CSW": "CYS",
    "OCS": "CYS",
    "DAL": "ALA",
    "DAR": "ARG",
    "DSG": "ASN",
    "DSP": "ASP",
    "DCY": "CYS",
    "CRO": "CRO",
    "DGL": "GLU",
    "DGN": "GLN",
    "DHI": "HIS",
    "DIL": "ILE",
    "DIV": "VAL",
    "DLE": "LEU",
    "DLY": "LYS",
    "DPN": "PHE",
    "DPR": "PRO",
    "DSN": "SER",
    "DTH": "THR",
    "DTR": "DTR",
    "DTY": "TYR",
    "DVA": "VAL",
    "FOR": "-",
    "CGU": "GLU",
    "IVA": "-",
    "KCX": "LYS",
    "LLP": "LYS",
    "PYL": "LYS",
    "CXM": "MET",
    "FME": "MET",
    "MLE": "LEU",
    "MVA": "VAL",
    "NLE": "LEU",
    "PTR": "TYR",
    "ORN": "ALA",
    "SEP": "SER",
    "TPO": "THR",
    "PCA": "GLU",
    "PVL": "-",
    "SAR": "GLY",
    "CEA": "CYS",
    "CSO": "CYS",
    "CSS": "CYS",
    "CSX": "CYS",
    "CME": "CYS",
    "SEC": "CYS",
    "TYS": "TYR",
    "BOC": "-",
    "TPQ": "PHE",
    "STY": "TYR",
}

COFACTOR_NAMES: List[str] = [
    "ADP",
    "AMP",
    "ATP",
    "cAMP",
    "COENZYME_A",
    "FAD",
    "FLAVIN_MONONUCLEOTIDE",
    "NADP",
    "NADPH",
]

COFACTOR_CODES: List[str] = [
    "ADP",
    "AMP",
    "ATP",
    "CMP",
    "COA",
    "FAD",
    "FMN",
    "NAP",
    "NDP",
]

COFACTOR_CODE_NAME_MAPPING: Dict[str, str] = {
    "ADP": "ADP",
    "AMP": "AMP",
    "ATP": "ATP",
    "CMP": "cAMP",
    "COA": "COENZYME_A",
    "FAD": "FAD",
    "FMN": "FLAVIN_MONONUCLEOTIDE",
    "NAP": "NADP",
    "NDP": "NADPH",
}

CARBOHYDRATE_NAMES: List[str] = [
    "D-GLUCOSE",
    "D-MANNOSE",
    "FUCOSE",
    "D-GALACTOSE",
    "N-ACETYL-D-GLUCOSAMINE",
    "N-ACETYL-D-GALACTOSAMINE",
    "O-SIALIC_ACID",
    "D-XYLOPYRANOSE",
]

CARBOHYDRATE_CODES: List[str] = [
    "BGC",
    "GLC",
    "MAN",
    "BMA",
    "FUC",
    "GAL",
    "GLA",
    "NAG",
    "NGA",
    "SIA",
    "XYS",
]

CARBOHYDRATE_CODE_NAME_MAPPING: Dict[str, str] = {
    "BGC": "D-GLUCOSE",
    "GLC": "D-GLUCOSE",
    "MAN": "D-MANNOSE",
    "BMA": "D-MANNOSE",
    "FUC": "FUCOSE",
    "GAL": "D-GALACTOSE",
    "GLA": "D-GALACTOSE",
    "NAG": "N-ACETYL-D-GLUCOSAMINE",
    "NGA": "N-ACETYL-D-GALACTOSAMINE",
    "SIA": "O-SIALIC_ACID",
    "XYS": "D-XYLOPYRANOSE",
}

HYDROPHOBIC_RESIS: List[str] = [
    "ALA",
    "VAL",
    "LEU",
    "ILE",
    "MET",
    "PHE",
    "TRP",
    "PRO",
    "TYR",
]

DISULFIDE_RESIS: List[str] = ["CYS"]

DISULFIDE_ATOMS: List[str] = ["SG"]

IONIC_RESIS: List[str] = ["ARG", "LYS", "HIS", "ASP", "GLU"]

POS_AA: List[str] = ["HIS", "LYS", "ARG"]

NEG_AA: List[str] = ["GLU", "ASP"]

AA_RING_ATOMS: Dict[str, List[str]] = dict()
AA_RING_ATOMS["PHE"] = ["CG", "CD", "CE", "CZ"]
AA_RING_ATOMS["TRP"] = ["CD", "CE", "CH", "CZ"]
AA_RING_ATOMS["HIS"] = ["CG", "CD", "CE", "ND", "NE"]
AA_RING_ATOMS["TYR"] = ["CG", "CD", "CE", "CZ"]

AROMATIC_RESIS: List[str] = ["PHE", "TRP", "HIS", "TYR"]

CATION_PI_RESIS: List[str] = ["LYS", "ARG", "PHE", "TYR", "TRP"]

CATION_RESIS: List[str] = ["LYS", "ARG"]

PI_RESIS: List[str] = ["PHE", "TYR", "TRP"]

SULPHUR_RESIS: List[str] = ["MET", "CYS"]

ISOELECTRIC_POINTS: Dict[str, float] = {
    "ALA": 6.11,
    "ARG": 10.76,
    "ASN": 10.76,
    "ASP": 2.98,
    "CYS": 5.02,
    "GLU": 3.08,
    "GLN": 5.65,
    "GLY": 6.06,
    "HIS": 7.64,
    "ILE": 6.04,
    "LEU": 6.04,
    "LYS": 9.74,
    "MET": 5.74,
    "PHE": 5.91,
    "PRO": 6.30,
    "SER": 5.68,
    "THR": 5.60,
    "TRP": 5.88,
    "TYR": 5.63,
    "VAL": 6.02,
    "UNK": 7.00,  # unknown so assign neutral
    "ASX": 6.87,  # the average of D and N
    "GLX": 4.35,  # the average of E and Q
}

scaler = StandardScaler()
scaler.fit(np.array([v for v in ISOELECTRIC_POINTS.values()]).reshape(-1, 1))

ISOELECTRIC_POINTS_STD = dict()
for k, v in ISOELECTRIC_POINTS.items():
    ISOELECTRIC_POINTS_STD[k] = scaler.transform(np.array([v]).reshape(-1, 1))

MOLECULAR_WEIGHTS: Dict[str, float] = {
    "ALA": 89.0935,
    "ARG": 174.2017,
    "ASN": 132.1184,
    "ASP": 133.1032,
    "CYS": 121.1590,
    "GLU": 147.1299,
    "GLN": 146.1451,
    "GLY": 75.0669,
    "HIS": 155.1552,
    "ILE": 131.1736,
    "LEU": 131.1736,
    "LYS": 146.1882,
    "MET": 149.2124,
    "PHE": 165.1900,
    "PRO": 115.1310,
    "SER": 105.0930,
    "THR": 119.1197,
    "TRP": 204.2262,
    "TYR": 181.1894,
    "VAL": 117.1469,
    "UNK": 137.1484,  # unknown, therefore assign average of knowns
    "ASX": 132.6108,  # the average of D and N
    "GLX": 146.6375,  # the average of E and Q
}

MOLECULAR_WEIGHTS_STD = dict()

scaler.fit(np.array([v for v in MOLECULAR_WEIGHTS.values()]).reshape(-1, 1))
MOLECULAR_WEIGHTS_STD = dict()
for k, v in MOLECULAR_WEIGHTS.items():
    MOLECULAR_WEIGHTS_STD[k] = scaler.transform(np.array([v]).reshape(-1, 1))

# Grantham Chemical Distance Matrix. Taken from ProPy3.
# Amino Acid Difference Formula to Help Explain Protein Evolution
# R. Grantham
# Science
# Vol 185, Issue 4154
# 06 September 1974
# Paper: https://science.sciencemag.org/content/185/4154/862/tab-pdf
GRANTHAM_CHEMICAL_DISTANCE_MATRIX: Dict[str, float] = {
    "AA": 0.0,
    "AC": 0.112,
    "AD": 0.819,
    "AE": 0.827,
    "AF": 0.54,
    "AG": 0.208,
    "AH": 0.696,
    "AI": 0.407,
    "AK": 0.891,
    "AL": 0.406,
    "AM": 0.379,
    "AN": 0.318,
    "AP": 0.191,
    "AQ": 0.372,
    "AR": 1.0,
    "AS": 0.094,
    "AT": 0.22,
    "AV": 0.273,
    "AW": 0.739,
    "AY": 0.552,
    "CA": 0.114,
    "CC": 0.0,
    "CD": 0.847,
    "CE": 0.838,
    "CF": 0.437,
    "CG": 0.32,
    "CH": 0.66,
    "CI": 0.304,
    "CK": 0.887,
    "CL": 0.301,
    "CM": 0.277,
    "CN": 0.324,
    "CP": 0.157,
    "CQ": 0.341,
    "CR": 1.0,
    "CS": 0.176,
    "CT": 0.233,
    "CV": 0.167,
    "CW": 0.639,
    "CY": 0.457,
    "DA": 0.729,
    "DC": 0.742,
    "DD": 0.0,
    "DE": 0.124,
    "DF": 0.924,
    "DG": 0.697,
    "DH": 0.435,
    "DI": 0.847,
    "DK": 0.249,
    "DL": 0.841,
    "DM": 0.819,
    "DN": 0.56,
    "DP": 0.657,
    "DQ": 0.584,
    "DR": 0.295,
    "DS": 0.667,
    "DT": 0.649,
    "DV": 0.797,
    "DW": 1.0,
    "DY": 0.836,
    "EA": 0.79,
    "EC": 0.788,
    "ED": 0.133,
    "EE": 0.0,
    "EF": 0.932,
    "EG": 0.779,
    "EH": 0.406,
    "EI": 0.86,
    "EK": 0.143,
    "EL": 0.854,
    "EM": 0.83,
    "EN": 0.599,
    "EP": 0.688,
    "EQ": 0.598,
    "ER": 0.234,
    "ES": 0.726,
    "ET": 0.682,
    "EV": 0.824,
    "EW": 1.0,
    "EY": 0.837,
    "FA": 0.508,
    "FC": 0.405,
    "FD": 0.977,
    "FE": 0.918,
    "FF": 0.0,
    "FG": 0.69,
    "FH": 0.663,
    "FI": 0.128,
    "FK": 0.903,
    "FL": 0.131,
    "FM": 0.169,
    "FN": 0.541,
    "FP": 0.42,
    "FQ": 0.459,
    "FR": 1.0,
    "FS": 0.548,
    "FT": 0.499,
    "FV": 0.252,
    "FW": 0.207,
    "FY": 0.179,
    "GA": 0.206,
    "GC": 0.312,
    "GD": 0.776,
    "GE": 0.807,
    "GF": 0.727,
    "GG": 0.0,
    "GH": 0.769,
    "GI": 0.592,
    "GK": 0.894,
    "GL": 0.591,
    "GM": 0.557,
    "GN": 0.381,
    "GP": 0.323,
    "GQ": 0.467,
    "GR": 1.0,
    "GS": 0.158,
    "GT": 0.272,
    "GV": 0.464,
    "GW": 0.923,
    "GY": 0.728,
    "HA": 0.896,
    "HC": 0.836,
    "HD": 0.629,
    "HE": 0.547,
    "HF": 0.907,
    "HG": 1.0,
    "HH": 0.0,
    "HI": 0.848,
    "HK": 0.566,
    "HL": 0.842,
    "HM": 0.825,
    "HN": 0.754,
    "HP": 0.777,
    "HQ": 0.716,
    "HR": 0.697,
    "HS": 0.865,
    "HT": 0.834,
    "HV": 0.831,
    "HW": 0.981,
    "HY": 0.821,
    "IA": 0.403,
    "IC": 0.296,
    "ID": 0.942,
    "IE": 0.891,
    "IF": 0.134,
    "IG": 0.592,
    "IH": 0.652,
    "II": 0.0,
    "IK": 0.892,
    "IL": 0.013,
    "IM": 0.057,
    "IN": 0.457,
    "IP": 0.311,
    "IQ": 0.383,
    "IR": 1.0,
    "IS": 0.443,
    "IT": 0.396,
    "IV": 0.133,
    "IW": 0.339,
    "IY": 0.213,
    "KA": 0.889,
    "KC": 0.871,
    "KD": 0.279,
    "KE": 0.149,
    "KF": 0.957,
    "KG": 0.9,
    "KH": 0.438,
    "KI": 0.899,
    "KK": 0.0,
    "KL": 0.892,
    "KM": 0.871,
    "KN": 0.667,
    "KP": 0.757,
    "KQ": 0.639,
    "KR": 0.154,
    "KS": 0.825,
    "KT": 0.759,
    "KV": 0.882,
    "KW": 1.0,
    "KY": 0.848,
    "LA": 0.405,
    "LC": 0.296,
    "LD": 0.944,
    "LE": 0.892,
    "LF": 0.139,
    "LG": 0.596,
    "LH": 0.653,
    "LI": 0.013,
    "LK": 0.893,
    "LL": 0.0,
    "LM": 0.062,
    "LN": 0.452,
    "LP": 0.309,
    "LQ": 0.376,
    "LR": 1.0,
    "LS": 0.443,
    "LT": 0.397,
    "LV": 0.133,
    "LW": 0.341,
    "LY": 0.205,
    "MA": 0.383,
    "MC": 0.276,
    "MD": 0.932,
    "ME": 0.879,
    "MF": 0.182,
    "MG": 0.569,
    "MH": 0.648,
    "MI": 0.058,
    "MK": 0.884,
    "ML": 0.062,
    "MM": 0.0,
    "MN": 0.447,
    "MP": 0.285,
    "MQ": 0.372,
    "MR": 1.0,
    "MS": 0.417,
    "MT": 0.358,
    "MV": 0.12,
    "MW": 0.391,
    "MY": 0.255,
    "NA": 0.424,
    "NC": 0.425,
    "ND": 0.838,
    "NE": 0.835,
    "NF": 0.766,
    "NG": 0.512,
    "NH": 0.78,
    "NI": 0.615,
    "NK": 0.891,
    "NL": 0.603,
    "NM": 0.588,
    "NN": 0.0,
    "NP": 0.266,
    "NQ": 0.175,
    "NR": 1.0,
    "NS": 0.361,
    "NT": 0.368,
    "NV": 0.503,
    "NW": 0.945,
    "NY": 0.641,
    "PA": 0.22,
    "PC": 0.179,
    "PD": 0.852,
    "PE": 0.831,
    "PF": 0.515,
    "PG": 0.376,
    "PH": 0.696,
    "PI": 0.363,
    "PK": 0.875,
    "PL": 0.357,
    "PM": 0.326,
    "PN": 0.231,
    "PP": 0.0,
    "PQ": 0.228,
    "PR": 1.0,
    "PS": 0.196,
    "PT": 0.161,
    "PV": 0.244,
    "PW": 0.72,
    "PY": 0.481,
    "QA": 0.512,
    "QC": 0.462,
    "QD": 0.903,
    "QE": 0.861,
    "QF": 0.671,
    "QG": 0.648,
    "QH": 0.765,
    "QI": 0.532,
    "QK": 0.881,
    "QL": 0.518,
    "QM": 0.505,
    "QN": 0.181,
    "QP": 0.272,
    "QQ": 0.0,
    "QR": 1.0,
    "QS": 0.461,
    "QT": 0.389,
    "QV": 0.464,
    "QW": 0.831,
    "QY": 0.522,
    "RA": 0.919,
    "RC": 0.905,
    "RD": 0.305,
    "RE": 0.225,
    "RF": 0.977,
    "RG": 0.928,
    "RH": 0.498,
    "RI": 0.929,
    "RK": 0.141,
    "RL": 0.92,
    "RM": 0.908,
    "RN": 0.69,
    "RP": 0.796,
    "RQ": 0.668,
    "RR": 0.0,
    "RS": 0.86,
    "RT": 0.808,
    "RV": 0.914,
    "RW": 1.0,
    "RY": 0.859,
    "SA": 0.1,
    "SC": 0.185,
    "SD": 0.801,
    "SE": 0.812,
    "SF": 0.622,
    "SG": 0.17,
    "SH": 0.718,
    "SI": 0.478,
    "SK": 0.883,
    "SL": 0.474,
    "SM": 0.44,
    "SN": 0.289,
    "SP": 0.181,
    "SQ": 0.358,
    "SR": 1.0,
    "SS": 0.0,
    "ST": 0.174,
    "SV": 0.342,
    "SW": 0.827,
    "SY": 0.615,
    "TA": 0.251,
    "TC": 0.261,
    "TD": 0.83,
    "TE": 0.812,
    "TF": 0.604,
    "TG": 0.312,
    "TH": 0.737,
    "TI": 0.455,
    "TK": 0.866,
    "TL": 0.453,
    "TM": 0.403,
    "TN": 0.315,
    "TP": 0.159,
    "TQ": 0.322,
    "TR": 1.0,
    "TS": 0.185,
    "TT": 0.0,
    "TV": 0.345,
    "TW": 0.816,
    "TY": 0.596,
    "VA": 0.275,
    "VC": 0.165,
    "VD": 0.9,
    "VE": 0.867,
    "VF": 0.269,
    "VG": 0.471,
    "VH": 0.649,
    "VI": 0.135,
    "VK": 0.889,
    "VL": 0.134,
    "VM": 0.12,
    "VN": 0.38,
    "VP": 0.212,
    "VQ": 0.339,
    "VR": 1.0,
    "VS": 0.322,
    "VT": 0.305,
    "VV": 0.0,
    "VW": 0.472,
    "VY": 0.31,
    "WA": 0.658,
    "WC": 0.56,
    "WD": 1.0,
    "WE": 0.931,
    "WF": 0.196,
    "WG": 0.829,
    "WH": 0.678,
    "WI": 0.305,
    "WK": 0.892,
    "WL": 0.304,
    "WM": 0.344,
    "WN": 0.631,
    "WP": 0.555,
    "WQ": 0.538,
    "WR": 0.968,
    "WS": 0.689,
    "WT": 0.638,
    "WV": 0.418,
    "WW": 0.0,
    "WY": 0.204,
    "YA": 0.587,
    "YC": 0.478,
    "YD": 1.0,
    "YE": 0.932,
    "YF": 0.202,
    "YG": 0.782,
    "YH": 0.678,
    "YI": 0.23,
    "YK": 0.904,
    "YL": 0.219,
    "YM": 0.268,
    "YN": 0.512,
    "YP": 0.444,
    "YQ": 0.404,
    "YR": 0.995,
    "YS": 0.612,
    "YT": 0.557,
    "YV": 0.328,
    "YW": 0.244,
    "YY": 0.0,
}


# Scheider-Wrede Physicochemical Distance Matrix taken from ProPy3.
# Paper: The rational design of amino acid sequences by artificial neural networks and simulated molecular evolution:
# de novo design of an idealized leader peptidase cleavage site
# Biophysical Journal
# Volume 66, Issue 2, Part 1, February 1994, Pages 335-344
# G.Schneider, P.Wrede

SCHNEIDER_WREDE_DISTMAT: Dict[str, float] = {
    "GW": 0.923,
    "GV": 0.464,
    "GT": 0.272,
    "GS": 0.158,
    "GR": 1.0,
    "GQ": 0.467,
    "GP": 0.323,
    "GY": 0.728,
    "GG": 0.0,
    "GF": 0.727,
    "GE": 0.807,
    "GD": 0.776,
    "GC": 0.312,
    "GA": 0.206,
    "GN": 0.381,
    "GM": 0.557,
    "GL": 0.591,
    "GK": 0.894,
    "GI": 0.592,
    "GH": 0.769,
    "ME": 0.879,
    "MD": 0.932,
    "MG": 0.569,
    "MF": 0.182,
    "MA": 0.383,
    "MC": 0.276,
    "MM": 0.0,
    "ML": 0.062,
    "MN": 0.447,
    "MI": 0.058,
    "MH": 0.648,
    "MK": 0.884,
    "MT": 0.358,
    "MW": 0.391,
    "MV": 0.12,
    "MQ": 0.372,
    "MP": 0.285,
    "MS": 0.417,
    "MR": 1.0,
    "MY": 0.255,
    "FP": 0.42,
    "FQ": 0.459,
    "FR": 1.0,
    "FS": 0.548,
    "FT": 0.499,
    "FV": 0.252,
    "FW": 0.207,
    "FY": 0.179,
    "FA": 0.508,
    "FC": 0.405,
    "FD": 0.977,
    "FE": 0.918,
    "FF": 0.0,
    "FG": 0.69,
    "FH": 0.663,
    "FI": 0.128,
    "FK": 0.903,
    "FL": 0.131,
    "FM": 0.169,
    "FN": 0.541,
    "SY": 0.615,
    "SS": 0.0,
    "SR": 1.0,
    "SQ": 0.358,
    "SP": 0.181,
    "SW": 0.827,
    "SV": 0.342,
    "ST": 0.174,
    "SK": 0.883,
    "SI": 0.478,
    "SH": 0.718,
    "SN": 0.289,
    "SM": 0.44,
    "SL": 0.474,
    "SC": 0.185,
    "SA": 0.1,
    "SG": 0.17,
    "SF": 0.622,
    "SE": 0.812,
    "SD": 0.801,
    "YI": 0.23,
    "YH": 0.678,
    "YK": 0.904,
    "YM": 0.268,
    "YL": 0.219,
    "YN": 0.512,
    "YA": 0.587,
    "YC": 0.478,
    "YE": 0.932,
    "YD": 1.0,
    "YG": 0.782,
    "YF": 0.202,
    "YY": 0.0,
    "YQ": 0.404,
    "YP": 0.444,
    "YS": 0.612,
    "YR": 0.995,
    "YT": 0.557,
    "YW": 0.244,
    "YV": 0.328,
    "LF": 0.139,
    "LG": 0.596,
    "LD": 0.944,
    "LE": 0.892,
    "LC": 0.296,
    "LA": 0.405,
    "LN": 0.452,
    "LL": 0.0,
    "LM": 0.062,
    "LK": 0.893,
    "LH": 0.653,
    "LI": 0.013,
    "LV": 0.133,
    "LW": 0.341,
    "LT": 0.397,
    "LR": 1.0,
    "LS": 0.443,
    "LP": 0.309,
    "LQ": 0.376,
    "LY": 0.205,
    "RT": 0.808,
    "RV": 0.914,
    "RW": 1.0,
    "RP": 0.796,
    "RQ": 0.668,
    "RR": 0.0,
    "RS": 0.86,
    "RY": 0.859,
    "RD": 0.305,
    "RE": 0.225,
    "RF": 0.977,
    "RG": 0.928,
    "RA": 0.919,
    "RC": 0.905,
    "RL": 0.92,
    "RM": 0.908,
    "RN": 0.69,
    "RH": 0.498,
    "RI": 0.929,
    "RK": 0.141,
    "VH": 0.649,
    "VI": 0.135,
    "EM": 0.83,
    "EL": 0.854,
    "EN": 0.599,
    "EI": 0.86,
    "EH": 0.406,
    "EK": 0.143,
    "EE": 0.0,
    "ED": 0.133,
    "EG": 0.779,
    "EF": 0.932,
    "EA": 0.79,
    "EC": 0.788,
    "VM": 0.12,
    "EY": 0.837,
    "VN": 0.38,
    "ET": 0.682,
    "EW": 1.0,
    "EV": 0.824,
    "EQ": 0.598,
    "EP": 0.688,
    "ES": 0.726,
    "ER": 0.234,
    "VP": 0.212,
    "VQ": 0.339,
    "VR": 1.0,
    "VT": 0.305,
    "VW": 0.472,
    "KC": 0.871,
    "KA": 0.889,
    "KG": 0.9,
    "KF": 0.957,
    "KE": 0.149,
    "KD": 0.279,
    "KK": 0.0,
    "KI": 0.899,
    "KH": 0.438,
    "KN": 0.667,
    "KM": 0.871,
    "KL": 0.892,
    "KS": 0.825,
    "KR": 0.154,
    "KQ": 0.639,
    "KP": 0.757,
    "KW": 1.0,
    "KV": 0.882,
    "KT": 0.759,
    "KY": 0.848,
    "DN": 0.56,
    "DL": 0.841,
    "DM": 0.819,
    "DK": 0.249,
    "DH": 0.435,
    "DI": 0.847,
    "DF": 0.924,
    "DG": 0.697,
    "DD": 0.0,
    "DE": 0.124,
    "DC": 0.742,
    "DA": 0.729,
    "DY": 0.836,
    "DV": 0.797,
    "DW": 1.0,
    "DT": 0.649,
    "DR": 0.295,
    "DS": 0.667,
    "DP": 0.657,
    "DQ": 0.584,
    "QQ": 0.0,
    "QP": 0.272,
    "QS": 0.461,
    "QR": 1.0,
    "QT": 0.389,
    "QW": 0.831,
    "QV": 0.464,
    "QY": 0.522,
    "QA": 0.512,
    "QC": 0.462,
    "QE": 0.861,
    "QD": 0.903,
    "QG": 0.648,
    "QF": 0.671,
    "QI": 0.532,
    "QH": 0.765,
    "QK": 0.881,
    "QM": 0.505,
    "QL": 0.518,
    "QN": 0.181,
    "WG": 0.829,
    "WF": 0.196,
    "WE": 0.931,
    "WD": 1.0,
    "WC": 0.56,
    "WA": 0.658,
    "WN": 0.631,
    "WM": 0.344,
    "WL": 0.304,
    "WK": 0.892,
    "WI": 0.305,
    "WH": 0.678,
    "WW": 0.0,
    "WV": 0.418,
    "WT": 0.638,
    "WS": 0.689,
    "WR": 0.968,
    "WQ": 0.538,
    "WP": 0.555,
    "WY": 0.204,
    "PR": 1.0,
    "PS": 0.196,
    "PP": 0.0,
    "PQ": 0.228,
    "PV": 0.244,
    "PW": 0.72,
    "PT": 0.161,
    "PY": 0.481,
    "PC": 0.179,
    "PA": 0.22,
    "PF": 0.515,
    "PG": 0.376,
    "PD": 0.852,
    "PE": 0.831,
    "PK": 0.875,
    "PH": 0.696,
    "PI": 0.363,
    "PN": 0.231,
    "PL": 0.357,
    "PM": 0.326,
    "CK": 0.887,
    "CI": 0.304,
    "CH": 0.66,
    "CN": 0.324,
    "CM": 0.277,
    "CL": 0.301,
    "CC": 0.0,
    "CA": 0.114,
    "CG": 0.32,
    "CF": 0.437,
    "CE": 0.838,
    "CD": 0.847,
    "CY": 0.457,
    "CS": 0.176,
    "CR": 1.0,
    "CQ": 0.341,
    "CP": 0.157,
    "CW": 0.639,
    "CV": 0.167,
    "CT": 0.233,
    "IY": 0.213,
    "VA": 0.275,
    "VC": 0.165,
    "VD": 0.9,
    "VE": 0.867,
    "VF": 0.269,
    "VG": 0.471,
    "IQ": 0.383,
    "IP": 0.311,
    "IS": 0.443,
    "IR": 1.0,
    "VL": 0.134,
    "IT": 0.396,
    "IW": 0.339,
    "IV": 0.133,
    "II": 0.0,
    "IH": 0.652,
    "IK": 0.892,
    "VS": 0.322,
    "IM": 0.057,
    "IL": 0.013,
    "VV": 0.0,
    "IN": 0.457,
    "IA": 0.403,
    "VY": 0.31,
    "IC": 0.296,
    "IE": 0.891,
    "ID": 0.942,
    "IG": 0.592,
    "IF": 0.134,
    "HY": 0.821,
    "HR": 0.697,
    "HS": 0.865,
    "HP": 0.777,
    "HQ": 0.716,
    "HV": 0.831,
    "HW": 0.981,
    "HT": 0.834,
    "HK": 0.566,
    "HH": 0.0,
    "HI": 0.848,
    "HN": 0.754,
    "HL": 0.842,
    "HM": 0.825,
    "HC": 0.836,
    "HA": 0.896,
    "HF": 0.907,
    "HG": 1.0,
    "HD": 0.629,
    "HE": 0.547,
    "NH": 0.78,
    "NI": 0.615,
    "NK": 0.891,
    "NL": 0.603,
    "NM": 0.588,
    "NN": 0.0,
    "NA": 0.424,
    "NC": 0.425,
    "ND": 0.838,
    "NE": 0.835,
    "NF": 0.766,
    "NG": 0.512,
    "NY": 0.641,
    "NP": 0.266,
    "NQ": 0.175,
    "NR": 1.0,
    "NS": 0.361,
    "NT": 0.368,
    "NV": 0.503,
    "NW": 0.945,
    "TY": 0.596,
    "TV": 0.345,
    "TW": 0.816,
    "TT": 0.0,
    "TR": 1.0,
    "TS": 0.185,
    "TP": 0.159,
    "TQ": 0.322,
    "TN": 0.315,
    "TL": 0.453,
    "TM": 0.403,
    "TK": 0.866,
    "TH": 0.737,
    "TI": 0.455,
    "TF": 0.604,
    "TG": 0.312,
    "TD": 0.83,
    "TE": 0.812,
    "TC": 0.261,
    "TA": 0.251,
    "AA": 0.0,
    "AC": 0.112,
    "AE": 0.827,
    "AD": 0.819,
    "AG": 0.208,
    "AF": 0.54,
    "AI": 0.407,
    "AH": 0.696,
    "AK": 0.891,
    "AM": 0.379,
    "AL": 0.406,
    "AN": 0.318,
    "AQ": 0.372,
    "AP": 0.191,
    "AS": 0.094,
    "AR": 1.0,
    "AT": 0.22,
    "AW": 0.739,
    "AV": 0.273,
    "AY": 0.552,
    "VK": 0.889,
}

# Maximum numer of neighbours an atom can have.
# Taken from: https://www.daylight.com/meetings/mug01/Sayle/m4xbondage.html
MAX_NEIGHBOURS: Dict[str, int] = {
    "C": 4,
    "H": 1,
    "B": 3,
    "O": 2,
    "F": 1,
    "Br": 1,
    "I": 3,
}

# Covalent radii for OpenSCAD output.

# Covalent radii from Heyrovska, Raji : 'Atomic Structures of all the Twenty
# Essential Amino Acids and a Tripeptide, with Bond Lengths as Sums of Atomic
# Covalent Radii' <https://arxiv.org/pdf/0804.2488.pdf>
# Adding Ores between Osb and Odb for Asp and Glu, Nres between Nsb and Ndb
# for Arg, as PDB does not specify

COVALENT_RADII: Dict[str, float] = {
    "Csb": 0.77,
    "Cres": 0.72,
    "Cdb": 0.67,
    "Osb": 0.67,
    "Ores": 0.635,
    "Odb": 0.60,
    "Nsb": 0.70,
    "Nres": 0.66,
    "Ndb": 0.62,
    "Hsb": 0.37,
    "Ssb": 1.04,
}

# Atom classes based on Heyrovska, Raji covalent radii paper.
DEFAULT_BOND_STATE: Dict[str, str] = {
    "N": "Nsb",
    "CA": "Csb",
    "C": "Cdb",
    "O": "Odb",
    "OXT": "Osb",
    "CB": "Csb",
    "H": "Hsb",
    # Not sure about these - assuming they're all standard Hydrogen. Won't make much difference given
    # the tolerance is larger than Hs covalent radius
    "HG1": "Hsb",
    "HE": "Hsb",
    "1HH1": "Hsb",
    "1HH2": "Hsb",
    "2HH1": "Hsb",
    "2HH2": "Hsb",
    "HG": "Hsb",
    "HH": "Hsb",
    "1HD2": "Hsb",
    "2HD2": "Hsb",
    "HZ1": "Hsb",
    "HZ2": "Hsb",
    "HZ3": "Hsb",
}

RESIDUE_ATOM_BOND_STATE: Dict[str, Dict[str, str]] = {
    "XXX": {
        "N": "Nsb",
        "CA": "Csb",
        "C": "Cdb",
        "O": "Odb",
        "OXT": "Osb",
        "CB": "Csb",
        "H": "Hsb",
    },
    "VAL": {"CG1": "Csb", "CG2": "Csb"},
    "LEU": {"CG": "Csb", "CD1": "Csb", "CD2": "Csb"},
    "ILE": {"CG1": "Csb", "CG2": "Csb", "CD1": "Csb"},
    "MET": {"CG": "Csb", "SD": "Ssb", "CE": "Csb"},
    "PHE": {
        "CG": "Cdb",
        "CD1": "Cres",
        "CD2": "Cres",
        "CE1": "Cdb",
        "CE2": "Cdb",
        "CZ": "Cres",
    },
    "PRO": {"CG": "Csb", "CD": "Csb"},
    "SER": {"OG": "Osb"},
    "THR": {"OG1": "Osb", "CG2": "Csb"},
    "CYS": {"SG": "Ssb"},
    "ASN": {"CG": "Csb", "OD1": "Odb", "ND2": "Ndb"},
    "GLN": {"CG": "Csb", "CD": "Csb", "OE1": "Odb", "NE2": "Ndb"},
    "TYR": {
        "CG": "Cdb",
        "CD1": "Cres",
        "CD2": "Cres",
        "CE1": "Cdb",
        "CE2": "Cdb",
        "CZ": "Cres",
        "OH": "Osb",
    },
    "TRP": {
        "CG": "Cdb",
        "CD1": "Cdb",
        "CD2": "Cres",
        "NE1": "Nsb",
        "CE2": "Cdb",
        "CE3": "Cdb",
        "CZ2": "Cres",
        "CZ3": "Cres",
        "CH2": "Cdb",
    },
    "ASP": {"CG": "Csb", "OD1": "Ores", "OD2": "Ores"},
    "GLU": {"CG": "Csb", "CD": "Csb", "OE1": "Ores", "OE2": "Ores"},
    "HIS": {
        "CG": "Cdb",
        "CD2": "Cdb",
        "ND1": "Nsb",
        "CE1": "Cdb",
        "NE2": "Ndb",
    },
    "LYS": {"CG": "Csb", "CD": "Csb", "CE": "Csb", "NZ": "Nsb"},
    "ARG": {
        "CG": "Csb",
        "CD": "Csb",
        "NE": "Nsb",
        "CZ": "Cdb",
        "NH1": "Nres",
        "NH2": "Nres",
    },
}

# Contains idealised single, double and triple bond lengths (i_s, i_d, i_t) and watersheds (w_sd, w_dt),
# below which a bond is probably double/triple (e.g. triple < double < single)
# Taken from: Automatic Assignment of Chemical Connectivity to Organic Molecules in the Cambridge Structural Database
# Jon C. Baber and Edward E. Hodgkin*
# J. Chem. Inf. Comput. Sci. 1992, 32. 401-406
BOND_LENGTHS: Dict[str, Dict[str, float]] = {
    "As-N": {"i_s": 1.86, "i_d": 1.835, "w_sd": 1.845},
    "As-O": {"i_s": 1.71, "i_d": 1.66, "w_sd": 1.68},
    "As-S": {"i_s": 2.28, "i_d": 2.08, "w_sd": 2.15},
    "C-C": {
        "i_s": 1.49,
        "i_d": 1.31,
        "i_t": 1.18,
        "w_sd": 1.38,
        "w_dt": 1.21,
    },
    "C-N": {"i_s": 1.42, "i_d": 1.32, "i_t": 1.14, "w_sd": 1.34, "w_dt": 1.20},
    "C-O": {
        "i_s": 1.41,
        "i_d": 1.22,
        "w_sd": 1.28,
    },
    "C-S": {
        "i_s": 1.78,
        "i_d": 1.68,
        "w_sd": 1.70,
    },
    "C-Te": {
        "i_s": 2.20,
        "i_d": 1.80,
        "w_sd": 2.10,
    },
    "N-N": {
        "i_s": 1.40,
        "i_d": 1.22,
        "w_sd": 1.32,
    },
    "N-O": {
        "i_s": 1.39,
        "i_d": 1.22,
        "w_sd": 1.25,
    },
    "N-P": {
        "i_s": 1.69,
        "i_d": 1.59,
        "w_sd": 1.62,
    },
    "N-S": {
        "i_s": 1.66,
        "i_d": 1.54,
        "w_sd": 1.58,
    },
    "N-Se": {
        "i_s": 1.83,
        "i_d": 1.79,
        "w_sd": 1.80,
    },
    "O-P": {
        "i_s": 1.60,
        "i_d": 1.48,
        "w_sd": 1.52,
    },
    "O-S": {
        "i_s": 1.58,
        "i_d": 1.45,
        "w_sd": 1.54,
    },
    "P-P": {
        "i_s": 2.23,
        "i_d": 2.04,
        "w_sd": 2.06,
    },
}

BOND_ORDERS: Dict = {
    "As-N": [1, 2],
    "As-O": [1, 2],
    "As-S": [1, 2],
    "C-C": [1, 2, 3],
    "C-N": [1, 2, 3],
    "C-O": [1, 2],
    "C-S": [1, 2],
    "C-Te": [1, 2],
    "N-N": [1, 2],
    "N-O": [1, 2],
    "N-P": [1, 2],
    "N-S": [1, 2],
    "N-Se": [1, 2],
    "O-P": [1, 2],
    "O-S": [1, 2],
    "P-P": [1, 2],
}
