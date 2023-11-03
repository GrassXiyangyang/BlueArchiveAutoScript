import time

from utils import ocr
from iconst.emulator import *


# 回到首页
def go_home(self):
    app = self.d.app_current()
    if app['package'] != CN_BA_PKG:
        # 启动游戏
        return start_game(self)

    # 返回首页
    if recursion_click_house(self):
        return
    # 返回首页失败启动游戏
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
        if ocr.is_home(self, 0):
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
    ocr.is_home(self)
    # 点击妹子，防止多次点击点出来菜单
    self.click(851, 262, False, 2)


def recursion_click_house(self, check_text=False):
    """
    递归点击首页按钮，如果返回False则返回首页失败，反之返回首页成功
    """
    if ocr.screenshot_check_text(self, "认证信息已超时", (529, 295, 719, 329), 0):
        return False

    if ocr.is_home(self, 0):
        return True

    if check_text:
        menu = ocr.screenshot_get_text(self, (97, 2, 368, 40), False)
        if menu == "":
            self.d.click(355, 22)
            return recursion_click_house(self, False)

    # 查看是否有首页按钮
    path = SS_PATH + SS_FILE
    ss = self.d.screenshot()
    img = ss.crop((1218, 5, 1253, 40))
    img.save(path)
    if not ocr.calc_image_mse(path, HOUSE_FILE):
        return False
    # 返回首页
    self.click(1236, 25)
    # 重新检查
    time.sleep(1)
    return recursion_click_house(self)
