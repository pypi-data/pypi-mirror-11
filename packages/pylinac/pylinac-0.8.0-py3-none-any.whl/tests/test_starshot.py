import os
import os.path as osp
import unittest

import numpy as np

from pylinac.starshot import Starshot
from pylinac.core.geometry import Point
from tests.utils import save_file


test_file_dir = osp.join(osp.dirname(__file__), 'test_files', 'Starshot')


class GeneralTests(unittest.TestCase):
    """Performs general tests (not image specific)."""

    def setUp(self):
        self.star = Starshot.from_demo_image()
        self.star.analyze()

    def test_analyze_without_images(self):
        star = Starshot()
        self.assertRaises(AttributeError, star.analyze)

    def test_save_image(self):
        """Test that saving an image does something."""
        save_file('test.jpg', self.star.save_analyzed_image)

    def test_from_url(self):
        url = 'https://s3.amazonaws.com/assuranceqa-staging/uploads/imgs/10X_collimator_dvTK5Jc.jpg'
        star = Starshot.from_url(url)  # shouldn't raise


class StarMixin:
    """Mixin for testing a starshot image."""
    star_file = ''
    wobble_diameter_mm = 0
    wobble_center = Point()
    num_rad_lines = 0
    recursive = True
    passes = True
    min_peak_height = 0.25
    test_all_radii = True

    @classmethod
    def setUpClass(cls):
        cls.star = Starshot(cls.star_file)
        cls.star.analyze(recursive=cls.recursive, min_peak_height=cls.min_peak_height)

    def test_passed(self):
        """Test that the demo image passed"""
        self.star.analyze(recursive=self.recursive, min_peak_height=self.min_peak_height)
        self.assertEqual(self.star.passed, self.passes, msg="Wobble was not within tolerance")

    def test_wobble_diameter(self):
        """Test than the wobble radius is similar to what it has been shown to be)."""
        self.assertAlmostEqual(self.star.wobble.diameter_mm, self.wobble_diameter_mm, delta=0.25)

    def test_wobble_center(self):
        """Test that the center of the wobble circle is close to what it's shown to be."""
        # test y-coordinate
        y_coord = self.star.wobble.center.y
        self.assertAlmostEqual(y_coord, self.wobble_center.y, delta=3)
        # test x-coordinate
        x_coord = self.star.wobble.center.x
        self.assertAlmostEqual(x_coord, self.wobble_center.x, delta=3)

    def test_num_rad_lines(self):
        """Test than the number of radiation lines found is what is expected."""
        self.assertEqual(len(self.star.lines), self.num_rad_lines,
                         msg="The number of radiation lines found was not the number expected")

    def test_all_radii_give_same_wobble(self):
        """Test that the wobble stays roughly the same for all radii."""
        if self.test_all_radii:
            star = Starshot(self.star_file)
            for radius in np.linspace(0.9, 0.25, 8):
                star.analyze(radius=float(radius), min_peak_height=self.min_peak_height, recursive=self.recursive)
                self.assertAlmostEqual(star.wobble.diameter_mm, self.wobble_diameter_mm, delta=0.15)


class Demo(StarMixin, unittest.TestCase):
    """Specific tests for the demo image"""
    star_file = osp.join(osp.dirname(osp.dirname(__file__)), 'pylinac', 'demo_files', 'starshot', '10X_collimator.tif')
    wobble_diameter_mm = 0.3
    wobble_center = Point(1270, 1437)
    num_rad_lines = 4

    def test_fails_with_tight_tol(self):
        star = Starshot.from_demo_image()
        star.analyze(tolerance=0.1)
        self.assertFalse(star.passed)

    def test_bad_inputs_still_recovers(self):
        self.star.analyze(radius=0.3, min_peak_height=0.1)
        self.test_wobble_center()
        self.test_wobble_diameter()

    def test_demo_runs(self):
        """Test that the demo runs without error."""
        self.star.run_demo()

    def test_image_inverted(self):
        """Check that the demo image was actually inverted, as it needs to be."""
        star = Starshot.from_demo_image()
        top_left_corner_val_before = star.image.array[0,0]
        star._check_image_inversion()
        top_left_corner_val_after = star.image.array[0,0]
        self.assertNotEqual(top_left_corner_val_before, top_left_corner_val_after)

    def test_SID_can_be_overridden_for_nonEPID(self):
        self.star.analyze(SID=400)
        self.assertNotEqual(self.star.wobble.diameter, self.wobble_diameter_mm*2)

    def test_bad_start_point_recovers(self):
        """Test that even at a distance start point, the search algorithm recovers."""
        self.star.analyze(start_point=(1000, 1000))
        self.test_passed()
        self.test_wobble_center()
        self.test_wobble_diameter()


