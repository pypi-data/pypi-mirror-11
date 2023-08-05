# -*- coding: utf-8 -*-
"""
===============================================================================
Atoms class for :class:`TypeAtom`\ s (:mod:`sknano.core.atoms._type_atoms`)
===============================================================================

.. currentmodule:: sknano.core.atoms._type_atoms

"""
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
__docformat__ = 'restructuredtext en'

from operator import attrgetter

import numpy as np

from sknano.core import dedupe
from ._atoms import Atoms
from ._type_atom import TypeAtom

__all__ = ['TypeAtoms']


class TypeAtoms(Atoms):
    """An eXtended `Atoms` class.

    Sub-class of `Atoms` class, and a container class for lists of
    :class:`~sknano.core.atoms.TypeAtom` instances.

    Parameters
    ----------
    atoms : {None, sequence, `TypeAtoms`}, optional
        if not `None`, then a list of `TypeAtom` instance objects or an
        existing `TypeAtoms` instance object.

    """
    def __init__(self, atoms=None, **kwargs):

        super().__init__(atoms, **kwargs)
        self._typemap = {}

    @property
    def __atom_class__(self):
        return TypeAtom

    def sort(self, key=attrgetter('type'), reverse=False):
        super().sort(key=key, reverse=reverse)

    @property
    def types(self):
        """:class:`~numpy:numpy.ndarray`  of :attr:`TypeAtom.type`\ s.

        .. versionchanged:: 0.3.11

           Returns an :class:`~numpy:numpy.ndarray` of
           :attr:`TypeAtom.type`\ s instead of a :class:`~python:dict`
           of type mapping. The :class:`~python:dict` of type
           mappings is now assigned to the :attr:`~TypeAtoms.typemap`
           attribute.

        """
        return np.asarray([atom.type for atom in self])

    @property
    def atomtypes(self):
        """Alias for :attr:`~TypeAtoms.types`."""
        return self.types

    @property
    def Ntypes(self):
        """Number of unique :attr:`~TypeAtoms.types`."""
        return len(list(self.typemap.keys()))

    @property
    def typemap(self):
        """:class:`python:dict` of :attr:`TypeAtom.type`\ s.

        .. versionadded:: 0.3.11

        """
        self._update_typemap()
        return self._typemap

    def _update_typemap(self):
        [self.add_type(atom) for atom in self]

    def add_type(self, atom):
        """Add atom type to :attr:`~TypeAtoms.typemap`.

        Parameters
        ----------
        atom : :class:`~sknano.core.atoms.TypeAtom`
            A :class:`~sknano.core.atoms.TypeAtom` instance.

        """
        self._typemap[atom.type] = {}
        self._typemap[atom.type]['mass'] = atom.mass

    def add_atomtype(self, atom):
        """Alias for :meth:`~TypeAtoms.add_type`."""
        self.add_type(atom)

    def add_types(self, atoms=None):
        """Add atom type for each atom in atoms to :attr:`TypeAtom.typemap` \
            dictionary.

        Parameters
        ----------
        atoms : sequence
            a list of `Atom` object instances

        """
        try:
            [self.add_type(atom) for atom in atoms]
        except TypeError:
            print('Expected an iterable sequence of `Atom` objects.')

    def add_atomtypes(self, atoms=None):
        """Alias for :meth:`~TypeAtoms.add_types`."""
        self.add_types(atoms=atoms)

    def assign_unique_types(self, from_attr='element'):
        """Assign unique :attr:`TypeAtom.type`\s to each `TypeAtom` in \
            `TypeAtoms` from an existing unique atom attribute.

        .. versionchanged:: 0.3.11

           Now accepts a keyword argument `from_attr`.

        The assignment of unique :attr:`TypeAtom.type`\s is performed
        by mapping an existing atom attribute (default: element)
        to a unique integer, starting at 1.

        Parameters
        ----------
        from_attr : :class:`~python:str`
            An existing atom attribute used to generate an attribute
            mapping that maps the attribute to a unique atom
            :attr:`~TypeAtom.type`.

        """
        attrlist = [getattr(atom, from_attr) for atom in self]
        attrmap = \
            {attr: i for i, attr in enumerate(dedupe(attrlist), start=1)}
        self.mapatomattr(from_attr, 'type', attrmap)

    def get_types(self, asdict=False):
        """Return list of `TypeAtom` :attr:`TypeAtom.type`\ s.

        Parameters
        ----------
        asdict : :class:`python:bool`, optional

        Returns
        -------
        :class:`python:list` if `asdict` is `False`
        :class:`python:dict` if `asdict` is `True`

        """
        if asdict:
            return self.typemap
        else:
            return self.types.tolist()

    def get_atomtypes(self, asdict=False):
        """Alias for :meth:`~TypeAtoms.get_types`."""
        return self.get_types(asdict=asdict)
