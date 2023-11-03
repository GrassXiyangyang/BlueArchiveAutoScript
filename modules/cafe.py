import time
from iconst.emulator import *

from main import Main
from modules import home
from utils import ocr
from PIL import Image, ImageEnhance


def start(self: Main):
    # 初始化窗口
    init_window(self)
    # 领取收益
    get_cafe_money(self)
    # 邀请妹子
    invite_girl(self)
    # 和妹子互动
    i = 5
    while i > 0:
        click_girl2(self, i)
        if ocr.screenshot_check_text(self, '好感等级提升', (473, 593, 757, 644), 3):
            # 关闭好感窗口
            self.d.click(651, 285)
            continue
        i -= 1
    # 返回首页
    home.click_house(self)


def init_window(self):
    # 回到首页
    home.go_home(self)
    # 点击咖啡厅
    self.double_click(89, 653)
    # 等待进入咖啡厅
    ocr.is_cafe(self)
    # 关闭到访成员
    self.click(919, 186)
    # 双指捏合
    sx1, sy1 = 1000, 330
    sx2, sy2 = 800, 330
    ex1, ey1 = 150, 330
    ex2, ey2 = 150, 330
    self.d().gesture((sx1, sy1), (sx2, sy2), (ex1, ey1), (ex2, ey2))
    # 拖到最左边
    self.d.swipe(392, 564, 983, 82)


def invite_girl(self):
    if not ocr.screenshot_check_text(self, "可以使用", (801, 586, 875, 606), 0):
        return
    # 点击邀请券
    self.click(830, 640)
    # 等待加载邀请
    ocr.screenshot_check_text(self, "邀请", (760, 200, 815, 236))
    # 邀请第一个
    self.click(787, 221)
    # 等待确认加载
    ocr.screenshot_check_text(self, "确认", (727, 480, 805, 519))
    # 点击确认
    self.click(770, 500)
    # 强制等待发消息邀请妹子
    time.sleep(2)


def get_cafe_money(self):
    # 查看收益
    surplus = float(ocr.screenshot_get_text(self, (1095, 641, 1160, 671)))
    if surplus == 0:
        return
    # 点击咖啡厅收益
    self.click(1155, 645)
    # 等待领取
    ocr.screenshot_check_text(self, "领取", (600, 500, 678, 538))
    # 点击领取
    self.click(641, 516)
    # 关闭获得奖励
    ocr.close_prize_info(self)
    # 关闭领取界面
    self.d.click(903, 155)


def click_girl(self: Main):
    # 定义四个坐标点
    left_top = (12, 301)
    right_top = (773, 103)
    right_bottom = (1264, 360)
    left_bottom = (487, 579)

    # 确定矩形区域的边界
    xmin = min(left_top[0], right_top[0], right_bottom[0], left_bottom[0])
    xmax = max(left_top[0], right_top[0], right_bottom[0], left_bottom[0])
    ymin = min(left_top[1], right_top[1], right_bottom[1], left_bottom[1])
    ymax = max(left_top[1], right_top[1], right_bottom[1], left_bottom[1])

    # 每隔20个像素单位进行一次点击操作
    for y in range(ymin, ymax + 1, 50):  # 先遍历y坐标
        for x in range(xmin, xmax + 1, 50):  # 再遍历x坐标
            if y < 160 or y > 570:
                continue
            self.d.click(x, y)


# # 每隔20个像素单位进行一次点击操作
# for x in range(xmin, xmax + 1, 50):
#     for y in range(ymin, ymax + 1, 50):
#         if y < 160 or y > 570:
#             continue
#         time.sleep(0.01)
#         self.click(x, y)


def click_girl2(self: Main, i):
    if i % 2 == 0:
        self.d.swipe(327, 512, 1027, 125)
    else:
        self.d.swipe(1008, 516, 300, 150)

    ocr.screenshot(self)
    path = SS_PATH + SS_FILE

    # 创建一个增强器对象，用于调整饱和度
    enhancer = ImageEnhance.Color(Image.open(path))
    # 控制饱和度，0.0 代表完全不饱和（即纯黑白），1.0 保持不变
    factor = 999  # 增加或减少饱和度的量，你可以根据需要调整这个值
    img_enhanced = enhancer.enhance(factor)
    img_enhanced.save(path)

    # img_edges = Image.open(path).filter(ImageFilter.FIND_EDGES)
    #
    # # 转换为灰度图
    # img_gray = img_edges.convert('L')
    #
    # # 应用二值化阈值
    # threshold = 200  # 阈值范围在 0（全黑）到 255（全白），你可以根据需要调整
    # bin_img = img_gray.point(lambda p: p > threshold and 255)
    # bin_img.save(path)

    # 保存处理后的图片

    result = ocr.match_image(path, GIRL_FILE, 0.1)
    for r in result:
        x = r['result'][0]
        y = r['result'][1]
        # 防止溢出到功能按钮
        if y < 160 or y > 570:
            continue
        print("点击了", x, y)
        self.d.click(x, y)
