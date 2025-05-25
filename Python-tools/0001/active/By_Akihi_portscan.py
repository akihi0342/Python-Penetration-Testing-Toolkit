#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import socket
import optparse
import threading
import queue

# 端口扫描类，继承自 threading.Thread
class PortScaner(threading.Thread):
    def __init__(self, port_queue, ip, timeout=3):
        # 调用父类的构造函数
        super().__init__()
        self._port_queue = port_queue
        self._ip = ip
        self._timeout = timeout

    def run(self):
        while True:
            try:
                # 从端口队列中获取端口，超时时间为 0.5 秒
                port = self._port_queue.get(timeout=0.5)
            except queue.Empty:
                # 若队列为空，说明扫描完成，跳出循环
                break
            try:
                # 创建一个 TCP 套接字
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    # 设置套接字的超时时间
                    s.settimeout(self._timeout)
                    # 尝试连接目标 IP 和端口
                    result_code = s.connect_ex((self._ip, port))
                    # 若端口开放，返回码为 0
                    if result_code == 0:
                        print(f"[{port}] OPEN")
            except Exception as e:
                print(f"扫描端口 {port} 时出现错误: {e}")

def start_scan(target_ip, port, thread_num):
    # 初始化端口列表
    port_list = []
    # 判断输入的是单个端口还是端口范围
    if '-' in port:
        start_port, end_port = map(int, port.split('-'))
        port_list.extend(range(start_port, end_port + 1))
    else:
        port_list.append(int(port))
    # 目标 IP 地址
    ip = target_ip
    # 线程列表
    threads = []
    # 端口队列
    port_queue = queue.Queue()
    # 将端口添加到队列中
    for port in port_list:
        port_queue.put(port)
    # 创建并启动线程
    for _ in range(thread_num):
        scanner = PortScaner(port_queue, ip)
        threads.append(scanner)
        scanner.start()
    # 等待所有线程完成
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    # 创建命令行参数解析器
    parser = optparse.OptionParser('示例: python %prog -i 127.0.0.1 -p 80 \n      python %prog -i 127.0.0.1 -p 1-100\n')
    # 目标 IP 参数 -i
    parser.add_option('-i', '--ip', dest='target_ip', default='127.0.0.1', type='string', help='目标 IP')
    # 端口参数 -p
    parser.add_option('-p', '--port', dest='port', default='80', type='string', help='扫描的端口')
    # 线程数量参数 -t
    parser.add_option('-t', '--thread', dest='thread_num', default=100, type='int', help='扫描线程数量')
    # 解析命令行参数
    options, args = parser.parse_args()
    # 开始扫描
    start_scan(options.target_ip, options.port, options.thread_num)