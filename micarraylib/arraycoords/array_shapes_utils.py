import math
import numpy as np


def _deg2rad(coords_dict):
    """
    Take a dictionary with microphone array
    capsules and 3D polar coordinates to
    convert them from degrees to radians

    colatitude, azimuth, and radius (radius
    is left intact)
    """
    return {
        m: [math.radians(c[0]), math.radians(c[1]), c[2]]
        for m, c in coords_dict.items()
    }


def _polar2cart(coords_dict, units=None):
    """
    Take a dictionary with microphone array
    capsules and polar coordinates and convert
    to cartesian

    Parameters:
        units: (str) indicating 'degrees' or 'radians'
    """
    if units == None or units != "degrees" and units != "radians":
        raise ValueError("you must specify units of 'degrees' or 'radians'")
    elif units == "degrees":
        coords_dict = _deg2rad(coords_dict)
    return {
        m: [
            c[2] * math.sin(c[0]) * math.cos(c[1]),
            c[2] * math.sin(c[0]) * math.sin(c[1]),
            c[2] * math.cos(c[0]),
        ]
        for m, c in coords_dict.items()
    }


def _centercoords(coords_dict):
    """
    Take a dictionary with microphone array
    capsules and cartesian coordinates, find the center
    of such coordinates and subtract it to center all
    the coordinates around zero.
    """
    C = np.array([c for c in coords_dict.values()])
    c_mean = np.mean(C, axis=0)
    return {m: c - c_mean for m, c in coords_dict.items()}


def _cart2polar(coords_dict):
    """
    Take a dictionary with microphone array
    capsules and cartesian coordinates, and convert
    to polar: colatitude (radians), azimuth (radians), radius
    """
    return {
        m: [
            math.acos(c[2] / math.sqrt(c[0] ** 2 + c[1] ** 2 + c[2] ** 2)),
            math.atan(c[1] / c[0]) if c[0] >= 0 else math.atan(c[1] / c[1]) + math.pi,
            math.sqrt(c[0] ** 2 + c[1] ** 2 + c[2] ** 2),
        ]
        for m, c in coords_dict.items()
    }
