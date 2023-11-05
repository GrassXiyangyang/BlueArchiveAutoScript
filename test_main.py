import unittest

import uiautomator2 as u2
from cnocr import CnOcr
from utils import ocr
from fuzzywuzzy import fuzz


class TestMain(unittest.TestCase):

    def test_ss(self):
        self.d = u2.connect("emulator-5554")
        self.ocr = CnOcr()
        self.ocrEN = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
        self.ocrNum = CnOcr(det_model_name='number-densenet_lite_136-fc', rec_model_name='number-densenet_lite_136-fc')
        print(ocr.screenshot_get_text(self, (122, 178, 163, 208), self.ocrNum))
        ocr.check_rgb_similar(self, (700, 150, 701, 151), 0)

def test_fuzz(self):
        str1 = "POwLO8Olagooo"
        str2 = "NowLoading"
        similarity = fuzz.ratio(str1, str2)
        print(similarity)
