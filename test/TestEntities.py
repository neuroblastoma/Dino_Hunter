import unittest
from Dino_Hunter import *


class TestEntity(unittest.TestCase):
    def setUp(self):
        pass

    def test__init__(self):
        pass


class TestEnemy(unittest.TestCase):
    def test__init__(self):
        with self.assertRaises(TypeError):
            enemy = Enemy()

class TestTRex(unittest.TestCase):
    def test__init__(self):
        trex = TRex(0, 0, spritesheet="../../images/trex-sheet.png")