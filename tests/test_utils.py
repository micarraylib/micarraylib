from micarraylib.utils import a2b, _get_audio_numpy
from micarraylib.datasets import marco
from spaudiopy import sph
import numpy as np
import pytest
import os
import librosa
import warnings




def test_a2b():
    SH = sph.sh_matrix(5, [np.pi / 4, 7 * np.pi / 4], [np.pi / 3, np.pi- np.pi / 3],'real')
    Y = np.linalg.pinv(SH)
    b = np.dot(Y, np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
    a = a2b(
        5,
        np.array([[1, 2, 3], [4, 5, 6]]),
        {"a": [np.pi / 3, np.pi / 4, 1], "b": [2 * np.pi / 3, -np.pi / 4, 1]},
    )

    assert np.allclose(a, b)




def test_get_audio_numpy_valueerrors():

    a = marco(download=False,data_home='tests/resources/datasets/marco') 

    with pytest.raises(ValueError):
        _get_audio_numpy('a',a.dataset,'foo','A')
    with pytest.raises(ValueError):
        _get_audio_numpy('a',a.dataset,'A','foo')
    with pytest.raises(ValueError):
        _get_audio_numpy('a',a.dataset,'foo1','foo2')

    with pytest.raises(ValueError):
        _get_audio_numpy('a',a.dataset,'B','A')

    with pytest.raises(ValueError):
        _get_audio_numpy(['a','b','c','d'],a.dataset,'A','B',{'a':[0,0,0]},1000)

    with pytest.raises(ValueError):
        _get_audio_numpy('a',a.dataset,'A','B')

    with pytest.warns(UserWarning):
        a = marco(download=False,data_home='tests/resources/datasets/marco') 
        A = _get_audio_numpy(a.micarray_capsule_clip_ids['OCT3D']['impulse_response+90d'],a.dataset,'B','B',N=1,fs=48000)




def test_get_audio_numpy_resample():
    data_dir = 'tests/resources/datasets/marco'
    a = marco(download=False,data_home=data_dir) 
    A = _get_audio_numpy(a.micarray_capsule_clip_ids['OCT3D']['impulse_response+90d'],a.dataset,'A','A',fs=24000)
    wavs_dir = os.path.join(data_dir,'3D-MARCo Impulse Responses/01_Speaker_+90deg_3m')
    wavs = os.listdir(wavs_dir)
    wavs.sort()
    B = np.array([librosa.load(os.path.join(wavs_dir,w),24000,mono=False)[0] for w in wavs])
    assert np.allclose(A,B,atol=1e-6)




def test_get_audio_numpy_a2b():
    data_dir = 'tests/resources/datasets/marco'
    a = marco(download=False,data_home=data_dir) 
    A = _get_audio_numpy(a.micarray_capsule_clip_ids['OCT3D']['impulse_response+90d'],a.dataset,'A','B',a.capsule_coords['OCT3D'],fs=48000)
    wavs_dir = os.path.join(data_dir,'3D-MARCo Impulse Responses/01_Speaker_+90deg_3m')
    wavs = os.listdir(wavs_dir)
    wavs.sort()
    B = np.array([librosa.load(os.path.join(wavs_dir,w),sr=48000,mono=False)[0] for w in wavs])
    B = a2b(2,B,a.capsule_coords['OCT3D'])
    assert np.allclose(A,B)

