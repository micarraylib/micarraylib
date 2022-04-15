from micarraylib.datasets import starss2022_loader
from micarraylib.arraycoords.array_shapes_utils import _polar2cart
import numpy as np
import soundata
import pytest
import librosa


def test_starss2022_init():

    a = starss2022_loader.starss2022(download=False, data_home="~/")
    assert a.name == "starss2022"
    assert a.fs == 24000
    assert len(a.array_format) == 1
    assert a.array_format["Eigenmike"] == "A"
    assert len(a.capsule_coords["Eigenmike"]) == 4
    assert list(a.capsule_coords["Eigenmike"].keys()) == ["6", "10", "22", "26"]
    b = _polar2cart(a.capsule_coords["Eigenmike"], "radians")
    # TODO: analize why the atol is needed
    assert np.allclose(
        np.mean(np.array([c for c in b.values()]), axis=0), [0, 0, 0], atol=1e-4
    )
    assert (
        len(a.micarray_clip_ids["Eigenmike"])
        == len(soundata.initialize("starss2022", data_home="~/").clip_ids) / 2
    )  # because soundata has clip_ids for each format A and B
    assert (
        len(a.clips_list)
        == len(soundata.initialize("starss2022", data_home="~/").clip_ids) / 2
    )  # because soundata has clip_ids for each format A and B


def test_starss2022_get_audio_numpy():

    a = starss2022_loader.starss2022(
        download=False, data_home="tests/resources/datasets/starss2022"
    )
    A = a.get_audio_numpy("dev/dev-train-sony/fold3_room21_mix001")
    B = a.get_audio_numpy("dev/dev-train-sony/fold3_room21_mix001", fmt="B")

    Al = librosa.load(
        "tests/resources/datasets/starss2022/mic_dev/dev-train-sony/fold3_room21_mix001.wav",
        sr=24000,
        mono=False,
    )[0]
    Bl = librosa.load(
        "tests/resources/datasets/starss2022/foa_dev/dev-train-sony/fold3_room21_mix001.wav",
        sr=24000,
        mono=False,
    )[0]

    assert (B == Bl).all()
    assert (A == Al).all()

    with pytest.raises(ValueError):
        a.get_audio_numpy("a", "b")
    with pytest.raises(ValueError):
        a.get_audio_numpy("a", "Eigenmike")


def test_starss2022_get_audio_events():

    a = starss2022_loader.starss2022(
        download=False, data_home="tests/resources/datasets/starss2022"
    )
    A = a.get_audio_events("dev/dev-train-sony/fold3_room21_mix001")

    with pytest.raises(ValueError):
        a.get_audio_events("a")
