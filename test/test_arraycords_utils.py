from micarraylib.arraycoords.array_shapes_utils import _deg2rad
from micarraylib.arraycoords.array_shapes_utils import _polar2cart
from micarraylib import arraycoords
import math
import numpy as np
import pytest




def test_deg2rad():
    # TODO add more items to dictionary in addition to 'a'
    coords_dict_deg = {'a':[150,45,9]}
    coords_dict_rad = {'a':[150*(math.pi/180),45*(math.pi/180),9]}

    assert all([np.allclose(coords_dict_rad[k],_deg2rad(coords_dict_deg)[k]) for k in coords_dict_deg.keys()])




def test_polar2cart():
    piover180 = math.pi/180
    # TODO add more items to dictionary in addition to 'a'
    coords_dict_deg = {'a':[150,45,9]}
    coords_dict_rad = _deg2rad(coords_dict_deg)
    coords_dict_cart = {'a':
        [
            9*math.sin(150*piover180)*math.cos(45*piover180),
            9*math.sin(150*piover180)*math.sin(45*piover180),
            9*math.cos(150*piover180),
        ]
    }

    assert all([np.allclose(coords_dict_cart[k],_polar2cart(coords_dict_deg,'degrees')[k]) for k in coords_dict_cart.keys()])
    assert all([np.allclose(coords_dict_cart[k],_polar2cart(coords_dict_rad,'radians')[k]) for k in coords_dict_cart.keys()])
    
    # test the expected directions
    assert _polar2cart(coords_dict_rad,'radians')['a'][0]>0
    assert _polar2cart(coords_dict_rad,'radians')['a'][1]>0
    assert _polar2cart(coords_dict_rad,'radians')['a'][2]<0

    # also test value errors
    with pytest.raises(ValueError):
        _polar2cart(coords_dict_deg)
    with pytest.raises(ValueError):
        _polar2cart(coords_dict_deg,'foo')
