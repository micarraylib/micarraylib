import soundata
from micarraylib.core import Dataset, _initialize
import pytest
import mock


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


def test_initialize():

    a = _initialize("eigenscape", data_home=None, download=False)
    assert isinstance(a, soundata.datasets.eigenscape.Dataset)


@mock.patch("soundata.datasets.eigenscape.Dataset.download")
def test_initialize_download_true(mock_method):
    _initialize("eigenscape", data_home="~/", download=True)
    mock_method.assert_called_once()
