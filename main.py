import sys
from multiprocessing import Process

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget

from baas import Baas
from common.gui import Gui


def baas_dashboard():
    baas_instance = Baas()
    baas_instance.dashboard()


class Main(QWidget, Gui):
    baas: Process

    def __init__(self):
        super(Main, self).__init__()
        self.task = None
        self.ui = None
        self.baas = None
        self.init_app()

    def start_process(self):
        # 如果baas进程没有运行，则启动它
        if self.baas is None or not self.baas.is_alive():
            self.baas = Process(target=baas_dashboard)
            self.baas.start()

    def stop_process(self):
        if self.baas is None or not self.baas.is_alive():
            return
        # 请求终止baas进程
        self.baas.terminate()
        # 等待进程实际结束
        self.baas.join()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_wnd = Main()
    main_wnd.resize(1280, 720)
    main_wnd.show()
    app.setApplicationName("蔚蓝档案-BAAS")
    app.exec()
