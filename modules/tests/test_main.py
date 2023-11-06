import unittest
import uiautomator2 as u2
from cnocr import CnOcr
from common import ocr


class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.d = u2.connect("emulator-5554")
        self.ocr = CnOcr()
        self.ocrEN = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
        self.ocrNum = CnOcr(det_model_name='number-densenet_lite_136-fc', rec_model_name='number-densenet_lite_136-fc')

    def test_ss(self):
        # print(ocr.screenshot_check_text(self, '制造工坊', (1049, 632, 1187, 670)), 0)
        print(ocr.screenshot_check_text(self, '', (326, 656, 366, 677)))
        # print(color.check_rgb_similar(self, (1022, 634, 1023, 635), (61, 219, 250)))
        # ocr.check_rgb_similar(self, (700, 150, 701, 151), 0)
