import json
import sys
import time
from filelock import FileLock
import uiautomator2 as u2
from uiautomator2 import Device
from datetime import datetime, timedelta
from cnocr import CnOcr
from modules import group, cafe, mailbox, task, schedule, shop, special_entrust, wanted, arena, momo_talk, restart
from utils import ocr

func_dict = {
    'group': group.start,
    'momo_talk': momo_talk.start,
    'shop': shop.start,
    'cafe': cafe.start,
    'schedule': schedule.start,
    'special_entrust': special_entrust.start,
    'wanted': wanted.start,
    'arena': arena.start,
    'task': task.start,
    'mailbox': mailbox.start,
    'restart': restart.start
}


class Main:
    ocr: CnOcr
    ocrEN: CnOcr
    ocrNum: CnOcr
    d: Device
    bc: dict  # baas config BA配置
    tc: dict  # task config 任务配置

    def __init__(self):
        self.load_config()
        self.d = u2.connect(self.bc['baas']['serial'])
        self.ocr = CnOcr()
        self.ocrEN = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
        self.ocrNum = CnOcr(det_model_name='number-densenet_lite_136-fc', rec_model_name='number-densenet_lite_136-fc')

    def click(self, x, y, wait=True, count=1, rate=0):
        if wait:
            ocr.wait_loading(self)
        for i in range(count):
            print("\t\t\n\n Click", x, y, "\n\n")
            if rate > 0:
                time.sleep(rate)
            self.d.click(x, y)

    def double_click(self, x, y, wait=True, count=1, rate=0):
        if wait:
            ocr.wait_loading(self)
        ocr.wait_loading(self)
        for i in range(count):
            print("\t\t\n\n DoubleClick", x, y, "\n\n")
            if rate > 0:
                time.sleep(rate)
            self.d.double_click(x, y)

    def dashboard(self):
        # 使用字典将字符串映射到对应的函数

        while True:
            fn, tc = self.get_task()
            if fn is None:
                print("没有要执行的任务")
                time.sleep(1)
                continue
            # 从字典中获取函数并执行
            if fn in func_dict:
                self.tc = tc
                self.tc['task'] = fn
                func_dict[fn](self)
                self.finish_task(fn)
            else:
                print(f"函数不存在:{fn}")
                sys.exit(0)

    def config_path(self):
        return './configs/{0}'.format(sys.argv[1])

    def load_config(self):
        with open(self.config_path(), 'r') as f:
            data = json.load(f)
        self.bc = data
        pass

    def save_config(self):
        lock = FileLock(self.config_path())
        with lock:
            with open(self.config_path().format(sys.argv[1]), 'w') as f:
                f.write(json.dumps(self.bc, indent=4))

    def get_task(self):
        self.load_config()
        for ba_task, con in self.bc.items():
            if ba_task == 'baas':
                continue
            if not con['enable']:
                print("功能已关闭", ba_task, con, "\n")
                continue
            if datetime.strptime(con['next'], "%Y-%m-%d %H:%M:%S") > datetime.now():
                print("队列中", ba_task, con, "\n")
                continue
            return ba_task, con
        return None, None

    def finish_task(self, fn):
        # 获取当前日期时间
        now = datetime.now()
        # 计算下次执行时间
        if 'interval' in self.tc:
            future = now + timedelta(seconds=self.tc['interval'])
        else:
            future = now + timedelta(days=1)
            # 别问我为什么要写5点 :)
            future = datetime(future.year, future.month, future.day, 5, 0)
        # 将datetime对象转成字符串
        self.bc[fn]['next'] = future.strftime("%Y-%m-%d %H:%M:%S")
        # 完成任务
        del self.tc["task"]
        self.save_config()


if __name__ == '__main__':
    Main().dashboard()
