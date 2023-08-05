# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

from pkg_resources import resource_filename

import nose
from nose.tools import *

import numpy as np

from sknano.core.crystallography import AlphaQuartz, DiamondStructure, \
    CaesiumChlorideStructure, RocksaltStructure, ZincblendeStructure, \
    Gold, Copper, MoS2
from sknano.generators import AlphaQuartzGenerator, \
    DiamondStructureGenerator, GoldGenerator, CopperGenerator, \
    CaesiumChlorideStructureGenerator, RocksaltStructureGenerator, \
    ZincblendeStructureGenerator, MoS2Generator
from sknano.io import XYZReader, DATAReader
from sknano.testing import GeneratorTestFixtures


class TestCase(GeneratorTestFixtures):

    def test1(self):
        quartz = AlphaQuartzGenerator()
        quartz.save()
        self.tmpdata.append(quartz.fname)
        assert_equals(quartz.atoms.Natoms, AlphaQuartz().basis.Natoms)

    def test2(self):
        quartz = AlphaQuartzGenerator(scaling_matrix=[3, 3, 3])
        quartz.save()
        self.tmpdata.append(quartz.fname)
        assert_equals(quartz.atoms.Natoms, AlphaQuartz().basis.Natoms * 3**3)

    def test3(self):
        gold = GoldGenerator()
        gold.save()
        self.tmpdata.append(gold.fname)
        assert_equals(gold.atoms.Natoms, Gold().basis.Natoms)

    def test4(self):
        gold = GoldGenerator(scaling_matrix=[5, 5, 5])
        gold.save()
        self.tmpdata.append(gold.fname)
        assert_equals(gold.atoms.Natoms, Gold().basis.Natoms * 5**3)

    def test5(self):
        copper = CopperGenerator()
        copper.save()
        self.tmpdata.append(copper.fname)
        assert_equals(copper.atoms.Natoms, Copper().basis.Natoms)

    def test6(self):
        copper = CopperGenerator(scaling_matrix=[5, 5, 5])
        copper.save()
        self.tmpdata.append(copper.fname)
        assert_equals(copper.atoms.Natoms, Copper().basis.Natoms * 5**3)

    def test7(self):
        diamond = DiamondStructureGenerator()
        diamond.save()
        self.tmpdata.append(diamond.fname)
        assert_equals(diamond.atoms.Natoms, DiamondStructure().basis.Natoms)

    def test8(self):
        diamond = DiamondStructureGenerator(scaling_matrix=[3, 3, 3])
        diamond.save()
        self.tmpdata.append(diamond.fname)
        assert_equals(diamond.atoms.Natoms,
                      DiamondStructure().basis.Natoms * 3**3)

    def test9(self):
        caesium_chloride = CaesiumChlorideStructureGenerator()
        caesium_chloride.save()
        self.tmpdata.append(caesium_chloride.fname)
        assert_equals(caesium_chloride.atoms.Natoms,
                      CaesiumChlorideStructure().basis.Natoms)

    def test10(self):
        caesium_chloride = \
            CaesiumChlorideStructureGenerator(scaling_matrix=[3, 3, 3])
        caesium_chloride.save()
        self.tmpdata.append(caesium_chloride.fname)
        assert_equals(caesium_chloride.atoms.Natoms,
                      CaesiumChlorideStructure().basis.Natoms * 3**3)

    def test11(self):
        molybdenum_disulphide = MoS2Generator()
        molybdenum_disulphide.save()
        self.tmpdata.append(molybdenum_disulphide.fname)
        assert_equals(molybdenum_disulphide.atoms.Natoms,
                      MoS2().basis.Natoms)

    def test12(self):
        molybdenum_disulphide = MoS2Generator(scaling_matrix=[3, 3, 3])
        molybdenum_disulphide.save()
        self.tmpdata.append(molybdenum_disulphide.fname)
        assert_equals(molybdenum_disulphide.atoms.Natoms,
                      MoS2().basis.Natoms * 3**3)


if __name__ == '__main__':
    nose.runmodule()
