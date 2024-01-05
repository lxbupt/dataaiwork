# _*_ coding : utf-8 _*_
# @Time : 2024/1/2 10:17
# @Author : 战斧牛排炖洋芋
# @File : ImageService
# @Project : dataaiwork
from PIL import ImageEnhance
from scipy.ndimage import median_filter
from scipy.signal import convolve2d

from dao.ImageDao import ImageDao


def convert_to_grayscale(imagesid):
    # 创建ImageDao实例
    image_dao = ImageDao()
    # 从数据库中获取图片的路径信息
    image_path = image_dao.get_filepath_by_imagesid(imagesid)
    full_image_path = "D:\\pystudy\\dataaiwork" + image_path
    original_image = Image.open(full_image_path)
    grayscale_image = original_image.convert("L")
    return grayscale_image
    pass


def convert_to_binary(imagesid, threshold=128):
    # 创建ImageDao实例
    image_dao = ImageDao()
    # 从数据库中获取图片的路径信息
    image_path = image_dao.get_filepath_by_imagesid(imagesid)
    full_image_path = "D:\\pystudy\\dataaiwork" + image_path
    # 打开原始图像
    original_image = Image.open(full_image_path)
    # 转换为灰度图像
    grayscale_image = original_image.convert("L")
    # 将灰度图像转换为 NumPy 数组
    grayscale_array = np.array(grayscale_image)
    # 二值化图像
    binary_array = (grayscale_array > threshold) * 255
    # 创建二值图像
    binary_image = Image.fromarray(binary_array.astype(np.uint8))
    return binary_image


from PIL import Image, ImageOps
import numpy as np


def histogram_equalization(imagesid):
    # 创建ImageDao实例
    image_dao = ImageDao()
    # 从数据库中获取图片的路径信息
    image_path = image_dao.get_filepath_by_imagesid(imagesid)
    full_image_path = "D:\\pystudy\\dataaiwork" + image_path

    # 打开原始图像
    original_image = Image.open(full_image_path)

    # 将图像转换为灰度图像
    gray_image = ImageOps.grayscale(original_image)

    # 进行直方图均衡
    equalized_image = ImageOps.equalize(gray_image)

    # 将 PIL 图像转换为 NumPy 数组
    equalized_array = np.array(equalized_image)

    # 创建均衡后的图像
    equalized_image = Image.fromarray(equalized_array.astype(np.uint8))

    return equalized_image


def median_filtering(imagesid, filter_size=3):
    # 创建ImageDao实例
    image_dao = ImageDao()
    # 从数据库中获取图片的路径信息
    image_path = image_dao.get_filepath_by_imagesid(imagesid)
    full_image_path = "D:\\pystudy\\dataaiwork" + image_path

    # 打开原始图像
    original_image = Image.open(full_image_path)

    # 将图像转换为 NumPy 数组
    image_array = np.array(original_image)

    # 使用 SciPy 中的中值滤波函数
    filtered_image_array = median_filter(image_array, size=filter_size)

    # 创建中值滤波后的图像
    filtered_image = Image.fromarray(filtered_image_array.astype(np.uint8))

    return filtered_image


def sobel_operator(imagesid):
    # 创建ImageDao实例
    image_dao = ImageDao()
    # 从数据库中获取图片的路径信息
    image_path = image_dao.get_filepath_by_imagesid(imagesid)
    full_image_path = "D:\\pystudy\\dataaiwork" + image_path

    # 打开原始图像
    original_image = Image.open(full_image_path)

    # 将图像转换为灰度图像
    gray_image = ImageOps.grayscale(original_image)

    # 将 PIL 图像转换为 NumPy 数组
    gray_array = np.array(gray_image)

    # 定义Sobel算子
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    # 对图像进行卷积操作
    gradient_x = convolve2d(gray_array, sobel_x, mode='same', boundary='symm', fillvalue=0)
    gradient_y = convolve2d(gray_array, sobel_y, mode='same', boundary='symm', fillvalue=0)

    # 计算梯度幅度
    gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)

    # 将梯度幅度映射到0-255范围
    normalized_gradient = (gradient_magnitude / gradient_magnitude.max()) * 255

    # 创建Sobel锐化后的图像
    sharpened_image = Image.fromarray(normalized_gradient.astype(np.uint8))

    return sharpened_image


def otsu_segmentation(imagesid):
    # 创建ImageDao实例
    image_dao = ImageDao()
    # 从数据库中获取图片的路径信息
    image_path = image_dao.get_filepath_by_imagesid(imagesid)
    full_image_path = "D:\\pystudy\\dataaiwork" + image_path

    # 打开原始图像
    original_image = Image.open(full_image_path)

    # 将图像转换为灰度图像
    gray_image = original_image.convert("L")
    gray_array = np.array(gray_image)

    # 获取图像直方图
    hist, _ = np.histogram(gray_array.flatten(), bins=256, range=[0, 256])

    # 计算图像总体的平均灰度
    total_pixels = gray_array.size
    mean_intensity = np.sum(np.arange(256) * hist) / total_pixels

    # 初始化类内方差和总体方差
    class_variances = []

    # 遍历每个可能的阈值
    for threshold in range(1, 256):
        # 计算低于和高于阈值的像素的类别
        class_below_threshold = gray_array[gray_array <= threshold]
        class_above_threshold = gray_array[gray_array > threshold]

        # 计算各类别的像素数量
        count_below_threshold = class_below_threshold.size
        count_above_threshold = class_above_threshold.size

        # 计算各类别的权重
        weight_below_threshold = count_below_threshold / total_pixels
        weight_above_threshold = count_above_threshold / total_pixels

        # 计算各类别的平均灰度
        mean_below_threshold = np.sum(class_below_threshold) / count_below_threshold if count_below_threshold > 0 else 0
        mean_above_threshold = np.sum(class_above_threshold) / count_above_threshold if count_above_threshold > 0 else 0

        # 计算各类别的方差
        variance_below_threshold = np.sum((
                                                  class_below_threshold - mean_below_threshold) ** 2) / count_below_threshold if count_below_threshold > 0 else 0
        variance_above_threshold = np.sum((
                                                  class_above_threshold - mean_above_threshold) ** 2) / count_above_threshold if count_above_threshold > 0 else 0

        # 计算类内方差
        intra_class_variance = weight_below_threshold * variance_below_threshold + weight_above_threshold * variance_above_threshold

        # 计算总体方差
        total_variance = weight_below_threshold * (
                mean_below_threshold - mean_intensity) ** 2 + weight_above_threshold * (
                                 mean_above_threshold - mean_intensity) ** 2

        # 计算类间方差
        inter_class_variance = total_variance - intra_class_variance

        # 将类间方差添加到列表中
        class_variances.append(inter_class_variance)

    # 找到最大类间方差对应的阈值
    optimal_threshold = np.argmax(class_variances) + 1

    # 对图像进行二值化
    binary_array = (gray_array > optimal_threshold) * 255
    binary_image = Image.fromarray(binary_array.astype(np.uint8))

    return binary_image


def adjust_brightness(imagesid, brightness_factor=1.5):
    # 创建ImageDao实例
    image_dao = ImageDao()
    # 从数据库中获取图片的路径信息
    image_path = image_dao.get_filepath_by_imagesid(imagesid)
    full_image_path = "D:\\pystudy\\dataaiwork" + image_path
    # 打开原始图像
    original_image = Image.open(full_image_path)

    # 调整亮度
    enhancer = ImageEnhance.Brightness(original_image)
    brightened_image = enhancer.enhance(brightness_factor)

    return brightened_image
