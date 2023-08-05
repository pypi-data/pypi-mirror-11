# -*- coding: utf-8 -*-
"""
===============================================================================
Atoms class for :class:`XYZAtom`\ s (:mod:`sknano.core.atoms._xyz_atoms`)
===============================================================================

An `Atoms` class container for :class:`~sknano.core.atoms.XYZAtom`\ s.

.. currentmodule:: sknano.core.atoms._xyz_atoms

"""
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
__docformat__ = 'restructuredtext en'

from collections import OrderedDict
from operator import attrgetter

import numpy as np

from sknano.core import xyz
from sknano.core.math import Vector, transformation_matrix
from sknano.core.geometric_regions import Cuboid  # , Rectangle
from ._atoms import Atoms
from ._xyz_atom import XYZAtom

__all__ = ['XYZAtoms']


class XYZAtoms(Atoms):
    """An eXtended `Atoms` class.

    Sub-class of `Atoms` class, and a container class for lists of
    :class:`~sknano.core.atoms.XYZAtom` instances.

    Parameters
    ----------
    atoms : {None, sequence, `XYZAtoms`}, optional
        if not `None`, then a list of `XYZAtom` instance objects or an
        existing `XYZAtoms` instance object.

    """
    @property
    def __atom_class__(self):
        return XYZAtom

    def sort(self, key=attrgetter('r'), reverse=False):
        super().sort(key=key, reverse=reverse)

    @property
    def CM(self):
        """Center-of-Mass coordinates of `Atoms`.

        Computes the position vector of the center-of-mass coordinates:

        .. math::

           \\mathbf{R}_{CM} = \\frac{1}{M}\\sum_{i=1}^{N_{\\mathrm{atoms}}}
           m_i\\mathbf{r}_i

        Returns
        -------
        CM : :class:`~sknano.core.math.Vector`
            The position vector of the center of mass coordinates.

        """
        masses = np.asarray([self.masses])
        coords = self.coords
        MxR = masses.T * coords
        CM = Vector(np.sum(MxR, axis=0) / np.sum(masses))
        CM.rezero()
        return CM

    @property
    def centroid(self):
        """Centroid of `Atoms`.

        Computes the position vector of the centroid of the `Atoms`
        coordinates.

        .. math::
           \\mathbf{C} =
           \\frac{\\sum_{i=1}^{N_{\\mathrm{atoms}}}
           m_i\\mathbf{r}_i}{\\sum_{i=1}^{N_{\\mathrm{atoms}}}m_i}

        Returns
        -------
        C : :class:`~sknano.core.math.Vector`
            The position vector of the centroid coordinates.
        """
        C = Vector(np.mean(self.coords, axis=0))
        C.rezero()
        return C

    @property
    def bounds(self):
        """Bounds of `Atoms`.

        Returns
        -------
        :class:`~sknano.core.geometric_regions.Cuboid`"""
        return Cuboid(pmin=[self.x.min(), self.y.min(), self.z.min()],
                      pmax=[self.x.max(), self.y.max(), self.z.max()])

    @property
    def coords(self):
        """Alias for :meth:`Atoms.r`."""
        return self.r

    @property
    def r(self):
        """:class:`~numpy:numpy.ndarray` of :attr:`Atom.r` position \
            `Vector`\ s"""
        return np.asarray([atom.r for atom in self])

    @property
    def dr(self):
        """:class:`~numpy:numpy.ndarray` of :attr:`Atom.dr` displacement \
            `Vector`\ s"""
        return np.asarray([atom.dr for atom in self])

    @property
    def x(self):
        """:class:`~numpy:numpy.ndarray` of `Atom`\ s :math:`x` coordinates."""
        return self.r[:, 0]

    @property
    def y(self):
        """:class:`~numpy:numpy.ndarray` of `Atom`\ s :math:`y` coordinates."""
        return self.r[:, 1]

    @property
    def z(self):
        """:class:`~numpy:numpy.ndarray` of `Atom`\ s :math:`z` coordinates."""
        return self.r[:, 2]

    @property
    def inertia_tensor(self):
        """Inertia tensor."""
        Ixx = (self.masses * (self.y**2 + self.z**2)).sum()
        Iyy = (self.masses * (self.x**2 + self.z**2)).sum()
        Izz = (self.masses * (self.x**2 + self.y**2)).sum()
        Ixy = Iyx = (-self.masses * self.x * self.y).sum()
        Ixz = Izx = (-self.masses * self.x * self.z).sum()
        Iyz = Izy = (-self.masses * self.y * self.z).sum()
        return np.array([[Ixx, Ixy, Ixz], [Iyx, Iyy, Iyz], [Izx, Izy, Izz]])

    def center_CM(self, axes=None):
        """Center atoms on CM coordinates."""
        dr = -self.CM
        self.translate(dr)

    def clip_bounds(self, region, center_before_clipping=False):
        """Remove atoms outside the given region.

        Parameters
        ----------
        region : :class:`~sknano.core.geometric_regions.`GeometricRegion`

        """
        CM0 = None
        if center_before_clipping:
            CM0 = self.CM
            self.translate(-CM0)

        self.data = [atom for atom in self if region.contains(atom.r)]

        if CM0 is not None:
            self.translate(CM0)

    def get_coords(self, asdict=False):
        """Return atom coords.

        Parameters
        ----------
        asdict : :class:`~python:bool`, optional

        Returns
        -------
        coords : :class:`~python:collections.OrderedDict` or \
            :class:`~numpy:numpy.ndarray`

        """
        coords = self.coords
        if asdict:
            return OrderedDict(list(zip(xyz, coords.T)))
        else:
            return coords

    def rezero_coords(self, epsilon=1.0e-10):
        """Alias for :meth:`Atoms.rezero`."""
        self.rezero(epsilon=epsilon)

    def rezero_xyz(self, epsilon=1.0e-10):
        """Alias for :meth:`Atoms.rezero`."""
        self.rezero(epsilon=epsilon)

    def rezero(self, epsilon=1.0e-10):
        """Set really really small coordinates to zero.

        Set all coordinates with absolute value less than
        epsilon to zero.

        Parameters
        ----------
        epsilon : float
            smallest allowed absolute value of any :math:`x,y,z` component.

        """
        [atom.rezero(epsilon=epsilon) for atom in self]

    def rotate(self, **kwargs):
        """Rotate `Atom` position vectors.

        Parameters
        ----------
        angle : float
        axis : :class:`~sknano.core.math.Vector`, optional
        anchor_point : :class:`~sknano.core.math.Point`, optional
        rot_point : :class:`~sknano.core.math.Point`, optional
        from_vector, to_vector : :class:`~sknano.core.math.Vector`, optional
        degrees : bool, optional
        transform_matrix : :class:`~numpy:numpy.ndarray`

        """
        if kwargs.get('transform_matrix', None) is None:
            transform_matrix = transformation_matrix(**kwargs)
        [atom.rotate(transform_matrix=transform_matrix) for atom in self]

    def select(self, cmd):
        pass

    def select_within(self, volume):
        pass

    def translate(self, t, fix_anchor_points=True):
        """Translate `Atom` position vectors by :class:`Vector` `t`.

        Parameters
        ----------
        t : :class:`Vector`
        fix_anchor_points : bool, optional

        """
        [atom.translate(t, fix_anchor_point=fix_anchor_points)
         for atom in self]
