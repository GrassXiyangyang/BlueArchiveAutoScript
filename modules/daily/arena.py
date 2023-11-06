import time

from common import ocr, color, stage
from modules.baas import home


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

    # 检测已有冷却... todo

    # 开始战斗
    fight(self)
    # 领奖
    get_prize(self)
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


def fight(self, wait=False):
    # 检查余票
    surplus = ocr.screenshot_get_text(self, (189, 475, 229, 498))
    if surplus == '0/5':
        print("没票了")
        return
    if wait:
        # 战斗等待1分钟
        time.sleep(52)
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
    # 等待结果
    ex, position = ocr.screenshot_get_position(self, '确认', (550, 439, 733, 567))  # 确认战斗结果
    if ex:
        # 确认结果
        self.click(position[1][0] + 520, position[1][1] + 455)
    for i in range(2):
        # 确认排名升级
        if ocr.screenshot_check_text(self, '确认', (555, 516, 733, 567), 5):
            # 确认结果
            self.click(646, 526)
    # 重新战斗
    fight(self, True)


def choose_enemy(self):
    less_level = self.tc['config']['less_level']
    # 识别自己等级
    my_lv = float(ocr.screenshot_get_text(self, (165, 215, 208, 250), self.ocrNum))
    refresh = 0
    while True:
        # 超出最大次数,直接开始
        if refresh > self.tc['config']['max_refresh']:
            break
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
