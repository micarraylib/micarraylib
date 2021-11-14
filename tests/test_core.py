import soundata
from micarraylib.core import Dataset, _initialize, Aggregate
import micarraylib.datasets
import micarraylib.arraycoords
import matplotlib.pyplot as plt
import pytest
import mock
import os
import numpy as np
import librosa


def test_Aggregate():

    a = micarraylib.datasets.marco(
        download=False, data_home="tests/resources/datasets/marco"
    )
    b = micarraylib.datasets.eigenscape_raw(
        download=False, data_home="tests/resources/datasets/eigenscape_raw"
    )
    c = micarraylib.datasets.tau2019sse(
        download=False, data_home="tests/resources/datasets/tau2019sse"
    )

    C = Aggregate([a, b, c], 8000)

    assert C.datasets["marco"].name == "marco"
    assert C.datasets["eigenscape_raw"].name == "eigenscape_raw"
    assert C.datasets["tau2019sse"].name == "tau2019sse"
    assert all([c.fs == 8000 for c in C.datasets.values()])

    data_dir = "tests/resources/datasets/marco"
    A = C.datasets["marco"].get_audio_numpy("impulse_response+90d", "OCT3D")
    wavs_dir = os.path.join(data_dir, "3D-MARCo Impulse Responses/01_Speaker_+90deg_3m")
    wavs = os.listdir(wavs_dir)
    wavs.sort()
    B = np.array(
        [librosa.load(os.path.join(wavs_dir, w), 48000, mono=False)[0] for w in wavs]
    )
    B = librosa.resample(B, 48000, 8000)
    assert np.allclose(A, B)


def test_Dataset():

    a = Dataset(
        "eigenscape",
        1,
        {"a": "A"},
        {"a": {"b": [0, 0, 0]}},
        download=False,
        data_home="/",
    )
    assert a.name == "eigenscape"
    assert isinstance(a.dataset, soundata.datasets.eigenscape.Dataset)
    assert a.fs == 1
    assert a.array_names == ["a"]
    assert a.array_format == {"a": "A"}
    assert a.array_capsules == {"a": ["b"]}
    assert a.capsule_coords == {"a": {"b": [0, 0, 0]}}
    assert a.data_home == "/"
    with pytest.raises(ValueError):
        Dataset("name", 1, {"a": "A"}, {"a": {"b": [0, 0, 0]}}, download=False)


def test_Dataset_get_capsule_coords():

    a = micarraylib.datasets.marco(download=False, data_home="~/")
    A, B = a.get_capsule_coords_numpy("OCT3D")
    C = micarraylib.arraycoords.get_array("OCT3D").standard_coords("polar")
    D = [c for c in C.keys()]
    C = np.array([c for c in C.values()])

    assert np.allclose(A, C)
    assert B == D

    with pytest.raises(ValueError):
        a.get_capsule_coords_numpy("foo")


def test_Dataset_plot_micarray():

    a = micarraylib.datasets.marco(download=False, data_home="~/")
    a.plot_micarray("OCT3D", show=False)


def test_initialize():

    a = _initialize("eigenscape", data_home=None, download=False)
    assert isinstance(a, soundata.datasets.eigenscape.Dataset)


@mock.patch("soundata.datasets.eigenscape.Dataset.download")
def test_initialize_download_true(mock_method):
    _initialize("eigenscape", data_home="~/", download=True)
    mock_method.assert_called_once()
