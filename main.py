import time

import uiautomator2 as u2
from uiautomator2 import Device

from iconst.emulator import *
from cnocr import CnOcr
from modules import group, cafe, mailbox, task, schedule, shop, special_entrust, wanted, arena
from utils import ocr


class Main:
    ocr: CnOcr
    ocrEN: CnOcr
    ocrNum: CnOcr
    d: Device

    def __init__(self):
        self.d = u2.connect(EMULATOR)
        self.ocr = CnOcr()
        self.ocrEN = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
        self.ocrNum = CnOcr(det_model_name='number-densenet_lite_136-fc', rec_model_name='number-densenet_lite_136-fc')

    def click(self, x, y, wait=True, count=1, rate=0):
        if wait:
            ocr.wait_loading(self)
        for i in range(count):
            print("\t\t\n\n Click", x, y, "\n\n")
            if rate > 0:
                time.sleep(rate)
            self.d.click(x, y)

    def double_click(self, x, y, wait=True, count=1, rate=0):
        if wait:
            ocr.wait_loading(self)
        ocr.wait_loading(self)
        for i in range(count):
            print("\t\t\n\n DoubleClick", x, y, "\n\n")
            if rate > 0:
                time.sleep(rate)
            self.d.double_click(x, y)

    def dashboard(self):
        group.start(self)
        shop.start(self)
        cafe.start(self)
        schedule.start(self)
        special_entrust.start(self)
        wanted.start(self)
        arena.start(self)
        task.start(self)
        mailbox.start(self)


def main():
    Main().dashboard()


if __name__ == '__main__':
    main()
