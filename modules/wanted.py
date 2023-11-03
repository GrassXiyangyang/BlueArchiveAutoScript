from modules import home, special_entrust
from utils import ocr

entrust_position = {
    'gjgl': (950, 270), 'smtl': (950, 415), 'jt': (950, 550)
}

choose = {
    'gjgl': [[8, 2]],
    'smtl': [[8, 2]],
    'jt': [[8, 2]],
}


def start(self):
    # 回到首页
    home.go_home(self)
    # 点击业务区
    self.double_click(1195, 576)
    # 等待业务区页面加载
    ocr.is_business(self)

    # 点击悬赏通缉
    self.click(733, 472)
    # 等待加载
    ocr.screenshot_check_text(self, '讲堂', (1126, 506, 1222, 557))
    # 选择委托
    special_entrust.choose_entrust(self, 'wanted')
    # 返回首页
    home.click_house(self)
