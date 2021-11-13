from micarraylib.datasets import eigenscape_loader
import numpy as np
import soundata
import pytest
import librosa


def test_eigenscape_init():

    a = eigenscape_loader.eigenscape(download=False, data_home="~/")
    assert a.name == "eigenscape"
    assert a.fs == 48000
    assert len(a.array_format) == 1
    assert a.array_format["Eigenmike"] == "B"
    assert len(a.capsule_coords["Eigenmike"]) == 32
    assert len(a.micarray_clip_ids["Eigenmike"]) == len(
        soundata.initialize("eigenscape", data_home="~/").clip_ids
    )
    assert len(a.clips_list) == len(
        soundata.initialize("eigenscape", data_home="~/").clip_ids
    )


def test_eigenscape_get_audio_numpy():

    a = eigenscape_loader.eigenscape(
        download=False, data_home="tests/resources/datasets/eigenscape"
    )
    A = a.get_audio_numpy("Beach.1")

    Al = librosa.load(
        "tests/resources/datasets/eigenscape/Beach.1.wav", sr=48000, mono=False
    )[0]

    assert (A == Al).all()

    with pytest.raises(ValueError):
        a.get_audio_numpy("a", fmt="A")
    with pytest.raises(ValueError):
        a.get_audio_numpy("a", "Eigenfoo")
    with pytest.raises(ValueError):
        a.get_audio_numpy("a")


def test_eigenscape_raw_init():

    a = eigenscape_loader.eigenscape_raw(download=False, data_home="~/")
    assert a.name == "eigenscape_raw"
    assert a.fs == 48000
    assert len(a.array_format) == 1
    assert a.array_format["Eigenmike"] == "A"
    assert len(a.capsule_coords["Eigenmike"]) == 32
    assert len(a.micarray_clip_ids["Eigenmike"]) == len(
        soundata.initialize("eigenscape", data_home="~/").clip_ids
    )
    assert len(a.clips_list) == len(
        soundata.initialize("eigenscape", data_home="~/").clip_ids
    )


def test_eigenscape_raw_get_audio_numpy():

    a = eigenscape_loader.eigenscape_raw(
        download=False, data_home="tests/resources/datasets/eigenscape_raw"
    )
    A = a.get_audio_numpy("Beach-01-Raw")

    Al = librosa.load(
        "tests/resources/datasets/eigenscape_raw/Beach-01-Raw.wav", sr=48000, mono=False
    )[0]

    assert (A == Al).all()

    with pytest.raises(ValueError):
        a.get_audio_numpy("a", fmt="B")
    with pytest.raises(ValueError):
        a.get_audio_numpy("a", "Eigenfoo")
    with pytest.raises(ValueError):
        a.get_audio_numpy("a")
