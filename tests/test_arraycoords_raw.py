from micarraylib.arraycoords import array_shapes_raw
import numpy as np




def test_ambeovr_values():

    coords = array_shapes_raw.ambeovr_raw
    assert all([v[0]<=180 and v[0]>=0 for v in coords.values()])
    assert all([np.abs(v[1])<=180 for v in coords.values()])
    assert all([v[2]>=0 for v in coords.values()])




def test_eigenmike_values():

    coords = array_shapes_raw.eigenmike_raw
    assert all([v[0]<=180 and v[0]>=0 for v in coords.values()])
    assert all([v[1]<=360 for v in coords.values()])
    assert all([v[2]>=0 for v in coords.values()])




def test_oct3d_values():

    coords = array_shapes_raw.oct3d_raw
    assert all([v[0]>=0 if k[0]=='F' else v[0]<=0 for k,v in coords.items()])
    assert all([v[1]>=0 if k[1]=='L' else v[1]<=0 for k,v in coords.items()])
    assert all([v[2]>=0 if k[-1]=='h' else v[2]<=0 for k,v in coords.items()])




def test_pcma3d_values():

    coords = array_shapes_raw.pcma3d_raw
    assert all([v[0]>=0 if k[0]=='F' else v[0]<=0 for k,v in coords.items()])
    assert all([v[1]>=0 if k[1]=='L' else v[1]<=0 for k,v in coords.items()])
    assert all([v[2]>=0 if k[-1]=='h' else v[2]<=0 for k,v in coords.items()])




def test_cube2l_values():

    coords = array_shapes_raw.cube2l_raw
    assert all([v[0]>=0 if k[0]=='F' else v[0]<=0 for k,v in coords.items()])
    assert all([v[1]>=0 if k[1]=='L' else v[1]<=0 for k,v in coords.items()])
    assert all([v[2]>=0 if k[-1]=='h' else v[2]<=0 for k,v in coords.items()])




def test_deccacuboid_values():

    coords = array_shapes_raw.deccacuboid_raw
    assert all([v[0]>=0 if k[0]=='F' else v[0]<=0 for k,v in coords.items()])
    assert all([v[1]>=0 if k[1]=='L' else v[1]<=0 for k,v in coords.items()])
    assert all([v[2]>=0 if k[-1]=='h' else v[2]<=0 for k,v in coords.items()])




def test_hamasaki_values():

    coords = array_shapes_raw.hamasaki_raw
    assert all([v[0]>=0 if k[0]=='F' else v[0]<=0 for k,v in coords.items()])
    assert all([v[1]>=0 if k[1]=='L' else v[1]<=0 for k,v in coords.items()])
    assert all([v[2]>=1.0 if 'h' in k and k[-1]=='1' else v[2]<=1.6 for k,v in coords.items()])
