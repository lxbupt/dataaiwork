import json

from aip import AipFace
from flask import render_template, request, session, Blueprint

from service.UserService import UserService

AppID = '37367314'
APIKey = 'TMxW8EjNm5E99d8IXejqG4MH'
SecretKey = 'f7RKzB1a5dyabMQaGqw1WqG8Rezy89QL'

userController = Blueprint('userController', __name__)

aipFace = AipFace(AppID, APIKey, SecretKey)  # 云服务AI接口


@userController.route('/gologin')
def goLogin():
    return render_template('login.html')
    pass


@userController.route('/login', methods=['post'])
def login():
    # 获取前台参数
    imageData = request.form.get('imageData')
    # print(imageData)
    # 检测图片中是否有人脸：1、baidu-aip 2、opencv、3、face_recognition(作业：使用face_recognition实现人脸识别和比对)
    imageType = 'BASE64'
    result = aipFace.detect(imageData, imageType)
    print(result)
    # 实现人脸比对操作
    userService = UserService()
    userList = userService.getAllUserList()
    loginUser = None
    for user in userList:
        userFace = user['userFace']
        faceDict = [{'image_type': 'BASE64', 'image': imageData}, {'image_type': 'BASE64', 'image': userFace}]
        match = aipFace.match(faceDict)  # 比对人脸的接口
        print(match)
        if match['error_msg'] == 'SUCCESS':
            if match['result']['score'] > 95:
                loginUser = user
                break
                pass
            pass
        pass
    if loginUser:  # 人脸识别成功，将用户登录信息存放在session中
        loginUser['userFace'] = ''
        session['loginUser'] = loginUser
        result['face_login'] = 'SUCCESS'
        return json.dumps(result, ensure_ascii=False)
        pass
    result['face_login'] = 'FAIL'
    return json.dumps(result, ensure_ascii=False)  # response响应  json响应接口

    pass


@userController.route('/logout')
def logout():
    session.pop('loginUser')
    session.clear()
    return render_template('index.html')
    pass
