import time

from modules import home
from utils import ocr

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

    # 需要购买的商品 todo
    need_goods = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    # 商品排序,防止乱填
    need_goods.sort()
    swipe = False
    time.sleep(0.5)
    print("开始点击所需商品")
    for need in need_goods:
        if need > 8 and not swipe:
            swipe = True
            self.d.swipe(933, 586, 933, 230)
            self.d.swipe(933, 586, 933, 230)
            time.sleep(0.5)
        # 判断是否能购买 太慢了...
        # if not ocr.check_rgb(self, goods_position[need], (244, 241, 239)):
        #     print("该商品已售罄")
        #     continue
        # 点击商品,防止太快点不到
        time.sleep(0.2)
        self.d.click(*goods_position[need])

    if not ocr.screenshot_check_text(self, '选择购买', (1116, 645, 1213, 676), 0):
        print("没有选中道具")
        # 返回首页
        return home.click_house(self)

    # 点击选择购买
    self.d.click(1164, 660)

    # 等待确认购买页面
    ocr.screenshot_check_text(self, '是否购买', (581, 229, 698, 264))

    # 确认购买
    self.d.click(769, 484)

    # 关闭获得奖励
    ocr.close_prize_info(self)

    # 返回首页
    home.click_house(self)
