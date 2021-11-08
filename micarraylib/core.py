import soundata

class Dataset:
    """
    The generic Dataset class

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
    """

    def __init__(self, name, fs, array_format, capsule_coords, download=True, data_home=None):

        if download == False and data_home == None:
            raise ValueError('You must specify the directory with the data in data_home if you do not want to download it.')
        self.name = name
        self.dataset = _initialize(name, data_home, download)
        self.fs = fs
        self.array_names = list(capsule_coords.keys())
        self.array_format = array_format
        self.array_capsules = {a:list(capsule_coords[a].keys()) for a in capsule_coords.keys()}
        self.capsule_coords = capsule_coords
        self.data_home = data_home

def _initialize(name, data_home=None, download=True):
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
        dataset.download()
    return dataset
