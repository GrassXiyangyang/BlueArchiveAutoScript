import json
import sys
import time
import uiautomator2 as u2
from uiautomator2 import Device
from datetime import datetime, timedelta
from cnocr import CnOcr

from common import stage
from modules.baas import restart
from modules.daily import group, shop, cafe, schedule, special_entrust, wanted, arena, make
from modules.reward import momo_talk, work_task, mailbox
from modules.scan import normal_task, hard_task

func_dict = {
    'group': group.start,
    'momo_talk': momo_talk.start,
    'shop': shop.start,
    'cafe': cafe.start,
    'schedule': schedule.start,
    'special_entrust': special_entrust.start,
    'wanted': wanted.start,
    'arena': arena.start,
    'make': make.start,
    'work_task': work_task.start,
    'normal_task': normal_task.start,
    'hard_task': hard_task.start,
    'mailbox': mailbox.start,
    'restart': restart.start,
}


class Baas:
    ocr: CnOcr
    ocrEN: CnOcr
    ocrNum: CnOcr
    d: Device
    bc: dict  # baas config BA配置
    tc: dict  # task config 任务配置

    def __init__(self, con):
        self.con = con
        self.load_config()
        self.d = u2.connect(self.bc['baas']['serial'])
        self.ocr = CnOcr()
        self.ocrEN = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
        self.ocrNum = CnOcr(det_model_name='number-densenet_lite_136-fc', rec_model_name='number-densenet_lite_136-fc')

    def click(self, x, y, wait=True, count=1, rate=0):
        if wait:
            stage.wait_loading(self)
        for i in range(count):
            print("\t\t\n\n Click", x, y, "\n\n")
            if rate > 0:
                time.sleep(rate)
            self.d.click(x, y)

    def click_condition(self, x, y, cond, fn, fn_args, wait=True, rate=0):
        """
        条件点击，直到不满足条件为止
        @param x: x坐标
        @param y: y坐标
        @param cond: true 或 false 
        @param fn: 要执行的函数，需要返回bool
        @param fn_args: 执行函数的参数
        @param wait: 是否需要等待加载
        @param rate: 每次点击等待时间
        """
        if wait:
            stage.wait_loading(self)
        self.d.click(x, y)
        while cond != fn(self, *fn_args):
            time.sleep(rate)
            self.d.click(x, y)

    def double_click(self, x, y, wait=True, count=1, rate=0):
        if wait:
            stage.wait_loading(self)
        for i in range(count):
            print("\t\t\n\n DoubleClick", x, y, "\n\n")
            if rate > 0:
                time.sleep(rate)
            self.d.double_click(x, y)

    def dashboard(self):
        # 使用字典将字符串映射到对应的函数

        while True:
            fn, tc = self.task_schedule(True, True)
            if fn is None:
                print("没有要执行的任务")
                time.sleep(3)
                continue
            # 从字典中获取函数并执行
            if fn in func_dict:
                self.tc = tc
                self.tc['task'] = fn
                self.finish_seconds = 0
                func_dict[fn](self)
                self.finish_task(fn)
            else:
                print(f"函数不存在:{fn}")
                sys.exit(0)

    def config_path(self):
        return './configs/{0}.json'.format(self.con)

    def load_config(self):
        with open(self.config_path(), 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.bc = data
        pass

    def save_config(self):
        with open(self.config_path(), 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.bc, indent=4, ensure_ascii=False))

    def task_schedule(self, is_running, get_task=False):
        self.load_config()
        running = []
        waiting = []
        queue = []
        closed = []
        for ba_task, con in self.bc.items():
            # 被关闭的功能
            if ba_task == 'baas':
                continue
            # 超出截止时间
            task = {'next': con['next'], 'task': ba_task, 'text': con['text'], 'index': con['index']}
            if not con['enable'] or datetime.strptime(con['end'], "%Y-%m-%d %H:%M:%S") < datetime.now():
                closed.append(task)
                continue
            # 时间未到
            if datetime.strptime(con['next'], "%Y-%m-%d %H:%M:%S") > datetime.now():
                waiting.append(task)
                continue
            # 第一个是正在运行
            if get_task:
                return ba_task, con
            if is_running and len(running) == 0:
                running.append(task)
                continue
            # 队列中
            queue.append(task)

        if get_task:
            return None, None

        waiting.sort(key=lambda x: (x['index'], datetime.strptime(x['next'], "%Y-%m-%d %H:%M:%S")))
        queue.sort(key=lambda x: (x['index'], datetime.strptime(x['next'], "%Y-%m-%d %H:%M:%S")))
        return {'running': running, 'waiting': waiting, 'queue': queue, 'closed': closed}

    def finish_task(self, fn):
        self.load_config()
        # 获取当前日期时间
        now = datetime.now()
        if self.finish_seconds > 0:
            future = now + timedelta(seconds=self.finish_seconds)
        else:
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
