import micarraylib.datasets


def test_tau2021sse_nigens_helper():

    a = micarraylib.datasets.tau2021sse_nigens(download=False, data_home="~/")
    assert isinstance(
        a, micarraylib.datasets.tau2021sse_nigens_loader.tau2021sse_nigens
    )


def test_tau2020sse_nigens_helper():

    a = micarraylib.datasets.tau2020sse_nigens(download=False, data_home="~/")
    assert isinstance(
        a, micarraylib.datasets.tau2020sse_nigens_loader.tau2020sse_nigens
    )


def test_tau2019sse_helper():

    a = micarraylib.datasets.tau2019sse(download=False, data_home="~/")
    assert isinstance(a, micarraylib.datasets.tau2019sse_loader.tau2019sse)


def test_marco_helper():

    a = micarraylib.datasets.marco(download=False, data_home="~/")
    assert isinstance(a, micarraylib.datasets.marco_loader.marco)


def test_eigenscape_helper():

    a = micarraylib.datasets.eigenscape(download=False, data_home="~/")
    assert isinstance(a, micarraylib.datasets.eigenscape_loader.eigenscape)


def test_eigenscape_raw_helper():

    a = micarraylib.datasets.eigenscape_raw(download=False, data_home="~/")
    assert isinstance(a, micarraylib.datasets.eigenscape_loader.eigenscape_raw)
