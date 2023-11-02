import time
from iconst.emulator import *
from modules import home
from utils import ocr

school_position = {
    'sl_bus': (908, 182), 'sl_life': (908, 285), 'ghn': (908, 397), 'abds': (908, 502), 'qxn': (908, 606)
}
curse_position = {
    1: (300, 210), 2: (640, 210), 3: (990, 210),
    4: (300, 360), 5: (640, 360), 6: (990, 360),
    7: (300, 516), 8: (640, 516),
}
# todo 这里让用户选择
user_choose = {'qxn': [7, 8], 'ghn': [7, 8], 'sl_life': [5]}
user_choose = {'qxn': [1, 2, 3], 'ghn': [1], 'sl_life': [1]}


def start(self):
    # 回到首页
    home.go_home(self)
    # 点击日程
    self.double_click(212, 656)
    # 等待日程页面加载
    ocr.is_schedule(self)

    # 检查余票
    surplus = ocr.screenshot_get_text(self, (281, 89, 318, 112), True)
    if surplus == '0/5':
        print("没票了")
        # home.click_house(self)
        # return
    # 选择课程
    choose_course(self)


def choose_course(self):
    for school, course in user_choose.items():
        # 点击学院
        self.click(*school_position[school])
        # 等待页面加载
        ocr.screenshot_check_text(self, '全部日程', (1107, 646, 1222, 676), True)
        # 点击全部日程
        self.click(1166, 662)
        # 等待页面加载
        ocr.screenshot_check_text(self, '全部日程', (568, 97, 717, 132), True)
        # 学习课程
        if learn_course(self, course):
            return
        # 返回课程
        self.click(1140, 116)
        self.click(55, 36)
        # 等待日程页面加载
        ocr.is_schedule(self)
    # 返回首页
    home.click_house(self)


def learn_course(self, course):
    for c in course:
        # 检查课程是否可用
        if not ocr.check_rgb(self, curse_position[c], (255, 255, 255)):
            print("课程状态不可用")
            continue
        # 点击课程
        self.click(*curse_position[c])
        ocr.screenshot_check_text(self, '开始日程', (570, 528, 710, 565), True)
        # 点击开始日程
        self.d.click(640, 546)

        if ocr.screenshot_check_text(self, '每日入场次数已耗尽', (500, 312, 760, 350), False, 0.5):
            self.click(1233, 25, False, 3)
            home.click_house(self)
            return True

        # 等待日程报告
        while True:
            if ocr.screenshot_check_text(self, '日程报告', (579, 120, 700, 150), False):
                break
            self.click(774, 141)
            time.sleep(SS_RATE)

        # todo 截图到记录中
        # 确认日程报告
        self.d.click(640, 552)
