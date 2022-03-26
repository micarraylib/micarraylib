from spaudiopy import sph
import numpy as np
import warnings
import librosa
import scipy as sp


def a2b(N, audio_numpy, capsule_coords):

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

def b2binaural(audio_numpy, fs, N):

    """
    decode the audio from B format to binaural

    Args:
        audio_array (np.array): the audio numpy array in B format
        fs (int): the target sampling rate
        N (int): the order of B format. Currently only support 1st order

    Returns:
        audio_array (np.array): the 2 channel numpy array of the audio
    """

    W, X, Y, Z = audio_numpy[0], audio_numpy[1], audio_numpy[2], audio_numpy[3]
    HRTF_FS = 44100
    h_length = round(200 * float(fs) / HRTF_FS)

    phis = np.array([-125, -55, 0, 55, 125, 180, 0, 0], dtype=np.float32) * np.pi / 180
    thetas = np.array([0, 0, 0, 0, 0, 0, 90, -45], dtype=np.float32) * np.pi / 180
    p_idx = [23, 23, 13, 3, 3, 13, 13, 13]
    t_idx = [9, 9, 9, 9, 9, 9, 25, 0]
    hrtf = sp.io.loadmat('micarraylib/datasets/hrir_021.mat')

    left = np.zeros(W.size)
    right = np.zeros(W.size)
    for i in range(phis.size):
        w_ft = W + 0.7071 * (
               X * np.cos(phis[i]) * np.cos(thetas[i]) +
               Y * np.sin(phis[i]) * np.cos(thetas[i]) +
               Z * np.sin(thetas[i]))

        hrtf_l = sp.signal.resample(hrtf['hrir_l'][p_idx[i], t_idx[i], :], h_length)
        hrtf_r = sp.signal.resample(hrtf['hrir_r'][p_idx[i], t_idx[i], :], h_length)

        left += sp.signal.convolve(w_ft, hrtf_l, mode='same')
        right += sp.signal.convolve(w_ft, hrtf_r, mode='same')

    return np.vstack((left, right)) / 4


def _get_audio_numpy(
    clip_names, dataset, fmt_in, fmt_out, capsule_coords=None, N=None, fs=None, is_binaural_out=False
):

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
        is_binaural_out (boolean): whether the output should be decoded
            into binaural form

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
            "(N+1)^2 should be less than or equal to the number of capsules being converted to B format, but (N+1)^2 is {} and the number of capsules is {}".format(
                (N + 1) ** 2, len(audio_array)
            )
        )
    audio_fs = audio_fs[0]
    if fs != None and audio_fs != fs:
        audio_array, audio_fs = librosa.resample(audio_array, audio_fs, fs), fs
    if fmt_in == fmt_out:
        if N != None:
            warnings.warn(UserWarning("N parameter was specified but not used"))
        return audio_array
    if fmt_in == "A" and fmt_out == "B":
        N = int(np.sqrt(len(clip_names)) - 1) if N == None else N
        audio_array = a2b(N, audio_array, capsule_coords)
        if is_binaural_out:
            audio_array = b2binaural(audio_array, audio_fs, N)
        return audio_array
