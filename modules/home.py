import time

from utils import ocr
from iconst.emulator import *


# 回到首页
def go_home(self):
    # todo 判断游戏是否进入
    # 判断是否已经在首页
    if ocr.is_home(self, False):
        return
    # 启动游戏
    start_game(self)


def start_game(self):
    # 不在则重启应用
    self.d.app_stop(CN_BA_PKG)
    self.d.app_start(CN_BA_PKG)
    # 强制等待
    time.sleep(8)
    # 重新进入登录页面
    ocr.is_login(self)
    # 点击登录
    self.double_click(500, 500)
    # 重新判断是否进入首页
    while True:
        if ocr.is_home(self, False):
            # 关闭公告
            time.sleep(1)
            self.click(400, 40)
            break
        # 关闭签到
        self.click(661, 88)
        time.sleep(0.5)


def click_house(self):
    # 返回首页
    self.click(1236, 25)
    # 等待首页加载
    ocr.is_home(self, True)
    # 点击妹子，防止多次点击点出来菜单
    self.click(851, 262, False, 2)
