import time

from modules.baas import home
from common import ocr, stage

shop_position = {
    'general': (150, 150), 'arena': (150, 380)
}

goods_position = {
    1: (650, 200), 2: (805, 200), 3: (960, 200), 4: (1110, 200),
    5: (650, 460), 6: (805, 460), 7: (960, 460), 8: (1110, 460),
    9: (650, 160), 10: (805, 160), 11: (960, 160), 12: (1110, 160),
    13: (650, 420), 14: (805, 420), 15: (960, 420), 16: (1110, 420),
}


def start(self):
    # 回到首页
    home.go_home(self)
    # 点击商店
    self.double_click(821, 651)
    # 等待商店页面加载
    ocr.is_shop(self)
    # 购买商品
    buy_goods(self)
    # 回到首页
    home.go_home(self)


def buy_goods(self):
    for shop in self.tc['config']:
        if not shop['enable']:
            continue
        self.click(*shop_position[shop['shop']])
        # 检查商品是否选中
        # todo
        # 选择商品
        choose_goods(self, shop['goods'])

        if not ocr.screenshot_check_text(self, '选择购买', (1116, 645, 1213, 676), 0):
            print("没有选中道具")
            continue

        # 点击选择购买
        self.d.click(1164, 660)

        # 等待确认购买页面
        ocr.screenshot_check_text(self, '是否购买', (581, 229, 698, 264))

        # 确认购买
        self.d.click(769, 484)

        # 关闭获得奖励
        stage.close_prize_info(self, True)

        # 刷新功能 todo


def choose_goods(self, goods):
    swipe = False
    # todo 商品渲染需要时间...
    time.sleep(0.5)
    print("开始点击所需商品")
    for g in goods:
        if g > 8 and not swipe:
            swipe = True
            self.d.swipe(933, 586, 933, 230)
            self.d.swipe(933, 586, 933, 230)
            time.sleep(0.5)
        # 点击商品,防止太快点不到
        time.sleep(0.2)
        self.d.click(*goods_position[g])
