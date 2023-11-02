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
		self.ocrEN = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
		screenshot_check_text(self, "沙勒附属咖啡厅", (1218, 5, 1253, 40), False)
		print(111)

	def test_fuzz(self):
		str1 = "POwLO8Olagooo"
		str2 = "NowLoading"
		similarity = fuzz.ratio(str1, str2)
		print(similarity)
