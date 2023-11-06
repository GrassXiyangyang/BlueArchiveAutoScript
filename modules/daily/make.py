import time

from fuzzywuzzy import fuzz

from modules.baas import home
from common import ocr, stage, color

make_position = {
    1: (975, 279), 2: (975, 410), 3: (975, 551)
}

priority_position = {
    1: (174, 552), 2: (303, 527), 3: (414, 473), 4: (505, 388), 5: (569, 275)
}


def start(self):
    # 回到首页
    home.go_home(self)
    # 点击制造
    self.double_click(701, 645)
    # 等待制造页面加载
    is_make_page(self)
    # 开始制造
    start_make(self)
    # 回到首页
    home.go_home(self)


def is_make_page(self):
    ocr.screenshot_check_text(self, "制造工坊", (97, 7, 224, 38))


def start_make(self):
    for i in range(self.tc['config']['count']):
        self.click(975, 264)
        # 等待加载
        ocr.screenshot_check_text(self, "全部查看", (94, 101, 184, 126))
        # 选择石头
        if not choose_tone(self):
            break
        # 点击第1阶段启动
        self.d.click(1114, 653)
        # 等待加载
        stage.wait_loading(self)
        # 等待制造页面加载
        is_make_page(self)

        # 选择物品
        choose_item(self)

        # 点击选择节点
        self.click(1121, 650)
        # 等待加载
        ocr.screenshot_check_text(self, '开始制造', (1049, 632, 1187, 670))
        # 点击开始制造
        self.d.click(1116, 652)
        time.sleep(2)
        # 等待制造页面加载
        is_make_page(self)
        # 点击立即完成
        self.d.click(1128, 278)
        # 等待确认
        ocr.screenshot_check_text(self, '确认', (732, 461, 807, 498))
        # 点击确认
        self.d.click(771, 478)
        # 点击领取
        self.click(1122, 275)
        # 关闭奖励
        stage.close_prize_info(self)
        # 冷却
        time.sleep(1)


def choose_item(self):
    time.sleep(3)
    self.d.click(445, 552)
    # 选择优先级最高物品
    check_index = get_high_priority(self)
    # 选择最高优先级物品
    self.click(*priority_position[check_index + 1])
    return check_index


def get_high_priority(self):
    # 遍历查看所有物品
    items = []
    for i, position in priority_position.items():
        self.d.click(*position)
        item = ocr.screenshot_get_text(self, (720, 204, 1134, 269))
        items.append(item)
    # 计算优先级最高的物品
    check_item = None
    check_index = 0
    for i, item in enumerate(items):
        for priority in self.tc['config']['priority']:
            ratio = fuzz.ratio(item, priority)
            if ratio < 80:
                continue
            if not check_item or \
                    self.tc['config']['priority'].index(priority) < self.tc['config']['priority'].index(check_item):
                check_item = priority
                check_index = i
    return check_index


def choose_tone(self):
    # 点击拱心石
    self.d.click(908, 199)
    # 检查是否满足
    if color.check_rgb_similar(self, (995, 631, 996, 632), (61, 219, 250)):
        return True
    # 点击拱心石碎片
    self.click(769, 200, False, 10)
    return color.check_rgb_similar(self, (995, 631, 996, 632), (61, 219, 250))
