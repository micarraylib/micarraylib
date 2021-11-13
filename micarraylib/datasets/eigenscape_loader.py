from micarraylib import arraycoords
from micarraylib.core import Dataset
from micarraylib.utils import _get_audio_numpy
import numpy as np

EIGENSCAPE_ARRAYS = ["Eigenmike"]
eigenscape_raw_array_format = {m: "A" for m in EIGENSCAPE_ARRAYS}
eigenscape_capsule_coords = {
    m: arraycoords.get_array(m).standard_coords("polar") for m in EIGENSCAPE_ARRAYS
}


class eigenscape_raw(Dataset):
    """
    The eigenscape_raw Dataset class

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
        micarray_clip_ids (dict): a dictionary with soundata
            clips_ids sorted by the microphone array
            and sound source that they belong to.
        clips_list (list): a list with the different
            sound sources in the dataset, available with each
            of the microphone arrays.
    """

    def __init__(
        self,
        name="eigenscape_raw",
        fs=48000,
        array_format=eigenscape_raw_array_format,
        capsule_coords=eigenscape_capsule_coords,
        download=True,
        data_home=None,
    ):
        super().__init__(name, fs, array_format, capsule_coords, download, data_home)

        self.micarray_clip_ids, self.clips_list = self._sort_clip_ids()

    def _sort_clip_ids(self):
        """
        Sort clip_ids as belonging
        to a micarray and a source

        Returns:
            clip_ids_sorted (dict): a dictionary with soundata
                clips_ids sorted by the microphone array
                and sound source that they belong to.
            clips_list (list)
        """
        clip_ids = self.dataset.clip_ids
        clip_ids_sorted = {k: {c: [c] for c in clip_ids} for k in EIGENSCAPE_ARRAYS}
        return clip_ids_sorted, clip_ids

    def get_audio_numpy(self, clip_id, micarray="Eigenmike", fmt="A", N=None, fs=None):
        """
        combine single-capsule mono clips to
        form an numpy array with all the audio recorded by
        a mirophone array, and transform to A or B format
        if the user indicates it.

        Args:
            micarray (str): the name of the micarray to
                get audio for
            source (str): the sound source that was
                recorded in the audio
            fmt (str): the desired format that we
                want the audio in (A or B in the
                ambisonics sense)
            N (int): the order of B-format
            fs (int): the sampling rate we want
                the audio in (resampling as needed).

        Returns:
            a numpy array with the audio

        Note: this operation may take some time.
        """
        if fs == None:
            fs = self.fs
        if fmt == "B":
            raise ValueError(
                "Conversion between formats not necessary for eigenscape dataset. Each format already has its dataset in micarraylib (and soundata): eigenscape (B-format) and eigenscape_raw (A-format)"
            )
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
        return _get_audio_numpy(
            self.micarray_clip_ids[micarray][clip_id],
            self.dataset,
            self.array_format[micarray],
            fmt,
            self.capsule_coords[micarray],
            N,
            fs,
        )


eigenscape_array_format = {m: "B" for m in EIGENSCAPE_ARRAYS}


class eigenscape(Dataset):
    """
    The eigenscape Dataset class

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
        micarray_clip_ids (dict): a dictionary with soundata
            clips_ids sorted by the microphone array
            and sound source that they belong to.
        clips_list (list): a list with the different
            sound sources in the dataset, available with each
            of the microphone arrays.
    """

    def __init__(
        self,
        name="eigenscape",
        fs=48000,
        array_format=eigenscape_array_format,
        capsule_coords=eigenscape_capsule_coords,
        download=True,
        data_home=None,
    ):
        super().__init__(name, fs, array_format, capsule_coords, download, data_home)

        self.micarray_clip_ids, self.clips_list = self._sort_clip_ids()

    def _sort_clip_ids(self):
        """
        Sort clip_ids as belonging
        to a micarray and a source

        Returns:
            clip_ids_sorted (dict): a dictionary with soundata
                clips_ids sorted by the microphone array
                and sound source that they belong to.
            clips_list (list)
        """
        clip_ids = self.dataset.clip_ids
        clip_ids_sorted = {k: {c: [c] for c in clip_ids} for k in EIGENSCAPE_ARRAYS}
        return clip_ids_sorted, clip_ids

    def get_audio_numpy(self, clip_id, micarray="Eigenmike", fmt="B", N=None, fs=None):
        """
        combine single-capsule mono clips to
        form an numpy array with all the audio recorded by
        a mirophone array, and transform to A or B format
        if the user indicates it.

        Args:
            micarray (str): the name of the micarray to
                get audio for
            clip_id (str): the sound source that was
                recorded in the audio
            fmt (str): the desired format that we
                want the audio in (A or B in the
                ambisonics sense)
            N (int): the order of B-format
            fs (int): the sampling rate we want
                the audio in (resampling as needed).

        Returns:
            a numpy array with the audio

        Note: this operation may take some time.
        """
        if fs == None:
            fs = self.fs
        if fmt == "A":
            raise ValueError(
                "Conversion between formats not necessary for eigenscape dataset. Each format already has its dataset: eigenscape (B-format) and eigenscape_raw (A-format)"
            )
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
        return _get_audio_numpy(
            self.micarray_clip_ids[micarray][clip_id],
            self.dataset,
            self.array_format[micarray],
            fmt,
            self.capsule_coords[micarray],
            N,
            fs,
        )
