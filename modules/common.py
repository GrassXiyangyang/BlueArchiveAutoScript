from modules import home
from utils import ocr


def confirm_scan(self, tk):
    # 等关卡加载
    ocr.screenshot_check_text(self, '任务信息', (574, 122, 709, 155))
    # 扫荡指定次数
    self.click(1034, 299, False, tk['count'] - 1, 0.6)
    # 点击开始扫荡
    self.d.click(938, 403)
    # 判断困难次数
    if self.tc['task'] == 'hard_task':
        # 查看次数是否足够
        if ocr.screenshot_check_text(self, '是否恢复挑战次数', (522, 251, 729, 279), 0, 0.5):
            self.d.double_click(1236, 98)
            return 'continue'
    # 判断统计悬赏票数
    if self.tc['task'] == 'wanted':
        # 查看入场券是否足够
        if ocr.screenshot_check_text(self, '移动', (730, 485, 803, 516), 0, 0.5):
            # 下一个
            self.click(56, 38, 0, 3)
            return 'continue'
    else:
        # 查看体力是否足够
        if ocr.screenshot_check_text(self, '是否购买', (515, 227, 627, 260), 0, 0.5):
            # 关闭弹窗 返回首页
            home.go_home(self)
            return 'return'

    # 等待确认加载
    ocr.screenshot_check_text(self, '通知', (599, 144, 675, 178))
    # 确认扫荡
    self.d.click(770, 500)
    # 检查跳过,最多检查30次
    if tk['count'] >= 3:
        ocr.screenshot_check_text(self, '跳过', (600, 488, 684, 526), 30)
        # 点击跳过
        self.d.click(641, 504)
    # 等待结算
    ocr.screenshot_check_text(self, '确认', (597, 562, 680, 600))
    # 确认奖励
    self.d.click(641, 580)
    return 'nothing'
