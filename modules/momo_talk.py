import time

from modules import home
from utils import ocr


def start(self):
    # 回到首页
    home.go_home(self)

    if not ocr.check_rgb_similar(self, (183, 122, 184, 123), (1, 68, 241)):
        print("没有可以互动的学生")
        return
    # 点击桃信
    self.double_click(170, 144)
    # 等待桃信页面加载
    ocr.screenshot_check_text(self, '成员', (226, 167, 277, 189))
    # 点击短信tab
    self.click(174, 272)
    # 等短信页面加载
    ocr.screenshot_check_text(self, '未读信息', (226, 167, 321, 189))

    # 查看排序 todo

    # 查看第一个学生是否可以聊天
    if not ocr.check_rgb_similar(self, (640, 245, 641, 246), (25, 71, 251)):
        print("没人可以聊天了...")
        return

    # 点击第一个学生
    self.click(471, 251)
    # 开始聊天
    start_chat(self)
    # 关闭桃信
    self.click(1121, 125)
    # 重新桃信
    start(self)


def start_chat(self):
    self.mm_i = 0
    while self.mm_i < 6:
        # 检测回复
        ex, position = ocr.screenshot_momo_talk(self, '回复', (774, 196, 1123, 603), 0, 0)
        if ex:
            self.mm_i = 0
            reply_message(self, position)
            continue
        # 检测好感故事
        ex, position = ocr.screenshot_momo_talk(self, '好感故事', (774, 196, 1123, 603), 0, 0)
        if ex:
            self.mm_i = 0
            good_story(self, position)
            continue
        # 检查文字是否发生变动
        check_message(self)
        # 三种情况都不满足等待0.5秒
        time.sleep(0.5)


def reply_message(self, position):
    # 往回复的下方移动60px点击第一条回复
    self.click(774 + position[1][0], 196 + position[1][1] + 60)
    print("开始回复妹子")


def good_story(self, position):
    # 往回复的下方移动60px点击第一条回复
    self.click(774 + position[1][0], 196 + position[1][1] + 60)
    # 检测好感故事
    ocr.screenshot_check_text(self, '进入好感故事', (820, 545, 1017, 579))
    # 点击进入好感故事
    self.click(919, 563)
    # 等待菜单出现
    ocr.screenshot_check_text(self, '菜单', (1172, 24, 1232, 52))
    # 点击菜单
    self.click(1204, 40, False, 1, 0.5)
    # 点击跳过
    self.click(1212, 115, False, 1, 1)
    # 确认跳过
    ocr.screenshot_check_text(self, '确认', (730, 503, 807, 539))
    # 确认跳过
    self.d.click(770, 516)
    # 关闭奖励
    ocr.close_prize_info(self)


def check_message(self):
    # 检查文字是否发生变动
    out = ocr.screenshot_cut(self, (774, 196, 1123, 603))
    if len(out) == 0:
        self.mm_i += 1
        return
    latest_text = out[-1].get('text')
    if not hasattr(self, 'mm_prev') or self.mm_prev == latest_text:
        self.mm_i += 1
    self.mm_prev = latest_text
