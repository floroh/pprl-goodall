ATTRIBUTE_ORDER = [
    "FIRSTNAME",
    "MIDDLENAME",
    "LASTNAME",
    "CITY",
    "ZIP",
    "YEAROFBIRTH",
    "PLACEOFBIRTH",
    "COUNTRY",
    "SEX",
    "STREET",
]

ATTRIBUTE_SHORT = {
    "FIRSTNAME": "FN",
    "MIDDLENAME": "MN",
    "LASTNAME": "LN",
    "CITY": "CI",
    "ZIP": "ZIP",
    "YEAROFBIRTH": "YOB",
    "PLACEOFBIRTH": "POB",
    "DATEOFBIRTH": "DOB",
    "SEX": "SEX"
}

ATTRIBUTES_FOR_DISPLAY = [
    "FIRSTNAME",
    "MIDDLENAME",
    "LASTNAME",
    "CITY",
    "ZIP",
    "YEAROFBIRTH",
    "PLACEOFBIRTH",
]

ATTRIBUTE_REPLACEMENTS = {
    "PLZ": "ZIP",
    "plz": "ZIP",
    "GENDER": "SEX",
    "gender": "SEX",
}

DATASET_NAME_MAPPING = {
    "_yob1900": "NC-Yob00",
    "_yob1950": "NC-Yob50",
    "_yob1980": "NC-Yob80",
    "_female": "NC-Fe",
    "_male": "NC-Ma",
    "_min1E": "NC-min1E",
    "_min2E": "NC-min2E",
    "NCVR_TIME": "NC-T",
    "NCVR_DIRTY": "NC-D",
    "NCVR_FRQ": "NC-F",
    " TEST": "GER-t",
    " TIME": "GER-T",
    " DIRTY": "GER-D",
    " DIRTY_FRQ": "GER-F",
    " FRQ": "GER-F",
    "BaWue_TIME": "BW-T",
    "BaWue_DIRTY": "BW-D",
    "BaWue_FRQ": "BW-F",
    "BaWue_DIRTY_FRQ": "BW-F",
}

DATASET_ORDER = [
    "GER-T",
    "GER-D",
    "GER-F",
    "BW-T",
    "BW-D",
    "BW-F",
    "NC-T",
    "NC-D",
    "NC-F",
    "NC-min1E",
    "NC-min2E",
    "NC-Ma",
    "NC-Fe",
    "NC-Yob00",
    "NC-Yob50",
    "NC-Yob80",
]

DATASET_MOD_ORDER = [
    "T",
    "D",
    "F",
    "min1E",
    "min2E",
    "Ma",
    "Fe",
    "Yob00",
    "Yob50",
    "Yob80",
]

WEIGHT_SET_ORDER = [
    "Equal",
    "Core",
    "Core+"
    "FS"
]