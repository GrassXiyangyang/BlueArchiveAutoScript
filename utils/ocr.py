import math
import os
import time
import numpy as np
import cv2
from iconst.emulator import *
from fuzzywuzzy import fuzz
import aircv as ac


def screenshot(self):
	path = SS_PATH + SS_FILE
	self.d.screenshot(path)


def wait_loading(self):
	"""
	检查是否加载中，
	"""
	if not os.path.exists(SS_PATH):
		os.makedirs(SS_PATH)
	path = SS_PATH + SS_FILE
	ss = self.d.screenshot()
	img = ss.crop((925, 650, 1170, 685))
	img.save(path)
	out = self.ocrEN.ocr(path)
	text = "Now Loading"
	ex = any(map(lambda d: fuzz.ratio(d.get('text'), text) > 20, out))
	print("判断是否 为", text, "结果", ex)
	print("\t\t\t=======>>> \t\t", out)
	# 如果找到加载继续等待
	if ex:
		print("\t\t\t正在加载..............")
		time.sleep(SS_RATE)
		return wait_loading(self)
	# 因为ba的loading会转动,可能会识别不到,所以需要连续两次判定为未加载
	# if i < 2:
	#     return wait_loading(self, i + 1)
	return True


def screenshot_get_text(self, area, wait=True, ocr=None):
	# 检查文字前，等待加载完成
	wait_loading(self)
	if not os.path.exists(SS_PATH):
		os.makedirs(SS_PATH)
	path = SS_PATH + SS_FILE
	img = self.d.screenshot().crop(area)
	img.save(path)
	if ocr is None:
		out = self.ocr.ocr(path)
	else:
		out = ocr.ocr(path)
	if len(out) == 0 and wait:
		return screenshot_get_text(self, area, wait)
	if len(out) == 0:
		return ''
	return out[0]['text']


def screenshot_check_text(self, text, area=(), wait=True, before_wait=0):
	if before_wait > 0:
		time.sleep(before_wait)
	# 检查文字前，等待加载完成
	wait_loading(self)
	# 创建目录
	if not os.path.exists(SS_PATH):
		os.makedirs(SS_PATH)
	path = SS_PATH + SS_FILE
	if len(area) == 0:
		self.d.screenshot(path)
	else:
		ss = self.d.screenshot()
		img = ss.crop(area)
		img.save(path)
	out = self.ocr.ocr(path)
	ex = any(map(lambda d: fuzz.ratio(d.get('text'), text) > 60, out))
	print("判断是否 为", text, "结果", ex)
	print("\t\t\t", out)
	# 如果已经找到 或 不需要等待直接返回结果
	if ex or not wait:
		return ex
	time.sleep(SS_RATE)
	return screenshot_check_text(self, text, area, wait)


def color_distance(rgb1, rgb2):
	r1, g1, b1 = rgb1
	r2, g2, b2 = rgb2
	return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def check_rgb(self, area, rgb):
	"""
	根据一个坐标判断rgb
	"""
	area = (area[0], area[1], area[0] + 10, area[1] + 10)
	screenshot_check_text(self, '', area, False)
	path = SS_PATH + SS_FILE
	img = cv2.imread(path)
	return np.array_equal(img[0][0], np.array(rgb))


def check_one_key_active(self, area=(1090, 683, 1091, 684)):
	"""
	判断右下角<一键领取>是否可点击
	"""
	screenshot_check_text(self, '', area, False)
	path = SS_PATH + SS_FILE
	img = cv2.imread(path)
	dist = color_distance(img[0][0], (75, 238, 249))
	return dist <= 20


def close_prize_info(self):
	"""
	关闭奖励道具结算页面
	"""
	screenshot_check_text(self, '点击继续', (577, 614, 704, 648), True)
	# 关闭道具信息
	self.click(640, 635)
	time.sleep(0.5)


def is_home(self, wait=True):
	return screenshot_check_text(self, "咖啡厅", (60, 676, 122, 695), wait)


def is_login(self, wait=True):
	return screenshot_check_text(self, "菜单", (35, 625, 75, 650), wait)


def is_group(self, wait=True):
	return screenshot_check_text(self, "小组大厅", (97, 7, 220, 41), wait)


def is_mailbox(self, wait=True):
	return screenshot_check_text(self, "邮箱", (97, 7, 220, 41), wait)


def is_task(self, wait=True):
	return screenshot_check_text(self, "工作任务", (97, 7, 225, 41), wait)


def is_shop(self, wait=True):
	return screenshot_check_text(self, "商店", (97, 7, 163, 41), wait)


def is_schedule(self, wait=True):
	return screenshot_check_text(self, "日程", (97, 7, 165, 41), wait)


def is_cafe(self, wait=True):
	return screenshot_check_text(self, "咖啡厅", (213, 7, 300, 40), wait)


def match_imgage(raw, search, threshold=0.7):
	# raw=原始图像，search=待查找的图片
	match_result = ac.find_all_template(ac.imread(raw), ac.imread(search), threshold)
	return match_result


def calc_image_mse(raw, search, threshold=200):
	raw_img = ac.imread(raw)
	search_img = ac.imread(search)
	# 如果两张图片的尺寸不同
	if raw_img.shape != search_img.shape:
		# 将待查找的图片调整为与原始图像一样的尺寸
		search_img = cv2.resize(search_img, (raw_img.shape[1], raw_img.shape[0]))
	# 计算差异值
	diff = cv2.absdiff(raw_img, search_img)
	# 计算MSE（Mean Squared Error）
	mse = np.mean(diff ** 2)
	return mse <= threshold
