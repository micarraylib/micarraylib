from spaudiopy import sph
import numpy as np
import warnings
import librosa


def a2b(N, audio_numpy, capsule_coords):
    
    print("N: ",N)
    print("audio_numpy: ",audio_numpy)
    print("capsule_coords: ",capsule_coords)
    
    """
    encodes recordings from microphone array
    capsules (raw A-format) to B-format
    ambisonics using the pseudo_inverse of
    the spherical harmonics matrix

    Args:
        N (int): the order of B format
        audio_numpy (np.array): the numpy array with the audio
        capsule_coords (dict): dictionary with channel names and
            corresponding coordinates in polar form (colatitude
            and azimuth in radians)

    Returns:
        a numpy array with the encoded B format
    """

    coords_numpy = np.array([c for c in capsule_coords.values()])
    SH = sph.sh_matrix(N, coords_numpy[:, 1], coords_numpy[:, 0], "real")
    Y = np.linalg.pinv(SH)
    return np.dot(Y, audio_numpy)


def _get_audio_numpy(
    clip_names, dataset, fmt_in, fmt_out, capsule_coords=None, N=None, fs=None
):
    """
    print("clip_names: ",clip_names)
    print("dataset: ",dataset)
    print("fmt_in: ",fmt_in)
    print("fmt_out: ",fmt_out)
    print("capsule_coords: ",capsule_coords)
    print("N: ",N)
    print("fs: ",fs)
    print("\ncapsule_coords type:")
    print(type(capsule_coords))
    """

    """
    combine clips that correspond to a multitrack recording
    into a numpy array and return it in A or B format.

    Args:
        clip_names (list): list of strings with names of clips
            to be loaded (and combined if different clips have
            the recording by different microphone capsules).
        dataset (soundata.Dataset): the soundata dataset where
            the clips can be loaded from
        fmt_in (str): whether the clips originally are in A or B
            format
        fmt_out (str): the target format (A or B). Currently it only
            works A->B
        capsule_coords (dict): dictionary with channel names and
            corresponding coordinates in polar form (colatitude
            and azimuth in radians)
        N (int): the order of B format
        fs (int): the target sampling rate

    Returns:
        audio_array (np.array): the numpy array with the audio
    """
    all_dataset_clip_names = dataset.load_clips()
    if fmt_in not in ["A", "B"] or fmt_out not in ["A", "B"]:
        raise ValueError(
            "the input and output formats should be either 'A' or 'B' but fmt_in is {} and fmt_out is {}".format(
                fmt_in, fmt_out
            )
        )
    if fmt_in == "B" and fmt_out == "A":
        raise ValueError("B to A conversion currently not supported")
    
    if fmt_in == "A" and fmt_out == "B" and capsule_coords == None:
        raise ValueError(
            "To convert between A and B format you must specify capsule coordinates"
        )

    audio_data = [all_dataset_clip_names[ac].audio for ac in clip_names]
    audio_array, audio_fs = list(map(list, zip(*audio_data)))
    audio_array = np.squeeze(np.array(audio_array))

    if fmt_out == "B" and N != None and (N + 1) ** 2 > len(audio_array):
        raise ValueError(
            "(N+1)^2 should be less than or equal to the number of channels being combined but (N+1)^2 is {} and len(audio_array) is {}".format(
                (N + 1) ** 2, len(audio_array)
            )
        )

    audio_fs = audio_fs[0]
    
    if fs != None and audio_fs != fs:
        audio_array = librosa.resample(audio_array, audio_fs, fs)
    if fmt_in == fmt_out:
        if N != None:
            warnings.warn(UserWarning("N parameter was specified but not used"))
        return audio_array
    if fmt_in == "A" and fmt_out == "B":
        N = int(np.sqrt(len(clip_names)) - 1) if N == None else N
        audio_array = a2b(N, audio_array, capsule_coords)
        return audio_array
