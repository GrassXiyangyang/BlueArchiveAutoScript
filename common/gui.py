from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QListWidget, QStackedWidget
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QHBoxLayout

from PySide6.QtCore import QSize, Qt, QFile, QTimer

from common import config

menu_list = [
    {
        'text': 'Baas',
        'child': [
            {
                'name': 'home',
                'text': '总览',
                'page': 'home.ui',
                'height': 200
            },
            {
                'name': 'baas',
                'text': 'Baas设置',
                'page': 'baas.ui',
                'height': 800,
            },
            {
                'name': 'restart',
                'text': '重启设置',
                'page': 'restart.ui',
                'height': 200
            }
        ]
    },
    {
        'text': '每日',
        'child': [
            {
                'name': 'cafe',
                'text': '咖啡厅',
                'page': 'baas.ui',
                'height': 200
            },
            {
                'name': 'cafe',
                'text': '竞技场',
                'page': 'restart.ui',
                'height': 200
            },
            {
                'name': 'cafe',
                'text': '小组',
                'page': 'restart.ui',
                'height': 200
            },
            {
                'name': 'cafe',
                'text': '制造',
                'page': 'restart.ui',
                'height': 200
            },
            {
                'name': 'cafe',
                'text': '日程',
                'page': 'restart.ui',
                'height': 200
            },
            {
                'name': 'cafe',
                'text': '商店购买',
                'page': 'restart.ui',
                'height': 200
            },
            {
                'name': 'cafe',
                'text': '特殊委托',
                'page': 'restart.ui',
                'height': 200
            },
            {
                'name': 'cafe',
                'text': '统计悬赏',
                'page': 'restart.ui',
                'height': 200
            }
        ]
    }
]


class Gui:
    def init_app(self):
        self.setWindowTitle('Baas助手 - ' + config.get_config(self))
        with open('./gui/qss/main4.qss', 'r') as f:  # 导入QListWidget的qss样式
            self.list_style = f.read()
        with open('./gui/qss/sub_menu.qss', 'r') as f:  # 导入QListWidget的qss样式
            self.sub_menu_style = f.read()
        self.main_layout = QHBoxLayout(self, spacing=0)  # 窗口的整体布局
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_menu = QListWidget()  # 左侧选项列表
        self.main_menu.setStyleSheet(self.list_style)
        self.sub_menu = QListWidget()  # 左侧选项列表
        self.sub_menu.setStyleSheet(self.sub_menu_style)
        self.main_layout.addWidget(self.main_menu)
        self.main_layout.addWidget(self.sub_menu)
        self.right_widget = QStackedWidget()
        self.running = False

        # 创建一个QScrollArea实例
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)  # 如果你想让你的小部件能够调整大小，则设置为True
        # 把你的right_widget设置为滚动区域的小部件
        scroll.setWidget(self.right_widget)
        # 将滚动区域添加到布局中，而不是直接添加right_widget
        self.main_layout.addWidget(scroll)
        self.init_menu()

    def init_menu(self):
        self.main_menu.currentRowChanged.connect(self.right_widget.setCurrentIndex)  # list和右侧窗口的index对应绑定
        self.main_menu.setFrameShape(QListWidget.NoFrame)  # 去掉边框
        self.main_menu.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        self.main_menu.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sub_menu.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        self.sub_menu.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 创建一个映射，存储每个主菜单项和其对应的子菜单项
        self.sub_menus = {}

        for i, menu in enumerate(menu_list):
            self.item = QListWidgetItem(menu['text'], self.main_menu)  # 左侧选项的添加
            self.item.setSizeHint(QSize(30, 60))
            self.item.setTextAlignment(Qt.AlignCenter)  # 居中显示
            self.item.setData(1, menu['text'])
            if i == 0:
                self.item.setSelected(True)

            # 存储子菜单项列表
            self.sub_menus[menu['text']] = []

            for child in menu['child']:
                sub_item = QListWidgetItem(child['text'], self.sub_menu)  # 添加子菜单
                sub_item.setSizeHint(QSize(20, 50))
                sub_item.setTextAlignment(Qt.AlignCenter)  # 居中显示
                sub_item.setHidden(i != 0)  # 默认隐藏子菜单
                sub_item.setData(3, child)
                self.sub_menus[menu['text']].append(sub_item)  # 添加到对应的主菜单项列表
        # 连接信号和槽
        self.main_menu.itemClicked.connect(self.expand_sub_menu)
        self.sub_menu.itemClicked.connect(self.show_sub_menu_page)

    def load_ui_file(self, file_name):
        loader = QUiLoader()
        ui_file = QFile(file_name)
        ui_file.open(QFile.ReadOnly)
        widget = loader.load(ui_file)
        ui_file.close()
        return widget

    def expand_sub_menu(self, item: QListWidgetItem):
        """
        暂开子菜单
        @param item:
        """
        main_name = item.data(1)

        # 如果点击的是主菜单项，则显示其对应的子菜单项，并隐藏所有其他子菜单项
        for key in self.sub_menus.keys():
            if key == main_name:
                for sub_item in self.sub_menus[key]:
                    sub_item.setHidden(False)
            else:
                for sub_item in self.sub_menus[key]:
                    sub_item.setHidden(True)
                    sub_item.setSelected(False)  # 取消选中状态

    def show_sub_menu_page(self, item: QListWidgetItem):
        """
        渲染子菜单页面内容
        """
        item = item.data(3)
        self.right_widget.setMinimumSize(100, item['height'])
        self.right_widget.removeWidget(self.right_widget.currentWidget())
        ui = self.load_ui_file('./gui/pages/' + item['page'])
        self.right_widget.addWidget(ui)
        config.load_ba_config(self)

        self.ui = ui
        self.task = item['name']
        if item['name'] in config.load_map:
            config.load_map[item['name']](self, ui)

    def call_save_config(self):
        config.save_map[self.task](self, self.ui)
        if hasattr(self.ui, 'save'):
            original_text = self.ui.save.text()
            self.ui.save.setText("保存成功")
            QTimer.singleShot(3000, lambda: hasattr(self.ui, 'save') and self.ui.save.setText(original_text))
