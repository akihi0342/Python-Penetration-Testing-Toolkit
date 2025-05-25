#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File    : Fileclient.py

import socket
import os
import sys
import json
import struct
from optparse import OptionParser

# 接收文件的函数
def recv_file(head_dir, tcp_client):
    # 从报头信息中获取文件名
    filename = head_dir['filename'][0]
    # 从报头信息中获取文件大小
    filesize = head_dir['filesize_bytes']
    print(f"[+] 文件名: {filename}")
    print(f"[+] 文件大小: {filesize} 字节")

    # 已接收的文件长度
    recv_len = 0
    # 以二进制写入模式打开文件
    with open(filename, 'wb') as f:
        while recv_len < filesize:
            # 若文件大小大于1024字节，每次接收1024字节
            if filesize - recv_len > 1024:
                recv_mesg = tcp_client.recv(1024)
            else:
                # 若剩余文件大小小于等于1024字节，接收剩余部分
                recv_mesg = tcp_client.recv(filesize - recv_len)
            recv_len += len(recv_mesg)
            f.write(recv_mesg)
    print('[+] 文件传输完成!')

def main():
    # 创建命令行参数解析器
    parser = OptionParser("Usage:%prog -u <目标地址> -p <端口> ")
    # 添加目标IP地址参数
    parser.add_option('-u', type='string', dest='ip', help='指定目标IP地址')
    # 添加目标端口参数
    parser.add_option('-p', type='string', dest='port', help='指定目标端口')
    # 解析命令行参数
    options, args = parser.parse_args()

    # 将端口号转换为整数类型
    target_port = int(options.port)
    # 获取目标IP地址
    target_ip = options.ip

    # 创建TCP套接字
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 目标地址和端口元组
    ip_port = (target_ip, target_port)
    # 连接到目标地址和端口
    tcp_client.connect(ip_port)

    print('[+] 等待服务端应答数据....')
    # 接收报头长度
    struct_len = tcp_client.recv(4)
    # 解析报头长度
    struct_info_len = struct.unpack('i', struct_len)[0]
    print(f"[+] 接收头信息长度：{struct_info_len}")
    # 接收报头信息
    head_info = tcp_client.recv(struct_info_len)
    # 将报头信息反序列化为字典
    head_dir = json.loads(head_info.decode('utf-8'))
    print(f"[+] 输出头部信息内容：{head_dir}")
    # 调用接收文件函数
    recv_file(head_dir, tcp_client)

    # 关闭套接字连接
    tcp_client.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("用户中断操作，正在终止所有线程...")
    except Exception as e:
        print(f"发生错误: {e}")