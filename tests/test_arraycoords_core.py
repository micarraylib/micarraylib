from micarraylib.arraycoords.core import micarray
from micarraylib.arraycoords import array_shapes_raw
from micarraylib.arraycoords.array_shapes_utils import _polar2cart
import pytest
import numpy as np


def test_micarray_init():

    arr = micarray(array_shapes_raw.cube2l_raw, "cartesian", None, "foo")
    assert arr.name == "foo"
    assert arr.capsule_names == list(array_shapes_raw.cube2l_raw.keys())
    assert arr.coords_dict == array_shapes_raw.cube2l_raw
    assert arr.coords_form == "cartesian"
    assert arr.angle_units == None

    # no coordinates form
    with pytest.raises(ValueError):
        micarray(array_shapes_raw.ambeovr_raw)
    # cartesian with angle units
    with pytest.raises(ValueError):
        micarray(array_shapes_raw.cube2l_raw, "cartesian", "degree")


def test_micarray_center_coords():

    arr = micarray(array_shapes_raw.cube2l_raw, "cartesian")
    arr.center_coords()
    assert np.allclose(
        np.mean(np.array([c for c in arr.coords_dict.values()]), axis=0), [0, 0, 0]
    )

    arr = micarray(array_shapes_raw.ambeovr_raw, "polar", "degrees")
    arr.center_coords()
    assert np.allclose(
        np.mean(np.array([c for c in arr.coords_dict.values()]), axis=0), [0, 0, 0]
    )
    assert arr.coords_form == "cartesian"
    assert arr.angle_units == None


def test_micarray_standard_coords():

    arr = micarray(array_shapes_raw.eigenmike_raw, "polar", "degrees")
    arr.standard_coords("cartesian")
    assert np.allclose(
        np.mean(np.array([c for c in arr.coords_dict.values()]), axis=0), [0, 0, 0]
    )
    arr.standard_coords("polar")
    assert arr.coords_form == "polar"
    assert arr.angle_units == "radians"

    # sanity check on range of angles in polar coordinates
    assert all([c[0] > 0 and c[0] < 180 for c in arr.coords_dict.values()])
    assert all([c[1] <= 180 and c[1] >= -180 for c in arr.coords_dict.values()])

    # returning to cartesian should result in coordinates centered around zero
    coords_cart = _polar2cart(arr.coords_dict, "radians")
    # TODO: investigate why this error tolerance is needed, correct, and remove
    assert np.allclose(
        np.mean(np.array([v for v in coords_cart.values()]), axis=0),
        [0, 0, 0],
        atol=1e-2,
    )

    # value when form not specified
    with pytest.raises(ValueError):
        arr.standard_coords()
