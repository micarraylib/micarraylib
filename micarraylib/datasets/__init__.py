import soundata
from micarraylib import arraycoords
from micarraylib.core import Dataset
from micarraylib.utils import a2b, _get_audio_numpy
import numpy as np

import re
 
marco_arrays = ["OCT3D", "Eigenmike", "PCMA3D", "DeccaCuboid", "2LCube", "Ambeo", "Hamasaki"]

array_format = {m:'A' for m in marco_arrays}
capsule_coords = {m:arraycoords.get_array(m).standard_coords('polar') for m in marco_arrays}
name = 'marco'

class marco(Dataset):

    def __init__(self, name=name, fs=48000, array_format=array_format, capsule_coords=capsule_coords, download=True, data_home=None):
        super().__init__(name, fs, array_format, capsule_coords, download, data_home)

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
            sound_sources (list): 
        """
        clip_ids = self.dataset.clip_ids
        clip_ids_split = [c.split('/') for c in clip_ids]
        sound_sources_in_clips = list(set([c[0]+'/'+c[1][:4] for c in clip_ids_split]))
        sound_sources = [re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', ''.join(s.split('/')))).split()[0] for s in sound_sources_in_clips]
        clip_ids_sorted = {k:{} for k in marco_arrays}
        for micarray in marco_arrays:
            for source, source_clip in zip(sound_sources, sound_sources_in_clips):
                clip_ids_sorted[micarray][source] = sorted([c for c in clip_ids if source_clip in c and micarray in c])
    
        return clip_ids_sorted, sound_sources

    def get_audio_numpy(self, micarray, source, fmt='A', N=None, fs=None):
        """
        combine mono clips single-capsule mono clips to 
        form an numpy array with all the audio recorded by
        a mirophone array, and transform to A or B format
        This operation may take some time.
        """
        if fs == None:
            fs = self.fs
        if micarray not in self.array_names:
            raise ValueError("micarray is "+micarray+", but it should be one of ", self.array_names)
        if not any ([source in s for s in self.sound_sources]):
            raise ValueError("source is "+source+", but it should be one of ", self.sound_sources)
        return _get_audio_numpy(self.array_clips_dict[micarray][source], self.dataset, 'A', fmt, self.capsule_coords[micarray], N, fs)
