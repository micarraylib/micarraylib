from .array_shapes_utils import _deg2rad, _polar2cart, _cart2polar, _centercoords
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
        if coords_form == None:
            raise ValueError(
                "you must specify the form (cartesian or polar) of your capsule coordinates"
            )
        if coords_form == "cartesian" and angle_units != None:
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
        if self.coords_form == "cartesian":
            self.coords_dict = _centercoords(self.coords_dict)
            return self.coords_dict
        elif self.angle_units == "degrees":
            self.coords_dict = _deg2rad(self.coords_dict)
            self.angle_units = "radians"
        self.coords_dict = _polar2cart(self.coords_dict, "radians")
        self.coords_form = "cartesian"
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
        if form == "cartesian":
            return self.center_coords()
        elif form == "polar":
            self.center_coords()
            self.coords_dict = _cart2polar(self.coords_dict)
            self.coords_form = "polar"
            self.angle_units = "radians"
            return self.coords_dict
