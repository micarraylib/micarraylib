import soundata
from micarraylib import arraycoords
from micarraylib.core import Dataset
from micarraylib.utils import a2b
import numpy as np

import re
 
marco_arrays = ["OCT3D", "Eigenmike", "PCMA3D", "DeccaCuboid", "2LCube", "Ambeo", "Hamasaki"]

array_format = {m:'A' for m in marco_arrays}
array_coords = {m:arraycoords.get_array(m).standard_coords('polar') for m in marco_arrays}
name = 'marco'

class marco(Dataset):

    def __init__(self, name, data_home, fs, array_format=array_format, array_coords=array_coords, download=True):
        super().__init__(name, data_home, fs, array_format, array_coords, download)

        self.array_clips_dict, self.sound_sources = self._sort_clip_ids()

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
        sound_sources_in_clips = list(set([c[0]+'/'+c[1][:4] for c in clip_ids_split]))
        sound_sources = [re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', ''.join(s.split('/')))).split()[0] for s in sound_sources_in_clips]
        clip_ids_sorted = {k:{} for k in marco_arrays}
        for micarray in marco_arrays:
            for source, source_clip in zip(sound_sources, sound_sources_in_clips):
                clip_ids_sorted[micarray][source] = sorted([c for cap in self.array_capsules for c in clip_ids if source_clip in c and micarray in c and cap in c and micarray != "Ambeo" and micarray != "Eigenmike"])
                # add eigenmike
                clip_ids_sorted[micarray][source]

    
        return clip_ids_sorted, sound_sources

    def get_audio_numpy(self, micarray, source, fmt='A', N=None):
        """
        combine single-capsule mono clips to 
        form an numpy array with all the audio recorded by
        a mirophone array, and transform to A or B format
        This operation may take some time.
        """
        if micarray not in self.array_names:
            raise ValueError("micarray is "+micarray+", but it should be one of ", self.array_names)
        if not any ([source in s for s in self.sound_sources]):
            raise ValueError("source is "+source+", but it should be one of ", self.sound_sources)
        if fmt not in ['A','B']:
            raise ValueError('desired format should be A or B but is '+fmt )
        if fmt == 'B' and N == None:
            N = int(np.sqrt(len.self_array_clips_dict[micarray][source]))
        if fmt == 'B' and (N+1)**2 > len(self.array_clips_dict[micarray][source]):
            raise ValueError('N should be smaller than ')
        array_clips = self.array_clips_dict[micarray][source]
        all_clips = self.dataset.load_clips()
        audio_array = np.squeeze(np.array([all_clips[ac].audio[0] for ac in array_clips]))
        if fmt == 'A':
            return audio_array
        elif fmt == 'B':
            audio_array = a2b(N, audio_array, self.array_coords[micarray])
        return audio_array 
        

""""
"""
