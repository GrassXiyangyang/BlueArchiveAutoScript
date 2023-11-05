import time
from modules import home
from utils import ocr

schedule_position = {
    'sl_bus': (908, 182), 'sl_life': (908, 285), 'ghn': (908, 397), 'abds': (908, 502), 'qxn': (908, 606)
}
curse_position = {
    1: (300, 210), 2: (640, 210), 3: (990, 210),
    4: (300, 360), 5: (640, 360), 6: (990, 360),
    7: (300, 516), 8: (640, 516),
}


def start(self):
    # 回到首页
    home.go_home(self)
    # 点击日程
    self.double_click(212, 656)
    # 等待日程页面加载
    ocr.is_schedule(self)

    # 检查余票
    surplus = ocr.screenshot_get_text(self, (281, 89, 318, 112))
    if surplus == '0/5':
        print("没票了")
        # home.click_house(self)
        # return
    # 选择课程
    choose_course(self)


def choose_course(self):
    for tk in self.tc['config']:
        # 点击学院
        self.click(*schedule_position[tk['schedule']])
        # 等待页面加载
        ocr.screenshot_check_text(self, '全部日程', (1107, 646, 1222, 676))
        # 点击全部日程
        self.click(1166, 662)
        # 学习课程
        if learn_course(self, tk['stage']):
            return
        # 返回课程
        self.click(1140, 116)
        time.sleep(1)
        self.click(55, 36)
        # 等待日程页面加载
        ocr.is_schedule(self)
    # 回到首页
    home.go_home(self)


def learn_course(self, courses):
    for c in courses:
        # 等待页面加载
        ocr.screenshot_check_text(self, '全部日程', (568, 97, 717, 132))
        # 检查课程是否可用
        if not ocr.check_rgb(self, curse_position[c], (255, 255, 255)):
            print("课程状态不可用")
            continue
        # 点击课程
        self.click(*curse_position[c])
        ocr.screenshot_check_text(self, '开始日程', (570, 528, 710, 565))
        # 点击开始日程
        self.d.click(640, 546)

        if ocr.screenshot_check_text(self, '每日入场次数已耗尽', (500, 312, 760, 350), 0, 0.5):
            self.click(1233, 25, False, 3)
            home.go_home(self)
            return True

        # 等待日程报告
        while True:
            if ocr.screenshot_check_text(self, '日程报告', (579, 120, 700, 150), 0):
                break
            self.click(774, 141)
            time.sleep(self.bc['baas']['ss_rate'])

        # todo 截图到记录中
        # 确认日程报告
        self.d.click(640, 552)
        time.sleep(1)
