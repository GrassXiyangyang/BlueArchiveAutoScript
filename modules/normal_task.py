import time

from modules import home, common, hard_task
from utils import ocr

normal_position = {
    1: (1120, 240), 2: (1120, 340), 3: (1120, 440), 4: (1120, 540), 5: (1120, 568),
}


def start(self):
    # 回到首页
    home.go_home(self)
    # 点击业务区
    self.double_click(1195, 576)
    # 等待业务区页面加载
    ocr.is_business(self)

    # 点击任务
    self.click(816, 285)
    # 等待加载
    ocr.screenshot_check_text(self, '选择地点', (102, 6, 225, 41))

    if self.tc['task'] == 'hard_task':
        # 点击困难
        while not ocr.check_rgb_similar(self, (1000, 150, 1001, 151), (66, 66, 198)):
            self.click(1062, 154)
    else:
        # 点击普通
        while not ocr.check_rgb_similar(self, (700, 150, 701, 151), (88, 66, 46)):
            self.click(803, 156)
    # 开始扫荡
    start_scan(self)

    # 回到首页
    home.go_home(self)


def start_scan(self):
    prev_region = None
    swipe = False
    for tk in self.tc['config']:
        # 选择区域
        choose_region(self, tk['region'])
        if self.tc['task'] == 'hard_task':
            # 点击入场
            self.click(*hard_task.hard_position[tk['stage']])
        else:
            if prev_region == tk['region'] and swipe:
                self.d.swipe(933, 230, 933, 586)
                time.sleep(0.5)
            if tk['stage'] > 4:
                self.d.swipe(933, 586, 933, 230)
                time.sleep(0.5)
            prev_region = tk['region']
            swipe = tk['stage'] > 4
            # 点击入场
            self.click(*normal_position[tk['stage']])
        # 确认扫荡
        rst = common.confirm_scan(self, tk)
        if rst == 'return':
            return
        # 关闭任务信息
        self.double_click(1236, 98)


def choose_region(self, region):
    cu_region = int(ocr.screenshot_get_text(self, (122, 178, 163, 208), self.ocrNum))
    if cu_region == region:
        return
    elif cu_region > region:
        self.click(40, 360)
    else:
        self.click(1245, 360)
    return choose_region(self, region)
