import os
import time
from fuzzywuzzy import fuzz
from common import stage
from common.iconst import *


def screenshot(self):
    self.d.screenshot(SS_FILE)


def screenshot_get_text(self, area, ocr=None, wait=99999, i=0):
    # 检查文字前，等待加载完成
    stage.wait_loading(self)
    if not os.path.exists(SS_PATH):
        os.makedirs(SS_PATH)
    img = self.d.screenshot().crop(area)
    img.save(SS_FILE)
    if ocr is None:
        out = self.ocr.ocr(SS_FILE)
    else:
        out = ocr.ocr(SS_FILE)
    if len(out) == 0 and wait > 0:
        return screenshot_get_text(self, area, ocr, wait)
    if len(out) == 0:
        return ''
    return out[i]['text']


def screenshot_cut(self, area, before_wait=0, need_loading=True):
    if before_wait > 0:
        time.sleep(before_wait)
    # 检查文字前，等待加载完成
    if need_loading:
        stage.wait_loading(self)
    # 创建目录
    if not os.path.exists(SS_PATH):
        os.makedirs(SS_PATH)
    if len(area) == 0:
        self.d.screenshot(SS_FILE)
    else:
        ss = self.d.screenshot()
        img = ss.crop(area)
        img.save(SS_FILE)
    return self.ocr.ocr(SS_FILE)


def screenshot_check_text(self, text, area=(), wait=99999, before_wait=0, need_loading=True):
    out = screenshot_cut(self, area, before_wait, need_loading)
    ex = any(map(lambda d: fuzz.ratio(d.get('text'), text) > 60, out))
    print("判断是否 为", text, "结果", ex)
    print("\t\t\t", out)
    # 如果已经找到 或 不需要等待直接返回结果
    if ex or wait == 0:
        return ex
    time.sleep(self.bc['baas']['ss_rate'])
    if wait < 99999:
        wait -= 1
    return screenshot_check_text(self, text, area, wait)


def screenshot_get_position(self, text, area=(), wait=99999, before_wait=0, need_loading=True):
    out = screenshot_cut(self, area, before_wait, need_loading)
    print("\t\t\t", out)
    for t in out:
        if fuzz.ratio(t.get('text'), text) <= 60:
            continue
        print("判断是否 为", text, "结果", True)
        return True, t.get('position')
    print("判断是否 为", text, "结果", False)
    # 不需要等待直接返回结果
    if wait == 0:
        return False, ()
    time.sleep(self.bc['baas']['ss_rate'])
    if wait < 99999:
        wait -= 1
    return screenshot_get_position(self, text, area, wait)


def is_home(self, wait=99999):
    return screenshot_check_text(self, "咖啡厅", (60, 676, 122, 695), wait)


def is_login(self):
    return screenshot_check_text(self, "菜单", (35, 625, 75, 650))


def is_group(self):
    return screenshot_check_text(self, "小组大厅", (97, 7, 220, 41))


def is_mailbox(self):
    return screenshot_check_text(self, "邮箱", (97, 7, 220, 41))


def is_task(self):
    return screenshot_check_text(self, "工作任务", (97, 7, 225, 41))


def is_shop(self):
    return screenshot_check_text(self, "商店", (97, 7, 163, 41))


def is_schedule(self):
    return screenshot_check_text(self, "日程", (97, 7, 165, 41))


def is_business(self):
    return screenshot_check_text(self, "业务区", (97, 7, 199, 41))


def is_cafe(self):
    return screenshot_check_text(self, "咖啡厅", (213, 7, 300, 41))
