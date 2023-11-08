from common import ocr
import os
import time
from fuzzywuzzy import fuzz

from common.iconst import SS_PATH, SS_FILE
from modules.baas import home


def confirm_scan(self, tk):
    # 等关卡加载
    ocr.screenshot_check_text(self, '任务信息', (574, 122, 709, 155))
    # 扫荡指定次数
    self.click(1034, 299, False, tk['count'] - 1, 0.6)
    # 点击开始扫荡
    self.d.click(938, 403)
    # 判断困难次数
    if self.tc['task'] == 'hard_task':
        # 查看次数是否足够
        if ocr.screenshot_check_text(self, '是否恢复挑战次数', (522, 251, 729, 279), 0, 0.5):
            self.d.double_click(1236, 98)
            return 'continue'
    # 判断统计悬赏票数
    if self.tc['task'] == 'wanted':
        # 查看入场券是否足够
        if ocr.screenshot_check_text(self, '移动', (730, 485, 803, 516), 0, 0.5):
            # 下一个
            self.click(56, 38, 0, 3)
            return 'continue'
    else:
        # 查看体力是否足够
        if ocr.screenshot_check_text(self, '是否购买', (515, 227, 627, 260), 0, 0.5):
            # 关闭弹窗 返回首页
            home.go_home(self)
            return 'return'

    # 等待确认加载
    ocr.screenshot_check_text(self, '通知', (599, 144, 675, 178))
    # 确认扫荡
    self.d.click(770, 500)
    # 检查跳过,最多检查30次
    if tk['count'] >= 3:
        ocr.screenshot_check_text(self, '跳过', (600, 488, 684, 526), 30)
        # 点击跳过
        self.d.click(641, 504)
    # 等待结算,这里很有可能会升级点击关闭升级弹窗
    while not ocr.screenshot_check_text(self, '确认', (597, 562, 680, 600), 0):
        self.d.click(850, 582)
        time.sleep(1)
    # 确认奖励
    self.d.click(641, 580)
    return 'nothing'


def close_prize_info(self, ap_check=False, mail_check=False):
    """
    关闭奖励道具结算页面
    """
    if ocr.screenshot_check_text(self, '点击继续', (577, 614, 704, 648), 1):
        # 关闭道具信息
        self.click(640, 635)
        time.sleep(0.5)
        return
    if ap_check and ocr.screenshot_check_text(self, '因超出持有上限', (532, 282, 724, 314), 1):
        self.click(650, 501)
        return
    if mail_check and ocr.screenshot_check_text(self, '以上道具的库存已满', (508, 388, 745, 419), 1):
        self.click(642, 527)
        return
    return close_prize_info(self, ap_check, mail_check)


def wait_loading(self, i=0):
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
    if i < 1:
        return wait_loading(self, i + 1)
    return True
