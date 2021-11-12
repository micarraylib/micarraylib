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

array_objects = {
    "Ambeo": micarray(array_shapes_raw.ambeovr_raw, "polar", "degrees", "Ambeo"),
    "Eigenmike": micarray(
        array_shapes_raw.eigenmike_raw, "polar", "degrees", "Eigenmike"
    ),
    "OCT3D": micarray(array_shapes_raw.oct3d_raw, "cartesian", None, "OCT3D"),
    "PCMA3D": micarray(array_shapes_raw.pcma3d_raw, "cartesian", None, "PCMA3D"),
    "2LCube": micarray(array_shapes_raw.cube2l_raw, "cartesian", None, "2LCube"),
    "DeccaCuboid": micarray(
        array_shapes_raw.deccacuboid_raw, "cartesian", None, "DeccaCuboid"
    ),
    "Hamasaki": micarray(array_shapes_raw.hamasaki_raw, "cartesian", None, "Hamasaki"),
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
