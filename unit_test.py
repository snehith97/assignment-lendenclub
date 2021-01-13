import unittest
from ocr_main import *

class test(unittest.TestCase):

    def test_angle(self):
        img = "6.jpg"
        ang = angle.angle(img)
        self.assertTrue(ang is not None, "Angle is none")
        self.assertEqual(int(ang), 0 , "Angle is not equal to zero")

    def test_flash(self):
        img = "7.jpg"
        flh = flash.flash(img)
        self.assertTrue(flh is not None, "Flash is none")
        self.assertEqual(int(flh), 5 , "Flash is not equal to 5")