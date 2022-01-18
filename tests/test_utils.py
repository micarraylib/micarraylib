from micarraylib.utils import a2b, _get_audio_numpy
from micarraylib.datasets import marco
from spaudiopy import sph
import numpy as np
import pytest
import os
import librosa
import warnings


def test_a2b():
    SH = sph.sh_matrix(
        5, [np.pi / 4, 7 * np.pi / 4], [np.pi / 3, np.pi - np.pi / 3], "real"
    )
    Y = np.linalg.pinv(SH)
    b = np.dot(Y, np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
    a = a2b(
        5,
        np.array([[1, 2, 3], [4, 5, 6]]),
        {"a": [np.pi / 3, np.pi / 4, 1], "b": [2 * np.pi / 3, -np.pi / 4, 1]},
    )

    assert np.allclose(a, b)


def test_get_audio_numpy_valueerrors():

    a = marco(download=False, data_home="tests/resources/datasets/marco")

    with pytest.raises(ValueError):
        _get_audio_numpy("a", a.dataset, "foo", "A")
    with pytest.raises(ValueError):
        _get_audio_numpy("a", a.dataset, "A", "foo")
    with pytest.raises(ValueError):
        _get_audio_numpy("a", a.dataset, "foo1", "foo2")

    with pytest.raises(ValueError):
        _get_audio_numpy("a", a.dataset, "B", "A")

    with pytest.raises(ValueError):
        _get_audio_numpy(
            a.micarray_capsule_clip_ids["OCT3D"]["impulse_response+90d"], a.dataset, "A", "B", {"a": [0, 0, 0]}, 1000
        )

    with pytest.raises(ValueError):
        _get_audio_numpy("a", a.dataset, "A", "B")

    with pytest.warns(UserWarning):
        a = marco(download=False, data_home="tests/resources/datasets/marco")
        A = _get_audio_numpy(
            a.micarray_capsule_clip_ids["OCT3D"]["impulse_response+90d"],
            a.dataset,
            "B",
            "B",
            N=1,
            fs=48000,
        )


def test_get_audio_numpy_resample():
    data_dir = "tests/resources/datasets/marco"
    a = marco(download=False, data_home=data_dir)
    A = _get_audio_numpy(
        a.micarray_capsule_clip_ids["OCT3D"]["impulse_response+90d"],
        a.dataset,
        "A",
        "A",
        fs=24000,
    )
    wavs_dir = os.path.join(data_dir, "3D-MARCo Impulse Responses/01_Speaker_+90deg_3m")
    wavs = [wavs_dir+"/+90deg_010_OCT3D_1_FL.wav",wavs_dir+"/+90deg_011_OCT3D_2_FR.wav",
    wavs_dir+"/+90deg_012_OCT3D_3_FC.wav",wavs_dir+"/+90deg_013_OCT3D_4_RL.wav",
    wavs_dir+"/+90deg_014_OCT3D_5_RR.wav",wavs_dir+"/+90deg_015_OCT3D_6_FLh_1m.wav",
    wavs_dir+"/+90deg_016_OCT3D_7_FRh_1m.wav",wavs_dir+"/+90deg_017_OCT3D_8_RLh_1m.wav",
    wavs_dir+"/+90deg_018_OCT3D_9_RRh_1m.wav"]
    wavs.sort()
    B = np.array(
        [librosa.load(w, 24000, mono=False)[0] for w in wavs]
    )
    assert np.allclose(A, B, atol=1e-4)


def test_get_audio_numpy_a2b():
    data_dir = "tests/resources/datasets/marco"
    a = marco(download=False, data_home=data_dir)
    A = _get_audio_numpy(
        a.micarray_capsule_clip_ids["OCT3D"]["impulse_response+90d"],
        a.dataset,
        "A",
        "B",
        a.capsule_coords["OCT3D"],
        fs=48000,
    )
    wavs_dir = os.path.join(data_dir, "3D-MARCo Impulse Responses/01_Speaker_+90deg_3m")
    wavs = [wavs_dir+"/+90deg_010_OCT3D_1_FL.wav",wavs_dir+"/+90deg_011_OCT3D_2_FR.wav",
    wavs_dir+"/+90deg_012_OCT3D_3_FC.wav",wavs_dir+"/+90deg_013_OCT3D_4_RL.wav",
    wavs_dir+"/+90deg_014_OCT3D_5_RR.wav",wavs_dir+"/+90deg_015_OCT3D_6_FLh_1m.wav",
    wavs_dir+"/+90deg_016_OCT3D_7_FRh_1m.wav",wavs_dir+"/+90deg_017_OCT3D_8_RLh_1m.wav",
    wavs_dir+"/+90deg_018_OCT3D_9_RRh_1m.wav"]

    wavs.sort()
    
    B = np.array(
        [librosa.load(w, sr=48000, mono=False)[0] for w in wavs]
    )

    B = a2b(2, B, a.capsule_coords["OCT3D"])
    assert np.allclose(A, B)

    A = _get_audio_numpy(
        a.micarray_capsule_clip_ids["Eigenmike"]["impulse_response+90d"],
        a.dataset,
        "A",
        "B",
        a.capsule_coords["Eigenmike"],
        N=2,
        fs=48000,   
    )
    
    B = librosa.load(wavs_dir+"/+90deg_065_Eigenmike_Raw_32ch.wav", sr=48000, mono=False)[0]

    B = a2b(2, B, a.capsule_coords["Eigenmike"])

    print("Shape of A: ", A.shape)
    print("Shape of B: ", B.shape)

    assert np.allclose(A, B)
