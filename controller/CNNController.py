import datetime
import json
import os

import numpy as np
import torch as t
from PIL import Image
from flask import Blueprint, render_template, request
from numpy import double

from dao.ImageDao import ImageDao
from models.Resnet34 import ResNet34CNN
from service.ImageService import convert_to_grayscale, convert_to_binary, histogram_equalization, median_filtering, \
    sobel_operator, otsu_segmentation, adjust_brightness

cnnController = Blueprint('cnnController', __name__)


# 加载模型
def loadModel():
    in_channels = 3
    num_classes = 10
    model = ResNet34CNN(num_classes)
    print(os.getcwd())
    # savePath = os.path.dirname(__file__) + "/../models/cnn_cifar10.pth"
    savePath = os.path.dirname(__file__) + "/../models/test.pth"
    model.eval()
    model.load_state_dict(t.load(savePath))
    return model
    pass


# 加载模型
model = loadModel()
classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']


@cnnController.route("/goimage")
def goImage():
    return render_template('uploadimage02.html')
    # return render_template('uploadimage.html')
    pass


@cnnController.route("/goimage2")
def goImage2():
    image_dao = ImageDao()
    images = image_dao.get_all_images()
    image_dao.close()
    return render_template('uploadimage03.html', images=images)
    pass


@cnnController.route("/goimage3", methods=["post"])
def goImage3():
    # 创建ImageDao实例
    image_dao = ImageDao()
    # 从数据库中获取图片的路径信息
    image_id = request.form.get("imagesid")
    left_image_path = image_dao.get_filepath_by_imagesid(image_id)
    image_dao.close()
    return render_template('uploadimage04.html', leftImagePath=left_image_path, imagesid=image_id)
    pass


@cnnController.route("/cnnimage", methods=["post"])
def cnnImage():
    file = request.files.get('uploadFile')  # 读取上传的文件
    if file:
        try:
            path = os.path.dirname(__file__) + '/../static/uploads/' + file.filename
            file.save(path)  # 保存文件到/static/uploads目录
        except Exception as e:
            return json.dumps({'uploaded': 0, 'fileName': "", 'url': ""})
            pass
        # 文件上传成功，调用算法模型识别图片

        image = Image.open(path)  # 使用PIL读取图片
        image = image.resize((32, 32))  # 缩放
        image = np.array(image)  # 转numpy
        image = image[:, :, :3].transpose(2, 0, 1).reshape(-1, 3, 32, 32) / 255  # 如果是RGBA  只获取RGB
        image = t.from_numpy(image)
        classList = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
        result = model(image.float()).flatten()
        softmax = t.nn.Softmax()
        result = softmax(result)
        index = np.argmax(result.detach().numpy())
        print((result[index] * 100))
        print(classList[index], "可能性：", '%.2f%%' % (result[index] * 100))

        # 获取张量的数值部分

        image_dao = ImageDao()
        result_value = result[index].item()
        formatted_result = '{:.2f}%'.format(result_value * 100)
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        image_dao.insert_image(file.filename, '/static/uploads/' + file.filename, classList[index], formatted_result,
                               current_time)
        image_dao.close()

        return json.dumps({'uploaded': 1, 'fileName': file.filename,
                           'url': '/static/uploads/' + file.filename, 'typeName': classList[index],
                           'acc': '%.2f%%' % (result[index] * 100)})
    else:
        return json.dumps({'uploaded': 0, 'fileName': "", 'url': ""})
    pass


@cnnController.route("/test", methods=["POST"])
def test():
    # 通过 request 对象获取 POST 请求中的参数
    imagesid = request.form.get("imagesid")
    image_dao = ImageDao()
    left_image_path = image_dao.get_filepath_by_imagesid(imagesid)
    image = convert_to_grayscale(imagesid)
    static_path = os.path.join(os.getcwd(), 'static')
    processed_image_path = os.path.join(static_path, 'processed_images', f'processed_{imagesid}.png')
    image.save(processed_image_path)
    # 计算相对路径
    right_image_path = os.path.relpath(processed_image_path, static_path)
    # 将反斜杠替换为正斜杠，确保在URL中的路径分隔符是正斜杠
    right_image_path = "/static/" + right_image_path.replace("\\", "/")
    return render_template('uploadimage04.html', leftImagePath=left_image_path, rightImagePath=right_image_path,
                           imagesid=imagesid)


@cnnController.route("/test2", methods=["POST"])
def test2():
    # 通过 request 对象获取 POST 请求中的参数
    imagesid = request.form.get("imagesid")
    image_dao = ImageDao()
    left_image_path = image_dao.get_filepath_by_imagesid(imagesid)
    image = convert_to_binary(imagesid)
    static_path = os.path.join(os.getcwd(), 'static')
    processed_image_path = os.path.join(static_path, 'processed_images', f'processed_{imagesid}.png')
    image.save(processed_image_path)
    # 计算相对路径
    right_image_path = os.path.relpath(processed_image_path, static_path)
    # 将反斜杠替换为正斜杠，确保在URL中的路径分隔符是正斜杠
    right_image_path = "/static/" + right_image_path.replace("\\", "/")
    return render_template('uploadimage04.html', leftImagePath=left_image_path, rightImagePath=right_image_path,
                           imagesid=imagesid)


