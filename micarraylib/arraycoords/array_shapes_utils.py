import math
import numpy as np

class micarray:
    """
    General micarray class

    Args:
        coords_dict (dict): a dictionary with capsule names 
            and coordinates.
        coords_form (str): whether 'polar' or 'cartesian' form. 
            The units of cartesian are assumed to be in meters.
        angle_units (str): if polar, whether angles are in 
            'degrees' or 'radians'.
    """

    def __init__(self, coords_dict, coords_form=None, angle_units=None, name=None):
        if coords_form == 'cartesian' and angle_units!=None:
            raise ValueError("cartesian coordinates do not need angle_units")
        self.name = name
        self.capsule_names = list(coords_dict.keys())
        self.coords_dict = coords_dict
        self.coords_form = coords_form
        self.angle_units = angle_units

    def center_coords(self):
        """
        Ensures that the array's physical center is at 
        the origin of the coordinate system
        Operates in place and returns the coords_dict
        in cartesian form 
        """
        if self.coords_form == 'cartesian':
            self.coords_dict = _centercoords(self.coords_dict)
            return self.coords_dict
        elif self.angle_units == 'degrees':
            self.coords_dict = _deg2rad(self.coords_dict)
            self.angle_units = 'radians'
        self.coords_dict = _polar2cart(self.coords_dict, 'radians')
        self.coords_form = 'cartesian'
        self.angle_units = None
        self.coords_dict = _centercoords(self.coords_dict)
        return self.coords_dict
        
    def standard_coords(self, form=None):
        """
        process the array's raw coordinates to 
        obtain the standard coordinates in the desired form

        Args:
            form (str): either 'polar' or 'cartesian' 
                polar returns coordinates in radians
                cartesian returns coordinates in meters
        """
        if form == None:
            raise ValueError("you must specify a form")
        if form == 'cartesian':
            return self.center_coords()
        elif form == 'polar':
            self.center_coords()
            self.coords_dict = _cart2polar(self.coords_dict)
            self.coords_form = 'polar'
            self.angle_units = 'radians'
            return self.coords_dict 


def _deg2rad(coords_dict):
    """
    Take a dictionary with microphone array 
    capsules and 3D polar coordinates to
    convert them from degrees to radians

    colatitude, azimuth, and radius (radius
    is left intact)
    """
    return {
        m: [math.radians(c[0]), math.radians(c[1]), c[2]] for m, c in coords_dict.items()
    }

def _polar2cart(coords_dict, units=None):
    """
    Take a dictionary with microphone array 
    capsules and polar coordinates and convert
    to cartesian

    Parameters:
        units: (str) indicating 'degrees' or 'radians'
    """
    if units == None or units != 'degrees' and units != 'radians':
        raise ValueError("you must specify units of 'degrees' or 'radians'")
    elif units == 'degrees':
        coords_dict = _deg2rad(coords_dict)
    return {
        m: [
            c[2] * math.sin(c[0]) * math.cos(c[1]),
            c[2] * math.sin(c[0]) * math.sin(c[1]),
            c[2] * math.cos(c[0])
        ] for m, c in coords_dict.items()
    }

def _centercoords(coords_dict):
    """
    Take a dictionary with microphone array 
    capsules and cartesian coordinates, find the center
    of such coordinates and subtract it to center all
    the coordinates around zero. 
    """
    C = np.array([c for c in coords_dict.values()])
    c_mean = np.mean(C,axis=0)
    return {
        m: c - c_mean for m, c in coords_dict.items()
    }

def _cart2polar(coords_dict):
    """
    Take a dictionary with microphone array 
    capsules and cartesian coordinates, and convert
    to polar: colatitude (radians), azimuth (radians), radius
    """
    return {
        m: [
            math.acos(c[2]/math.sqrt(c[0]**2+c[1]**2+c[2]**2)),
            math.atan(c[1]/c[0]) if c[0] >= 0 else math.atan(c[1]/c[1]) + math.pi,
            math.sqrt(c[0]**2+c[1]**2+c[2]**2) 

        ] for m, c in coords_dict.items()
    }
