from micarraylib import arraycoords
import pytest


def test_list_micarrays():

    ARRAYNAMES = [
        "Ambeo",
        "Eigenmike",
        "OCT3D",
        "PCMA3D",
        "2LCube",
        "DeccaCuboid",
        "Hamasaki",
    ]

    assert ARRAYNAMES == arraycoords.list_micarrays()


def test_get_array():

    ARRAYNAMES = [
        "Ambeo",
        "Eigenmike",
        "OCT3D",
        "PCMA3D",
        "2LCube",
        "DeccaCuboid",
        "Hamasaki",
    ]

    [arraycoords.get_array(arr) for arr in ARRAYNAMES]

    with pytest.raises(ValueError):
        arraycoords.get_array("foo")
