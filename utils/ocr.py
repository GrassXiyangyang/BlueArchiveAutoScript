import math
import os
import time
import numpy as np
import cv2
from iconst.emulator import *
from fuzzywuzzy import fuzz
import aircv as ac


def screenshot(self):
    self.d.screenshot(SS_FILE)


def wait_loading(self):
    """
    检查是否加载中，
    """
    if not os.path.exists(SS_PATH):
        os.makedirs(SS_PATH)
    ss = self.d.screenshot()
    img = ss.crop((925, 650, 1170, 685))
    img.save(SS_FILE)
    out = self.ocrEN.ocr(SS_FILE)
    text = "Now Loading"
    ex = any(map(lambda d: fuzz.ratio(d.get('text'), text) > 20, out))
    print("判断是否 为", text, "结果", ex)
    print("\t\t\t=======>>> \t\t", out)
    # 如果找到加载继续等待
    if ex:
        print("\t\t\t正在加载..............")
        time.sleep(self.bc['baas']['ss_rate'])
        return wait_loading(self)
    # 因为ba的loading会转动,可能会识别不到,所以需要连续两次判定为未加载
    # if i < 2:
    #     return wait_loading(self, i + 1)
    return True


def screenshot_get_text(self, area, ocr=None, wait=99999, i=0):
    # 检查文字前，等待加载完成
    wait_loading(self)
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


def screenshot_cut(self, area, before_wait=0):
    if before_wait > 0:
        time.sleep(before_wait)
    # 检查文字前，等待加载完成
    wait_loading(self)
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


def screenshot_check_text(self, text, area=(), wait=99999, before_wait=0):
    out = screenshot_cut(self, area, before_wait)
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


def screenshot_get_position(self, text, area=(), wait=99999, before_wait=0):
    out = screenshot_cut(self, area, before_wait)
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


def color_distance(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def check_rgb(self, area, rgb):
    """
    根据一个坐标判断rgb
    """
    area = (area[0], area[1], area[0] + 10, area[1] + 10)
    screenshot_check_text(self, '', area, 0)
    img = cv2.imread(SS_FILE)
    return np.array_equal(img[0][0], np.array(rgb))


def check_rgb_similar(self, area=(1090, 683, 1091, 684), rgb=(75, 238, 249)):
    """
    判断颜色是否相近，用来判断按钮是否可以点击
    """
    screenshot_check_text(self, '', area, 0)
    img = cv2.imread(SS_FILE)
    dist = color_distance(img[0][0], rgb)
    return dist <= 20


def close_prize_info(self):
    """
    关闭奖励道具结算页面
    """
    if screenshot_check_text(self, '点击继续', (577, 614, 704, 648), 1):
        # 关闭道具信息
        self.click(640, 635)
        time.sleep(0.5)
        return
    if screenshot_check_text(self, '因超出持有上限', (532, 282, 724, 314), 1):
        self.click(650, 501)
        return
    if screenshot_check_text(self, '以上道具的库存已满', (508, 388, 745, 419), 1):
        self.click(642, 527)
        return
    return close_prize_info(self)


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


def match_image(raw, search, threshold=0.7):
    # raw=原始图像，search=待查找的图片
    match_result = ac.find_all_template(ac.imread(raw), ac.imread(search), threshold)
    return match_result


def calc_image_mse(raw, search, threshold=200):
    raw_img = ac.imread(raw)
    search_img = ac.imread(search)
    # 如果两张图片的尺寸不同
    if raw_img.shape != search_img.shape:
        # 将待查找的图片调整为与原始图像一样的尺寸
        search_img = cv2.resize(search_img, (raw_img.shape[1], raw_img.shape[0]))
    # 计算差异值
    diff = cv2.absdiff(raw_img, search_img)
    # 计算MSE（Mean Squared Error）
    mse = np.mean(diff ** 2)
    return mse <= threshold
