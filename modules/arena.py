import time

from modules import home
from utils import ocr

# 策略1: 随便打
# 策略2: 打等级比我低N级
# choose = [1, 0]
choose = [2, 10]


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
    fight(self)

    if ocr.check_rgb_similar(self, (320, 400, 321, 401)):
        # 领取时间奖励
        self.click(353, 385)
        # 关闭奖励
        ocr.close_prize_info(self)
    if ocr.check_rgb_similar(self, (330, 480, 331, 481)):
        # 领取挑战奖励
        self.click(348, 465)
        # 关闭奖励
        ocr.close_prize_info(self)

    # 返回首页
    home.click_house(self)


def fight(self, wait=False):
    # 检查余票
    surplus = ocr.screenshot_get_text(self, (189, 475, 229, 498))
    if surplus == '0/5':
        print("没票了")
        return
    if wait:
        # 战斗等待1分钟
        time.sleep(55)
    # 选择对手
    choose_enemy(self)
    # 编队
    self.click(640, 570, True, 1, 0.5)
    # 等待出击加载
    ocr.screenshot_check_text(self, '出击', (1134, 650, 1207, 683))
    # 出击
    self.double_click(1175, 665, True, 1, 1)
    # 等待结果
    ocr.screenshot_check_text(self, '确认', (555, 516, 733, 567))  # 确认战斗结果
    # 确认结果
    self.d.click(646, 526)
    for i in range(2):
        # 确认排名升级
        if ocr.screenshot_check_text(self, '确认', (555, 516, 733, 567), 5):
            # 确认结果
            self.d.click(646, 526)
    # 重新战斗
    fight(self, True)


def choose_enemy(self):
    # 策略1: 随便打
    if choose[0] == 1:
        # 选择对手
        self.click(769, 251)
        return
    # 策略2: 打等级比我低N级
    if choose[0] == 2:
        # 识别自己等级
        my_lv = float(ocr.screenshot_get_text(self, (165, 215, 208, 250), self.ocrNum))
        while True:
            # 识别对手等级
            enemy_lv = float(ocr.screenshot_get_text(self, (551, 298, 581, 317), self.ocrNum))
            print("对手等级 ", enemy_lv)
            if enemy_lv + choose[1] <= my_lv:
                break
            # 更换对手
            self.click(1158, 145)
        # 选择对手
        self.click(769, 251)
