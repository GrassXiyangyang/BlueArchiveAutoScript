import numpy as np
import cv2
import aircv as ac
import os
import time
from common import stage
from common.iconst import *


def screenshot_cut(self, area, before_wait=0, need_loading=True, path=SS_PATH, file=SS_FILE):
    """
    截图并裁剪图片
    @param self:
    @param area: 剪切区域
    @param before_wait: 前置等待时间
    @param need_loading: 等待加载
    @return: 图片对象
    """
    if before_wait > 0:
        time.sleep(before_wait)
    # 检查文字前，等待加载完成
    if need_loading:
        stage.wait_loading(self)
    # 创建目录
    if not os.path.exists(path):
        os.makedirs(path)
    if len(area) == 0:
        return self.d.screenshot(file)
    else:
        ss = self.d.screenshot()
        img = ss.crop(area)
        img.save(file)
        return img


def match_image(raw, search, threshold=0.7):
    # raw=原始图像，search=待查找的图片
    match_result = ac.find_all_template(ac.imread(raw), ac.imread(search), threshold)
    return match_result


def compare_image(self, area, file, before_wait=0, need_loading=True, threshold=5):
    """
    对图片坐标内的图片和资源图片是否匹配
    @param self:
    @param area: 坐标(左上xy,右下xy)
    @param file: 资源文件
    @param before_wait: 前置等待
    @param need_loading: 需要加载
    @param threshold: 匹配程度0为完全匹配
    @return: 是否匹配
    """
    screenshot_cut(self, area, before_wait, need_loading)
    ss_img = ac.imread(SS_FILE)
    res_img = ac.imread('assets/{0}.png'.format(file))
    # 如果两张图片的尺寸不同
    if ss_img.shape != res_img.shape:
        # 将待查找的图片调整为与原始图像一样的尺寸
        res_img = cv2.resize(res_img, (ss_img.shape[1], ss_img.shape[0]))
    # 计算差异值
    diff = cv2.absdiff(ss_img, res_img)
    # 计算MSE（Mean Squared Error）
    mse = np.mean(diff ** 2)
    return mse <= threshold
