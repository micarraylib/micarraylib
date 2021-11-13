from micarraylib.datasets import tau2020sse_nigens_loader
from micarraylib.arraycoords.array_shapes_utils import _polar2cart
import numpy as np
import soundata
import pytest
import librosa




def test_tau2020sse_nigens_init():

    a = tau2020sse_nigens_loader.tau2020sse_nigens(download=False,data_home='~/')
    assert a.name == "tau2020sse_nigens"
    assert a.fs == 24000
    assert len(a.array_format) == 1
    assert a.array_format['Eigenmike'] == 'A'
    assert len(a.capsule_coords['Eigenmike']) == 4
    assert list(a.capsule_coords['Eigenmike'].keys()) == ['6','10','22','26']
    b = _polar2cart(a.capsule_coords['Eigenmike'],'radians')
    # TODO: analize why the atol is needed
    assert np.allclose(np.mean(np.array([c for c in b.values()]),axis=0),[0,0,0],atol=1.5e-2)
    assert len(a.micarray_clip_ids['Eigenmike']) == len(soundata.initialize('tau2020sse_nigens',data_home='~/').clip_ids)/2 # because soundata has clip_ids for each format A and B
    assert len(a.clips_list) == len(soundata.initialize('tau2020sse_nigens',data_home='~/').clip_ids)/2 # because soundata has clip_ids for each format A and B




def test_tau2020sse_nigens_get_audio_numpy():

    a = tau2020sse_nigens_loader.tau2020sse_nigens(download=False,data_home='tests/resources/datasets/tau2020sse_nigens')
    A = a.get_audio_numpy('dev/fold1_room1_mix001_ov1')
    B = a.get_audio_numpy('dev/fold1_room1_mix001_ov1',fmt='B')

    Al = librosa.load('tests/resources/datasets/tau2020sse_nigens/mic_dev/fold1_room1_mix001_ov1.wav',sr=24000,mono=False)[0]
    Bl = librosa.load('tests/resources/datasets/tau2020sse_nigens/foa_dev/fold1_room1_mix001_ov1.wav',sr=24000,mono=False)[0]
    
    assert (B==Bl).all()
    assert (A==Al).all()

    with pytest.raises(ValueError):
        a.get_audio_numpy('a','b')
    with pytest.raises(ValueError):
        a.get_audio_numpy('a','Eigenmike')




def test_tau2020sse_nigens_get_audio_events():

    a = tau2020sse_nigens_loader.tau2020sse_nigens(download=False,data_home='tests/resources/datasets/tau2020sse_nigens')
    A = a.get_audio_events('dev/fold1_room1_mix001_ov1')

    with pytest.raises(ValueError):
        a.get_audio_events('a')
