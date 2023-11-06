import numpy as np
import cv2
import aircv as ac


def match_image(raw, search, threshold=0.7):
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
