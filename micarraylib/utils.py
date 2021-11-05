from spaudiopy import sph
import numpy as np
import warnings

def a2b(N, audio_numpy, array_coords):
    """
    converts an array with microphone array
    recording channels (raw A-format) to 
    B-format ambisonics via simple
    encoding using the pseudo_inverse of 
    the spherical harmonics matrix
    """

    coords_numpy = np.array([c for c in array_coords.values()])
    SH = sph.sh_matrix(N, coords_numpy[:,1], coords_numpy[:,2], 'real')
    Y = np.linalg.pinv(SH)
    return np.dot(Y, audio_numpy)

def _get_audio_numpy(clip_names, dataset, fmt_in, fmt_out, capsule_coords=None, N=None):
    """
    combine clips that correspond to a multitrack recording
    into a numpy array and return it in A or B format. 

    Args:
        clip_names (list): list of strings with names of clips
            to be combined
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

    Returns:
        audio_array (np.array): the numpy array with the audio
    """
    all_dataset_clip_names = dataset.load_clips()
    if fmt_in not in ['A','B'] or fmt_out not in ['A','B']:
        raise ValueError("the input and output formats should be either 'A' or 'B' but fmt_in is {} and fmt_out is {}".format(fmt_in,fmt_out))
    if fmt_in == 'B' and fmt_out == 'A':
        raise ValueError('B to A conversion currently not supported')
    if fmt_out == 'B' and N!= None and (N+1)**2 > len(clip_names):
        raise ValueError('(N+1)^2 should be less than or equal to the number of channels being combined but (N+1)^2 is {} and len(clip_names) is {}'.format((N+1)**2,len(clip_nameS)))
    if fmt_in != fmt_out and capsule_coords == None:
        raise ValueError('To convert between A and B format you must specify capsule coordinates')
    audio_array = np.squeeze(np.array([all_dataset_clip_names[ac].audio[0] for ac in clip_names]))
    if fmt_in == fmt_out:
        if N != None:
            warnings.warn("N parameter was specified but not used")
        return audio_array
    if fmt_in == 'A' and fmt_out == 'B':
        N = int(np.sqrt(len(clip_names))) if N==None else N
        audio_array = a2b(N, audio_array, capsule_coords)
        return audio_array


    
    

