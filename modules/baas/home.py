from common import ocr, image
from common.iconst import SS_FILE
from modules.baas import restart


def go_home(self):
    app = self.d.app_current()
    if app['package'] != self.bc['baas']['package']:
        # 启动游戏
        return restart.start(self)

    # 返回首页
    if recursion_click_house(self):
        return
    # 返回首页失败启动游戏
    restart.start(self)


def recursion_click_house(self, check_text=False, fail_count=0):
    """
    递归点击首页按钮，如果返回False则返回首页失败，反之返回首页成功
    """
    # 多次返回失败
    if fail_count >= 5:
        return False
    if ocr.screenshot_check_text(self, "认证信息已超时", (529, 295, 719, 329), 0):
        return False

    if ocr.is_home(self, 0):
        # 和妹子互动
        self.d.double_click(851, 262)
        return True

    if check_text:
        menu = ocr.screenshot_get_text(self, (97, 2, 368, 40), 0)
        if menu == "":
            self.d.click(355, 22)
            return recursion_click_house(self, False, fail_count + 1)
    # 返回首页
    self.d.double_click(1233, 11)
    # 重新检查
    return recursion_click_house(self, check_text, fail_count + 1)