@cnnController.route("/test3", methods=["POST"])
def test3():
    # 通过 request 对象获取 POST 请求中的参数
    imagesid = request.form.get("imagesid")
    image_dao = ImageDao()
    left_image_path = image_dao.get_filepath_by_imagesid(imagesid)
    image = histogram_equalization(imagesid)
    static_path = os.path.join(os.getcwd(), 'static')
    processed_image_path = os.path.join(static_path, 'processed_images', f'processed_{imagesid}.png')
    image.save(processed_image_path)
    # 计算相对路径
    right_image_path = os.path.relpath(processed_image_path, static_path)
    # 将反斜杠替换为正斜杠，确保在URL中的路径分隔符是正斜杠
    right_image_path = "/static/" + right_image_path.replace("\\", "/")
    return render_template('uploadimage04.html', leftImagePath=left_image_path, rightImagePath=right_image_path,
                           imagesid=imagesid)


@cnnController.route("/test4", methods=["POST"])
def test4():
    # 通过 request 对象获取 POST 请求中的参数
    imagesid = request.form.get("imagesid")
    image_dao = ImageDao()
    left_image_path = image_dao.get_filepath_by_imagesid(imagesid)
    image = median_filtering(imagesid)
    static_path = os.path.join(os.getcwd(), 'static')
    processed_image_path = os.path.join(static_path, 'processed_images', f'processed_{imagesid}.png')
    image.save(processed_image_path)
    # 计算相对路径
    right_image_path = os.path.relpath(processed_image_path, static_path)
    # 将反斜杠替换为正斜杠，确保在URL中的路径分隔符是正斜杠
    right_image_path = "/static/" + right_image_path.replace("\\", "/")
    return render_template('uploadimage04.html', leftImagePath=left_image_path, rightImagePath=right_image_path,
                           imagesid=imagesid)


@cnnController.route("/test5", methods=["POST"])
def test5():
    # 通过 request 对象获取 POST 请求中的参数
    imagesid = request.form.get("imagesid")
    image_dao = ImageDao()
    left_image_path = image_dao.get_filepath_by_imagesid(imagesid)
    image = sobel_operator(imagesid)
    static_path = os.path.join(os.getcwd(), 'static')
    processed_image_path = os.path.join(static_path, 'processed_images', f'processed_{imagesid}.png')
    image.save(processed_image_path)
    # 计算相对路径
    right_image_path = os.path.relpath(processed_image_path, static_path)
    # 将反斜杠替换为正斜杠，确保在URL中的路径分隔符是正斜杠
    right_image_path = "/static/" + right_image_path.replace("\\", "/")
    return render_template('uploadimage04.html', leftImagePath=left_image_path, rightImagePath=right_image_path,
                           imagesid=imagesid)


@cnnController.route("/test6", methods=["POST"])
def test6():
    # 通过 request 对象获取 POST 请求中的参数
    imagesid = request.form.get("imagesid")
    image_dao = ImageDao()
    left_image_path = image_dao.get_filepath_by_imagesid(imagesid)
    image = otsu_segmentation(imagesid)
    static_path = os.path.join(os.getcwd(), 'static')
    processed_image_path = os.path.join(static_path, 'processed_images', f'processed_{imagesid}.png')
    image.save(processed_image_path)
    # 计算相对路径
    right_image_path = os.path.relpath(processed_image_path, static_path)
    # 将反斜杠替换为正斜杠，确保在URL中的路径分隔符是正斜杠
    right_image_path = "/static/" + right_image_path.replace("\\", "/")
    return render_template('uploadimage04.html', leftImagePath=left_image_path, rightImagePath=right_image_path,
                           imagesid=imagesid)


@cnnController.route("/test7", methods=['Post'])
def test7():
    # 通过 request 对象获取 POST 请求中的参数
    imagesid = request.form.get("imagesid")
    factor = request.form.get("factor")
    image_dao = ImageDao()
    left_image_path = image_dao.get_filepath_by_imagesid(imagesid)
    image = adjust_brightness(imagesid, double(factor))
    static_path = os.path.join(os.getcwd(), 'static')
    processed_image_path = os.path.join(static_path, 'processed_images', f'processed_{imagesid}.png')
    image.save(processed_image_path)
    # 计算相对路径
    right_image_path = os.path.relpath(processed_image_path, static_path)
    # 将反斜杠替换为正斜杠，确保在URL中的路径分隔符是正斜杠
    right_image_path = "/static/" + right_image_path.replace("\\", "/")
    return render_template('uploadimage04.html', leftImagePath=left_image_path, rightImagePath=right_image_path,
                           imagesid=imagesid)


@cnnController.route("/test8", methods=['Post'])
def test8():
    # 通过 request 对象获取 POST 请求中的参数
    imagesid = request.form.get("imagesid")
    factor = request.form.get("factor")
    image_dao = ImageDao()
    left_image_path = image_dao.get_filepath_by_imagesid(imagesid)
    image = adjust_brightness(imagesid, double(factor))
    static_path = os.path.join(os.getcwd(), 'static')
    processed_image_path = os.path.join(static_path, 'processed_images', f'processed_{imagesid}.png')
    image.save(processed_image_path)
    # 计算相对路径
    right_image_path = os.path.relpath(processed_image_path, static_path)
    # 将反斜杠替换为正斜杠，确保在URL中的路径分隔符是正斜杠
    right_image_path = "/static/" + right_image_path.replace("\\", "/")
    return render_template('uploadimage04.html', leftImagePath=left_image_path,
                           rightImagePath="static/processed_images/processed.jpg",
                           imagesid=imagesid)


@cnnController.route("/getByClasses", methods=['Post'])
def getByClasses():
    image_dao = ImageDao()
    images_class = request.form.get("inputData")
    print(images_class)
    if images_class == "":
        images = image_dao.get_all_images();
    else:
        images = image_dao.get_images_by_classes(images_class)
    image_dao.close()
    return render_template('uploadimage03.html', images=images)
    pass
