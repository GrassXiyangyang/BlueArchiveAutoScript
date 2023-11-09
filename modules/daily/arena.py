import time

from common import ocr, color, stage, image, iconst
from modules.baas import home

finish_seconds = 55


def start(self):
    # 回到首页
    home.go_home(self)
    # 点击业务区
    self.double_click(1195, 576)
    # 等待业务区页面加载
    ocr.is_business(self)

    # 点击战术对抗赛
    self.click(1093, 524)
    # 等待加载
    ocr.screenshot_check_text(self, '战术对抗赛', (102, 6, 248, 41))

    # 开始战斗
    start_fight(self)

    # 回到首页
    home.go_home(self)


def get_prize(self):
    if color.check_rgb_similar(self, (320, 400, 321, 401)):
        # 领取时间奖励
        self.click(353, 385)
        # 关闭奖励
        stage.close_prize_info(self)
    if color.check_rgb_similar(self, (330, 480, 331, 481)):
        # 领取挑战奖励
        self.click(348, 465)
        # 关闭奖励
        stage.close_prize_info(self)


def start_fight(self, wait=False):
    # 检查余票
    surplus = ocr.screenshot_get_text(self, (189, 475, 229, 498))
    if surplus == '0/5':
        print("没票了")
        get_prize(self)
        return True
    # 检测已有冷却
    if wait or not image.compare_image(self, (153, 516, 212, 535), 'jjc_wait_time', 0, False):
        self.finish_seconds = finish_seconds
        return False
    # 选择对手
    choose_enemy(self)
    # 编队
    self.click(640, 570, True, 1, 0.5)
    # 等待出击加载
    ocr.screenshot_check_text(self, '出击', (1134, 650, 1207, 683))
    # 角色加载太慢了... 暂时没有好办法 todo 吧
    time.sleep(3)
    # 出击
    self.double_click(1175, 665, True, 1, 1)
    while True:
        # 检查有没有出现ID
        if image.compare_image(self, (476, 424, 496, 442), 'jjc_id', 0, False):
            break
        # 关闭弹窗
        self.d.click(1235, 82)
        time.sleep(self.bc['baas']['ss_rate'])
    start_fight(self, True)


def choose_enemy(self):
    less_level = self.tc['config']['less_level']
    # 识别自己等级
    my_lv = float(ocr.screenshot_get_text(self, (165, 215, 208, 250), self.ocrNum))
    refresh = 0
    while True:
        # 超出最大次数,敌人预期等级-1
        if refresh > self.tc['config']['max_refresh']:
            less_level -= 1
            continue
        # 识别对手等级
        enemy_lv = float(ocr.screenshot_get_text(self, (551, 298, 581, 317), self.ocrNum))
        print("对手等级 ", enemy_lv)
        if enemy_lv + less_level <= my_lv:
            break
        # 更换对手
        self.double_click(1158, 145)
        refresh += 1
    # 选择对手
    self.click(769, 251)
