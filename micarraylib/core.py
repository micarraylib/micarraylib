import soundata
import numpy as np
import matplotlib.pyplot as plt
from micarraylib.arraycoords.array_shapes_utils import _polar2cart


class Aggregate:
    """
    The generic dataset aggregator class

    Args:
        micarray_dataset_list (list): a list with the
            micarray.Dataset objects to aggregate
        fs (float): the sampling rate to use across
            datasets in the aggregate
    """

    def __init__(self, micarray_dataset_list, fs):
        self.fs = fs
        self.datasets = {dataset.name: dataset for dataset in micarray_dataset_list}
        for dataset in self.datasets.values():
            dataset.fs = fs


class Dataset:
    """
    The generic Dataset class

    Args:
        name (str): the dataset name (must be one of
            soundata dataset names)
        fs (int): the dataset's global sampling rate
            (indicated in the soundata loader)
        array_format (dict): a dictionary specifying
            the format (A or B) of the original audio files
            for each microphone array in the dataset
        capsule_coords (dict): a dictionary specifying
            each of the array's capsule polar coordinates,
            with the array's physical center at the
            origin of the 3D space.
        download (bool): whether the data needs to
            be downloaded by soundata (True by default)
        data_home (str): path to directory where the
            data is (directories must follow
            the soundata index struct)

    Attributes:
        name (str): the dataset name (must be one of
            soundata dataset names)
        dataset (soundata.Dataset)
        fs (int): the dataset's global sampling rate
            (indicated in the soundata loader)
        array_format (dict): a dictionary specifying
            the format (A or B) of the original audio files
            for each microphone array in the dataset
        array_names (list): list with all the arrays
            in the dataset
        capsule_coords (dict): a dictionary specifying
            each of the array's capsule polar coordinates,
            with the array's physical center at the
            origin of the 3D space.
        array_capsules (dict):
        data_home (str): path to directory where the
            data is (directories inside data_home must
            follow the soundata index struct)
    """

    def __init__(
        self,
        name,
        fs,
        array_format,
        capsule_coords,
        download=True,
        data_home=None,
        partial_download=None,
        force_overwrite=False,
        cleanup=False,
    ):

        if download == False and data_home == None:
            raise ValueError(
                "You must specify the directory with the data in data_home if you do not want to download it."
            )
        self.name = name
        self.dataset = _initialize(
            name, data_home, download, partial_download, force_overwrite, cleanup
        )
        self.fs = fs
        self.array_names = list(capsule_coords.keys())
        self.array_format = array_format
        self.array_capsules = {
            a: list(capsule_coords[a].keys()) for a in capsule_coords.keys()
        }
        self.capsule_coords = capsule_coords
        self.data_home = data_home

    def get_capsule_coords_numpy(self, micarray):
        """
        returns the capsule coordinates in
        polar form

        Args:
            micarray (str): the name of the
                microphone array that we are
                getting coordinates for

        Returns:
            tuple with
                1) numpy array of shape (n,3)
                2) capsule coordinate names (list)
        """

        if micarray not in self.array_names:
            raise ValueError(
                "micarray is {}, but it should be one of {}".format(
                    micarray, ", ".join(self.array_names)
                )
            )
        capsule_coords = np.array([c for c in self.capsule_coords[micarray].values()])
        capsule_names = [c for c in self.capsule_coords[micarray].keys()]
        return capsule_coords, capsule_names

    def plot_micarray(self, micarray, show=True):
        """
        returns the capsule coordinates in
        polar form

        Args:
            micarray (str): the name of the
                microphone array that we are
                getting coordinates for

        """

        if micarray not in self.array_names:
            raise ValueError(
                "micarray is {}, but it should be one of {}".format(
                    micarray, ", ".join(self.array_names)
                )
            )
        capsule_coords, capsule_names = self.get_capsule_coords_numpy(micarray)
        capsule_coords_dict = _polar2cart(
            {c: capsule_coords[i] for i, c in enumerate(capsule_names)}, "radians"
        )
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        for n, m in capsule_coords_dict.items():
            ax.scatter(m[0], m[1], m[2], color="b", label=micarray)
            ax.text(m[0], m[1], m[2], "%s" % (str(n)), size=20, zorder=1, color="k")

        ax.set_xlabel("x (meters)")
        ax.set_ylabel("y (meters)")
        ax.set_zlabel("z (meters)")
        if show:
            plt.show()


def _initialize(
    name,
    data_home=None,
    download=True,
    partial_download=None,
    force_overwrite=False,
    cleanup=False,
):
    """
    Initializes and downloads the dataset
    using the soundata API

    Args:
        data_home (str): points to the directory with
            the data
        download (bool): True by default. soundata
            will skip this step if the files already exist
    """
    dataset = soundata.initialize(name, data_home)
    if download:
        dataset.download(partial_download, force_overwrite, cleanup)
    return dataset
