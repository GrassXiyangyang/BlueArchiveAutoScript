import uiautomator2 as u2
from uiautomator2 import Device

from iconst.emulator import *
from cnocr import CnOcr
from modules import group, cafe, mailbox, task, schedule, shop
from utils import ocr


class Main:
    ocr: CnOcr
    ocrEN: CnOcr
    d: Device

    def __init__(self):
        self.d = u2.connect(EMULATOR)
        self.ocr = CnOcr()
        self.ocrEN = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')

    def click(self, x, y, wait=True, count=1):
        if wait:
            ocr.wait_loading(self)
        for i in range(count):
            self.d.click(x, y)

    def double_click(self, x, y):
        ocr.wait_loading(self)
        self.d.double_click(x, y)

    def dashboard(self):
        group.start(self)
        shop.start(self)
        cafe.start(self)
        schedule.start(self)
        task.start(self)
        mailbox.start(self)


def main():
    Main().dashboard()


if __name__ == '__main__':
    main()
