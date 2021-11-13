from micarraylib.datasets import marco_loader
import numpy as np
import soundata
import pytest
import librosa


def test_marco_init():

    a = marco_loader.marco(download=False, data_home="~/")
    assert a.name == "marco"
    assert a.fs == 48000
    assert len(a.array_format) == 7
    assert all([fmt == "A" for fmt in a.array_format.values()])
    assert len(a.capsule_coords["OCT3D"]) == 9
    assert len(a.capsule_coords["Eigenmike"]) == 32
    assert len(a.capsule_coords["PCMA3D"]) == 9
    assert len(a.capsule_coords["DeccaCuboid"]) == 9
    assert len(a.capsule_coords["2LCube"]) == 9
    assert len(a.capsule_coords["Ambeo"]) == 4
    assert len(a.capsule_coords["Hamasaki"]) == 12


def test_marco_get_audio_numpy():

    a = marco_loader.marco(download=False, data_home="tests/resources/datasets/marco")
    A = a.get_audio_numpy("impulse_response+90d", "OCT3D")

    with pytest.raises(ValueError):
        a.get_audio_numpy("a", "Eigenfoo")
    with pytest.raises(ValueError):
        a.get_audio_numpy("a", "Eigenmike")
