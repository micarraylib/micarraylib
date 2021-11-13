from micarraylib.datasets import tau2019sse_loader
from micarraylib.arraycoords.array_shapes_utils import _polar2cart
import numpy as np
import soundata
import pytest
import librosa


def test_tau2019sse_init():

    a = tau2019sse_loader.tau2019sse(download=False, data_home="~/")
    assert a.name == "tau2019sse"
    assert a.fs == 24000
    assert len(a.array_format) == 1
    assert a.array_format["Eigenmike"] == "A"
    assert len(a.capsule_coords["Eigenmike"]) == 4
    assert list(a.capsule_coords["Eigenmike"].keys()) == ["6", "10", "22", "26"]
    b = _polar2cart(a.capsule_coords["Eigenmike"], "radians")
    assert np.allclose(
        np.mean(np.array([c for c in b.values()]), axis=0), [0, 0, 0], atol=1e-4
    )
    assert (
        len(a.micarray_clip_ids["Eigenmike"])
        == len(soundata.initialize("tau2019sse", data_home="~/").clip_ids) / 2
    )  # because soundata has clip_ids for each format A and B
    assert (
        len(a.clips_list)
        == len(soundata.initialize("tau2019sse", data_home="~/").clip_ids) / 2
    )  # because soundata has clip_ids for each format A and B


def test_tau2019sse_get_audio_numpy():

    a = tau2019sse_loader.tau2019sse(
        download=False, data_home="tests/resources/datasets/tau2019sse"
    )
    A = a.get_audio_numpy("dev/split1_ir0_ov1_1")
    B = a.get_audio_numpy("dev/split1_ir0_ov1_1", fmt="B")

    Al = librosa.load(
        "tests/resources/datasets/tau2019sse/mic_dev/split1_ir0_ov1_1.wav",
        sr=24000,
        mono=False,
    )[0]
    Bl = librosa.load(
        "tests/resources/datasets/tau2019sse/foa_dev/split1_ir0_ov1_1.wav",
        sr=24000,
        mono=False,
    )[0]

    assert (B == Bl).all()
    assert (A == Al).all()

    with pytest.raises(ValueError):
        a.get_audio_numpy("a", "b")
    with pytest.raises(ValueError):
        a.get_audio_numpy("a", "Eigenmike")


def test_tau2019sse_get_audio_events():

    a = tau2019sse_loader.tau2019sse(
        download=False, data_home="tests/resources/datasets/tau2019sse"
    )
    A = a.get_audio_events("dev/split1_ir0_ov1_1")

    with pytest.raises(ValueError):
        a.get_audio_events("a")
