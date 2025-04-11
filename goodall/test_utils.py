from unittest import TestCase

from goodall.utils import *


class Test(TestCase):
    def test_range_include_right(self):
        values = range_include_right(0.7, 0.95, 0.05)
        self.assertEqual(6, len(values))
        # print(str(values[0]))
        self.assertEqual(3, len(str(values[0])))
        # print(str(values[5]))
        self.assertEqual(4, len(str(values[5])))
