import soundata
from micarraylib import arraycoords
from micarraylib.code import Dataset
import re
 
marco_arrays = ["OCT3D", "Eigenmike", "PCMA3D", "DeccaCuboid", "2LCube", "Ambeo", "Hamasaki"]

array_format = {m:'A' for m in marco_arrays}
array_coords = {m:arraycoords.get_array(m).standard_coords('polar') for m in marco_arrays}
name = 'marco'

class marco(Dataset):

    def __init__(self, name, data_home, fs, array_format=array_format, array_coords=array_coords, download=True):
        super().__init__(name, array_format, fs, array_coords, data_home, download)

        self._array_clips_dict, self.sound_sources = self._sort_clip_ids(self)

    def _sort_clip_ids(self):
        """
        Sort clip_ids as belonging
        to a micarray and a source

        Returns:
            clip_ids_sorted (dict): a dictionary with soundata
                clips_ids sorted, so that keys indicate
                the array that the clips belong to.
                nested to specify the environment 
                in a group of clips
        """
        clip_ids = self.dataset.clip_ids
        clip_ids_split = [c.split('/') for c in clip_ids]
        sound_sources = list(set([c[0]+c[1] for c in clip_ids_split]))
        sound_sources = [re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', s)).split()[0] for s in sound_sources]
        clip_ids_sorted = {}
        for micarray in micarrays:
            for source in sound_sources:
                clip_ids_sorted[micarray][source] = [c for c in clip_ids if source in c and micarray in c and cap in c for cap in capsule]
    
        return clip_ids_sorted, sound_sources

    def _get_audio_array(self, micarray, source, fmt='A'):
        """
        combine single-capsule mono clips to 
        form an numpy array with all the audio recorded by
        a mirophone array, and transform to A or B format
        """
        if micarray not in self.array_names:
            raise ValueError("micarray is "+micarray+", but it should be one of ", self.array_names)
        if source not in self.sound_sources:
            raise ValueError("source is "+source+", but it should be one of ", self.sound_sources)
        if fmt not in ['A','B']:
        array_clips = self._array_clip_ids[micarray][source]
        all_clips = self.dataset.load_clips()
        audio_array = np.squeeze(np.array([all_clips[ac].audio[0] for ac in array_clips]))
        if fmt == 'A':
            return audio_array
        elif fmt == 'B':
            audio_array = 2b(audio_array, self.array_coords[micarray])
        return audio_array 
        

""""
"""
