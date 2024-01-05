import json

from flask import Flask, render_template

from controller.CNNController import cnnController
from controller.JobController import jobController
from controller.NLPController import nlpController
from controller.UserController import userController

app = Flask(__name__)  # Flask对象
app.config['SECRET_KEY'] = "AIWORKPROJECT123456789"  # 使用session必须配置
app.register_blueprint(jobController)
app.register_blueprint(cnnController)
app.register_blueprint(nlpController)
app.register_blueprint(userController)


# Flask是一个轻量级的Python Web开发框架

@app.route('/')  # 装饰器 类似 Java的注解   route路由flask中 绑定url和处理函数之间的对应关系
def index():
    return render_template("index.html")


# JSON接口
@app.route('/jsonuser')
def jsonUser():
    userDict = {'name': '张三', 'age': 30, 'money': 100000000}
    return json.dumps(userDict, ensure_ascii=False)
    pass


@app.route('/echarts')
def echarts():
    return render_template('echarts.html')
    pass


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)  # 会启动Web应用服务，默认端口号是5000
