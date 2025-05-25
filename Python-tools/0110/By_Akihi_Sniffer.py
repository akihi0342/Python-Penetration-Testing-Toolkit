#!/usr/bin/python3
# -*- coding: utf-8 -*-

from scapy.all import *
import time
import optparse

# 时间戳转换函数，将时间戳转换为可读的日期时间格式
def timestamp_to_time(timestamp):
    time_tmp = time.localtime(timestamp)
    my_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tmp)
    return my_time

# 回调打印函数，用于处理捕获到的数据包
def packet_callback(packet):
    try:
        print("*" * 30)
        # 打印源IP，源端口，目的IP，目的端口
        print(f"[{timestamp_to_time(packet.time)}]Source:{packet[IP].src}:{packet.sport}--->Target:{packet[IP].dst}:{packet.dport}")
        # 打印输出数据包详细信息
        print(packet.show())
        print("*" * 30)
    except IndexError:
        # 处理没有IP层或端口信息的数据包
        pass

if __name__ == '__main__':
    parser = optparse.OptionParser("Example:python %prog -i 127.0.0.1 -c 5 -o ms08067.pcap\n")
    # 添加IP参数 -i
    parser.add_option('-i', '--IP', dest='host_ip',
                      default="127.0.0.1", type='string',
                      help='IP address [default = 127.0.0.1]')
    # 添加数据包总数参数 -c
    parser.add_option('-c', '--count', dest='packet_count',
                      default=5, type='int',
                      help='Packet count [default = 5]')
    # 添加保存文件名参数 -o
    parser.add_option('-o', '--output', dest='file_name',
                      default="ms08067.pcap", type='string',
                      help='save filename [default = ms08067.pcap]')
    (options, args) = parser.parse_args()
    # 过滤规则，只捕获目标IP的数据包
    def_filter = f"dst {options.host_ip}"
    # 开始嗅探数据包
    packets = sniff(filter=def_filter, prn=packet_callback, count=options.packet_count)
    # 保存输出文件
    wrpcap(options.file_name, packets)