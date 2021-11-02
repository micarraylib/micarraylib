from .array_shapes_utils import micarray
from . import array_shapes_raw

ARRAYNAMES = [
    "Ambeo",
    "Eigenmike",
    "OCT3D",
    "PCMA3D",
    "2LCube",
    "DeccaCuboid",
    "Hamasaki",
]

array_objects = {
    "Ambeo": micarray(array_shapes_raw.ambeovr_raw, 'polar', 'degrees', "Ambeo"),
    "Eigenmike": micarray(array_shapes_raw.eigenmike_raw, 'polar', 'degrees', "Eigenmike"),
    "OCT3D": micarray(array_shapes_raw.oct3d_raw, 'cartesian', None, "OCT3D"),
    "PCMA3D": micarray(array_shapes_raw.pcma3d_raw, 'cartesian', None, "PCMA3D"),
    "2LCube": micarray(array_shapes_raw.cube2l_raw, 'cartesian', None, "2LCube"),
    "DeccaCuboid": micarray(array_shapes_raw.deccacuboid_raw, 'cartesian', None, "DeccaCuboid"),
    "Hamasaki": micarray(array_shapes_raw.hamasaki_raw, 'cartesian', None, "Hamasaki"),
}

def list_micarrays():
    """
    Get a list of microphone array
    topologies supported 
    """
    return ARRAYNAMES


def get_array(array_name):
    """
    Get the object associated with a
    microphone array shape
    """
    if array_name not in ARRAYNAMES:
        raise ValueError("Not a supported microphone array")
    return array_objects[array_name]

# dictionary of array capsules names 
# for each microphone array
arraycapsules = {
    "Ambeo": [
        "Ch1:FLU",
        "Ch2:FRD",
        "Ch3:BLD",
        "Ch4:BRU",
    ],
    "Eigenmike": [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
        "32",
    ],
    "OCT3D": [
        "FL",
        "FR",
        "FC",
        "RL",
        "RR",
        "FLh",
        "FRh",
        "RLh",
        "RRh",
    ],
    "PCMA3D": [
        "FL",
        "FR",
        "FC",
        "RL",
        "RR",
        "FLh",
        "FRh",
        "RLh",
        "RRh",
    ],
    "2LCube": [
        "FL",
        "FR",
        "FC",
        "RL",
        "RR",
        "FLh",
        "FRh",
        "RLh",
        "RRh",
    ],
    "DeccaCuboid": [
        "FL",
        "FR",
        "FC",
        "RL",
        "RR",
        "FLh",
        "FRh",
        "RLh",
        "RRh",
    ],
    "Hamasaki": [
        "FL",
        "FR",
        "RL",
        "RR",
        "FLh_0",
        "FRh_0",
        "RLh_0",
        "RRh_0",
        "FLh_1",
        "FRh_1",
        "RLh_1",
        "RRh_1",
    ]
}

