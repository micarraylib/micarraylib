import soundata

class Dataset:
    """
    The generic Dataset class

    Args:
        name (str): the dataset name (must be one of 
            soundata dataset names)
        array_format (dict): a dictionary specifying
            the format (A or B) of the audio files
        array_coords (dict): a dictionary specifying
            the array's capsule polar coordinates, 
            with the array's physical center at the 
            center of the 3D space.
        data_home (str): path to directory where the
            data is (follows the soundata index struct)
        download (bool): whether the data needs to
            be downloaded by soundata (True by default)

    Attributes:
        dataset (soundata.Dataset)
    """

    def __init__(self, name, data_home, fs, array_format, array_coords, download=True):

        dataset = _initialize(name, data_home, download)
        self.dataset = dataset
        self.array_format = array_format
        self.fs = 48000
        self.array_names = list(array_coords.keys())
        self.array_coords = array_coords
        self.array_capsules = {a:list(array_coords[a].keys()) for a in array_coords.keys()}

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
