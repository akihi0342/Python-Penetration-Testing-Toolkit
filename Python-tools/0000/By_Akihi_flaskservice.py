from flask import Flask, request
from jinja2 import Template

# 创建Flask应用实例
app = Flask(__name__)

# 定义根路由
@app.route("/")
def index():
    """
    处理根路由的请求，根据用户输入的name参数渲染模板。
    """
    # 获取用户输入的name参数，默认为guest
    name = request.args.get('name', 'guest')
    # 创建Jinja2模板
    t = Template("Hello " + name)
    # 渲染模板并返回结果
    return t.render()

if __name__ == '__main__':
    # 启动Flask应用，开启调试模式
    app.run(debug=True)