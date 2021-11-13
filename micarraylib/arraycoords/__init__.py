from .core import micarray
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
    if array_name == "Ambeo": 
        return micarray(array_shapes_raw.ambeovr_raw, "polar", "degrees", "Ambeo")
    elif array_name == "Eigenmike":
        return micarray(
            array_shapes_raw.eigenmike_raw, "polar", "degrees", "Eigenmike"
        )
    elif array_name == "OCT3D": 
        return micarray(array_shapes_raw.oct3d_raw, "cartesian", None, "OCT3D")
    elif array_name == "PCMA3D": 
        return micarray(array_shapes_raw.pcma3d_raw, "cartesian", None, "PCMA3D")
    elif array_name == "2LCube": 
        return micarray(array_shapes_raw.cube2l_raw, "cartesian", None, "2LCube")
    elif array_name == "DeccaCuboid": 
        return micarray(
            array_shapes_raw.deccacuboid_raw, "cartesian", None, "DeccaCuboid"
        )
    elif array_name == "Hamasaki": 
        return micarray(array_shapes_raw.hamasaki_raw, "cartesian", None, "Hamasaki")
