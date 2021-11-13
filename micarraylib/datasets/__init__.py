from micarraylib.datasets import tau2021sse_nigens_loader
from micarraylib.datasets import tau2020sse_nigens_loader
from micarraylib.datasets import tau2019sse_loader
from micarraylib.datasets import eigenscape_loader
from micarraylib.datasets import marco_loader


def tau2021sse_nigens(download=True, data_home=None):
    """
    helper to load the tau2021sse_nigens Dataset class
    """

    return tau2021sse_nigens_loader.tau2021sse_nigens(
        download=download, data_home=data_home
    )


def tau2020sse_nigens(download=True, data_home=None):
    """
    helper to load the tau2020sse_nigens Dataset class
    """

    return tau2020sse_nigens_loader.tau2020sse_nigens(
        download=download, data_home=data_home
    )


def tau2019sse(download=True, data_home=None):
    """
    helper to load the tau2019sse Dataset class
    """

    return tau2019sse_loader.tau2019sse(download=download, data_home=data_home)


def eigenscape(download=True, data_home=None):
    """
    helper to load the eigenscape Dataset class
    """

    return eigenscape_loader.eigenscape(download=download, data_home=data_home)


def eigenscape_raw(download=True, data_home=None):
    """
    helper to load the eigenscape_raw Dataset class
    """

    return eigenscape_loader.eigenscape_raw(download=download, data_home=data_home)


def marco(download=True, data_home=None):
    """
    helper to load the eigenscape_raw Dataset class
    """

    return marco_loader.marco(download=download, data_home=data_home)
