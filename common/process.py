from multiprocessing import Process
from common.baas import Baas


def baas_dashboard(con):
    Baas(con).dashboard()


class Main:
    def __init__(self):
        self.processes = {}  # 存储所有的进程

    def start_process(self, con):
        """
        启动进程
        @param con: 配置文件名称
        """
        # 如果对应的进程没有运行，则启动它
        if con not in self.processes or not self.processes[con].is_alive():
            self.processes[con] = Process(target=baas_dashboard, args=(con,))
            self.processes[con].start()

    def stop_process(self, con):
        """
        停止进程
        @param con: 配置文件名称
        """
        if con in self.processes and self.processes[con].is_alive():
            # 请求终止baas进程
            self.processes[con].terminate()
            # 等待进程实际结束
            self.processes[con].join()

    def state_process(self, con):
        """
        获取进程执行状态
        @param con: 配置文件名称
        """
        if con in self.processes:
            return self.processes[con].is_alive()
        else:
            return False


m = Main()
