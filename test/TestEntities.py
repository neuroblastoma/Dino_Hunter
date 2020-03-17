import unittest
import os
import pygame
import mock
from Dino_Hunter import *


class TestEntity(unittest.TestCase):
    @mock.patch('Dino_Hunter.os.path.abspath')
    def setUp(self, mock_abspath):
        path = os.path.normpath("../images")
        path = os.path.join(os.path.curdir, path)
        mock_abspath.return_value = path

        pygame.init()
        screen_width = 1500
        screen_height = 750
        game = ControlManager(caption="Dino Hunter", screen_width=screen_width, screen_height=screen_height)

    def test__init__(self):
        pass


class TestEnemy(unittest.TestCase):
    def test__init__(self):
        with self.assertRaises(TypeError):
            enemy = Enemy()


class TestTRex(unittest.TestCase):
    @mock.patch('Dino_Hunter.os.path.abspath')
    def test__init__(self, mock_abspath):
        # Wrong abs directory raises System Exit
        with self.assertRaises(SystemExit):
            trex = TRex(0, 0)

        self.assertTrue(mock_abspath.called)
        path = os.path.normpath("../images")
        path = os.path.join(os.path.curdir, path)
        mock_abspath.return_value = path

        # Screen width must be > 121
        with self.assertRaises(ValueError):
            trex = TRex(0, 0)

        # Negative dimensions
        with self.assertRaises(ValueError):
            raptor = TRex(-1, -1)

        trex = TRex(2000, 2000)


class TestRaptor(unittest.TestCase):
    @mock.patch('Dino_Hunter.os.path.abspath')
    def test__init__(self, mock_abspath):
        # Wrong abs directory raises System Exit
        with self.assertRaises(SystemExit):
            raptor = Raptor(0, 0)

        self.assertTrue(mock_abspath.called)
        path = os.path.normpath("../images")
        path = os.path.join(os.path.curdir, path)
        mock_abspath.return_value = path

        # Screen width must be > 121
        with self.assertRaises(ValueError):
            raptor = Raptor(0, 0)

        # Negative dimensions
        with self.assertRaises(ValueError):
            raptor = Raptor(-1, -1)

        raptor = Raptor(2000, 2000)


class TestPtero(unittest.TestCase):
    @mock.patch('Dino_Hunter.os.path.abspath')
    def test__init__(self, mock_abspath):
        # Wrong abs directory raises System Exit
        with self.assertRaises(SystemExit):
            ptero = Ptero(0, 0)

        self.assertTrue(mock_abspath.called)
        path = os.path.normpath("../images")
        path = os.path.join(os.path.curdir, path)
        mock_abspath.return_value = path

        # Screen width must be > 121
        with self.assertRaises(ValueError):
            ptero = Ptero(0, 0)

        # Negative dimensions
        with self.assertRaises(ValueError):
            pteor = Ptero(-1, -1)

        ptero = Ptero(2000, 2000)

class TestPlayer(unittest.TestCase):
    @mock.patch('Dino_Hunter.os.path.abspath')
    def test__init__(self, mock_abspath):
        with self.assertRaises(SystemExit):
            player = Player(0)

        self.assertTrue(mock_abspath.called)
        path = os.path.normpath("../images")
        path = os.path.join(os.path.curdir, path)
        mock_abspath.return_value = path

        with self.assertRaises(TypeError):
            player = Player()

        player = Player(2000)
