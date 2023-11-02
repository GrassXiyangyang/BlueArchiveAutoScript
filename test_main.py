import unittest

import uiautomator2 as u2
from iconst.emulator import *
from cnocr import CnOcr
from utils.ocr import screenshot_check_text
from fuzzywuzzy import fuzz


class TestMain(unittest.TestCase):

    def test_ss(self):
        self.d = u2.connect(EMULATOR)
        self.ocr = CnOcr()
        screenshot_check_text(self, "沙勒附属咖啡厅", (577, 614, 704, 648), False)
        print(111)

    def test_fuzz(self):
        str1 = "POwLO8Olagooo"
        str2 = "NowLoading"
        similarity = fuzz.ratio(str1, str2)
        print(similarity)