class Multiples(StarMixin, unittest.TestCase):
    """Test a starshot composed of multiple individual EPID images."""
    num_rad_lines = 9
    wobble_center = Point(254, 192)
    wobble_diameter_mm = 0.8

    @classmethod
    def setUpClass(cls):
        img_dir = osp.join(test_file_dir, 'set')
        img_files = [osp.join(img_dir, filename) for filename in os.listdir(img_dir)]
        cls.star = Starshot.from_multiple_images(img_files)
        cls.star.analyze(radius=0.6)

    def test_radius_larger_than_passed(self):
        """Test the outcome of an analysis where the passed radius is outside the edge of the radiation lines."""
        # with recursive recovers
        self.star.analyze(radius=0.9)
        self.test_passed()
        self.test_wobble_center()

    def test_all_radii_give_same_wobble(self):
        pass


class Starshot1(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#1.tif')
    wobble_center = Point(508, 683)
    wobble_diameter_mm = 0.23
    num_rad_lines = 4


class Starshot2(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#2.tif')
    wobble_center = Point(566, 590)
    wobble_diameter_mm = 0.2
    num_rad_lines = 4


class Starshot3(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#3.tif')
    wobble_center = Point(466, 595)
    wobble_diameter_mm = 0.34
    num_rad_lines = 6


class Starshot4(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#4.tif')
    wobble_center = Point(446, 565)
    wobble_diameter_mm = 0.4
    num_rad_lines = 6


class Starshot5(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#5.tif')
    wobble_center = Point(557, 580)
    wobble_diameter_mm = 0.15
    num_rad_lines = 4


class Starshot6(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#6.tif')
    wobble_center = Point(528, 607)
    wobble_diameter_mm = 0.3
    num_rad_lines = 7
    min_peak_height = 0.1
    test_all_radii = False

    def test_regular_peak_height_fails(self):
        star = Starshot(self.star_file)
        star.analyze()
        self.assertGreater(star.wobble.diameter_mm, 1)


class Starshot7(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#7.tif')
    wobble_center = Point(469, 646)
    wobble_diameter_mm = 0.25
    num_rad_lines = 4


class Starshot8(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#8.tiff')
    wobble_center = Point(686, 669)
    wobble_diameter_mm = 0.4
    num_rad_lines = 5


class Starshot9(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#9.tiff')
    wobble_center = Point(714, 611)
    wobble_diameter_mm = 0.3
    num_rad_lines = 5


class Starshot10(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#10.tiff')
    wobble_center = Point(725, 802)
    wobble_diameter_mm = 0.6
    num_rad_lines = 5


class Starshot11(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#11.tiff')
    wobble_center = Point(760, 650)
    wobble_diameter_mm = 0.6
    num_rad_lines = 4


class Starshot12(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#12.tiff')
    wobble_center = Point(315, 292)
    wobble_diameter_mm = 0.8
    num_rad_lines = 4


class Starshot13(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#13.tiff')
    wobble_center = Point(376, 303)
    wobble_diameter_mm = 0.2
    num_rad_lines = 4


class Starshot14(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#14.tiff')
    wobble_center = Point(334, 282)
    wobble_diameter_mm = 0.55
    num_rad_lines = 4


class Starshot15(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#15.tiff')
    wobble_center = Point(346, 309)
    wobble_diameter_mm = 0.6
    num_rad_lines = 4


class Starshot16(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#16.tiff')
    wobble_center = Point(1444, 1452)
    wobble_diameter_mm = 0.6
    num_rad_lines = 6
    min_peak_height = 0.6


class Starshot17(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#17.tiff')
    wobble_center = Point(1475, 1361)
    wobble_diameter_mm = 0.4
    num_rad_lines = 6


class Starshot18(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#18.tiff')
    wobble_center = Point(1516, 1214)
    wobble_diameter_mm = 0.6
    num_rad_lines = 6


class Starshot19(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#19.tiff')
    wobble_center = Point(1475, 1276)
    wobble_diameter_mm = 0.6
    num_rad_lines = 6


class Starshot20(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#20.tiff')
    wobble_center = Point(347, 328)
    wobble_diameter_mm = 0.75
    num_rad_lines = 4


class Starshot21(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#21.tiff')
    wobble_center = Point(354, 294)
    wobble_diameter_mm = 1.01
    num_rad_lines = 4
    min_peak_height = 0.1
    passes = False
    test_all_radii = False


class Starshot22(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#22.tiff')
    wobble_center = Point(1302, 1513)
    wobble_diameter_mm = 0.95
    num_rad_lines = 9

    def test_bad_input_no_recursion_fails(self):
        """Test that without recursion, a bad setup fails."""
        with self.assertRaises(RuntimeError):
            self.star.analyze(radius=0.3, min_peak_height=0.95, recursive=False)

        # but will pass with recursion
        self.star.analyze()
        self.test_passed()


class Starshot23(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#23.tiff')
    wobble_center = Point(1297, 1699)
    wobble_diameter_mm = 0.32
    num_rad_lines = 9

    def test_not_fwhm_passes(self):
        self.star.analyze(fwhm=False)
        self.test_passed()


class Starshot24(StarMixin, unittest.TestCase):
    star_file = osp.join(test_file_dir, 'Starshot#24.tiff')
    wobble_center = Point(1370, 1454)
    wobble_diameter_mm = 0.3
    num_rad_lines = 4
