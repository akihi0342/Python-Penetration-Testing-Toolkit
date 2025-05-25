#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File    : Fileserver.py

import socketserver
import os
import re
import json
import struct
from optparse import OptionParser

# 发送文件的函数
def sendFile(conn, head_info, head_info_len, filename):
    try:
        # 发送报头长度
        conn.send(head_info_len)
        # 发送报头信息
        conn.send(head_info.encode('utf-8'))
        # 以二进制读取模式打开文件并发送文件内容
        with open(filename, 'rb') as f:
            conn.sendall(f.read())
        print(f'[+] 发送成功! {filename}')
    except Exception as e:
        print(f'[-] 发送失败! {filename}, 错误信息: {e}')

# 处理文件信息的函数
def operafile(filename):
    # 获取文件大小
    filesize_bytes = os.path.getsize(filename)
    # 正则表达式匹配文件名
    pattern = re.compile(r'([^<>/\\\|:""\*\?]+\.\w+$)')
    data = pattern.findall(filename)
    # 构建报头字典
    head_dir = {
        'filename': data,
        'filesize_bytes': filesize_bytes,
    }
    # 将报头字典序列化为JSON字符串
    head_info = json.dumps(head_dir)
    # 打包报头信息长度
    head_info_len = struct.pack('i', len(head_info))
    return head_info_len, head_info

# 自定义请求处理类
class MyServer(socketserver.BaseRequestHandler):
    buffsize = 1024

    def handle(self):
        print(f'[+] 远程客户端IP地址：{self.client_address[0]}\n')
        while True:
            # 获取用户输入的文件名
            filename = input('请输入要发送的文件名（输入 "exit" 退出）>>>').strip()
            if filename == "exit":
                break
            if not os.path.isfile(filename):
                print(f'[-] 文件 {filename} 不存在，请重新输入。')
                continue
            # 处理文件信息
            head_info_len, head_info = operafile(filename)
            # 发送文件
            sendFile(self.request, head_info, head_info_len, filename)
        # 关闭连接
        self.request.close()

def main():
    # 创建命令行参数解析器
    parser = OptionParser("Usage:%prog -p <端口> ")
    # 添加端口参数
    parser.add_option('-p', type='string', dest='port', help='指定目标端口')
    # 解析命令行参数
    options, args = parser.parse_args()
    # 将端口号转换为整数类型
    port = int(options.port)

    print(f"[+] 正在监听端口 {port}")
    # 创建多线程TCP服务器
    s = socketserver.ThreadingTCPServer(('0.0.0.0', port), MyServer)
    # 启动服务器并持续监听
    s.serve_forever()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("用户中断操作，正在终止所有线程...")
    except Exception as e:
        print(f"发生错误: {e}")