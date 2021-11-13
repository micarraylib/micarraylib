from micarraylib import arraycoords
from micarraylib.core import Dataset
from micarraylib.utils import _get_audio_numpy
import numpy as np

TAUSSE_ARRAYS = ["Eigenmike"]
tausse_array_format = {m: "A" for m in TAUSSE_ARRAYS}
tausse_capsule_coords = {m: {} for m in TAUSSE_ARRAYS}
tausse_capsule_coords["Eigenmike"] = {
    k: v
    for k, v in arraycoords.get_array("Eigenmike").standard_coords("polar").items()
    if k in ["6", "10", "22", "26"]
}


class tau2021sse_nigens(Dataset):
    """
    The tau2021sse Dataset class

    Args:
        name (str): the dataset name (must be one of
            soundata dataset names)
        fs (int): the dataset's global sampling rate
            (indicated in the soundata loader)
        array_format (dict): a dictionary specifying
            the format (A or B) of the audio files
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
            the format (A or B) of the audio files
            for each microphone array in the dataset
        array_names (list): list with all the arrays
            in the dataset
        capsule_coords (dict): a dictionary specifying
            each of the array's capsule polar coordinates,
            with the array's physical center at the
            origin of the 3D space.
        array_capsules (dict):
        data_home (str): path to directory where the
            data is (directories must follow
            the soundata index struct)
        micarray_clips_id (dict): a dictionary with soundata
            clips_ids sorted by the microphone array
            that they belong to.
        clips_list (list): a list with the different
            clip_ids in the dataset that were recorded
            with each of the microphone arrays.
    """

    def __init__(
        self,
        name="tau2021sse_nigens",
        fs=24000,
        array_format=tausse_array_format,
        capsule_coords=tausse_capsule_coords,
        download=True,
        data_home=None,
    ):
        super().__init__(name, fs, array_format, capsule_coords, download, data_home)

        self.micarray_clip_ids, self.clips_list = self._sort_clip_ids()

    def _sort_clip_ids(self):
        """
        Sort clip_ids as belonging
        to a micarray

        Returns:
            clip_ids_sorted (dict): a dictionary with soundata
                clips_ids sorted by the microphone array
                that they belong to.
            clips_list (list)
        """
        clip_ids = self.dataset.clip_ids
        clip_ids = list(set([c[4:] for c in clip_ids]))
        clip_ids_sorted = {k: {c: [c] for c in clip_ids} for k in TAUSSE_ARRAYS}
        return clip_ids_sorted, clip_ids

    def get_audio_numpy(self, clip_id, micarray="Eigenmike", fmt="A", fs=None):
        """
        combine single-capsule mono clips to
        form an numpy array with all the audio recorded by
        a mirophone array, and return in A or B format.

        Args:
            clip_id (str): the clip_id of the
                recorded audio
            micarray (str): the name of the micarray to
                get audio for
            fmt (str): the desired format that we
                want the audio in ('A' or 'B' in the
                ambisonics sense)
            fs (int): the sampling rate we want
                the audio in (resampling as needed).

        Returns:
            a numpy array with the audio

        Note: this operation may take some time.
        """
        if fs == None:
            fs = self.fs
        if micarray not in self.array_names:
            raise ValueError(
                "micarray is {}, but it should be one of {}".format(
                    micarray, ", ".join(self.array_names)
                )
            )
        if not any([clip_id == s for s in self.clips_list]):
            raise ValueError(
                "clip_id is {}, but it should be one of {}".format(
                    clip_id, ", ".join(self.clips_list)
                )
            )
        if fmt == "A":
            return _get_audio_numpy(
                ["".join(["mic_", self.micarray_clip_ids[micarray][clip_id][0]])],
                self.dataset,
                self.array_format[micarray],
                fmt,
                self.capsule_coords[micarray],
                fs=fs,
            )
        if fmt == "B":
            return _get_audio_numpy(
                ["".join(["foa_", self.micarray_clip_ids[micarray][clip_id][0]])],
                self.dataset,
                "B",
                fmt,
                self.capsule_coords[micarray],
                fs=fs,
            )

    def get_audio_events(self, clip_id):
        """
        get the spatial events associated with a clip_id

        Args:
            clip_id (str): the sound source that was
                recorded in the audio

        Returns:
            a soundata.SpatialEvents object
        """
        if not any([clip_id == s for s in self.clips_list]):
            raise ValueError(
                "clip_id is {}, but it should be one of {}".format(
                    clip_id, ", ".join(self.clips_list)
                )
            )
        all_dataset_clip_names = self.dataset.load_clips()
        return all_dataset_clip_names["".join(["foa_", clip_id])].spatial_events
