#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TCP ACK主机存活检测工具
原理：发送ACK包，若收到RST响应则说明主机存活
"""

import argparse
import random
import time
from scapy.all import *
from scapy.layers.inet import IP, TCP

# 禁用Scapy的警告输出
conf.verb = 0


def tcp_ack_scan(target_ip):
    """
    执行TCP ACK扫描
    :param target_ip: 目标IP地址
    """
    try:
        # 生成随机目的端口（1-65535）
        dport = random.randint(1, 65535)

        # 构造ACK标志位数据包（flags=0x10表示ACK）
        packet = IP(dst=target_ip) / TCP(flags="A", dport=dport)

        # 发送数据包并等待响应（超时1秒）
        response = sr1(packet, timeout=1, verbose=0)

        if response:
            # 检查响应包是否包含TCP层
            if response.haslayer(TCP):
                # 获取TCP标志位
                flags = response.getlayer(TCP).flags
                # 判断是否包含RST标志
                if flags in ['R', 'RA']:
                    print(f"[+] 主机 {target_ip} 存活")
                else:
                    print(f"[-] 主机 {target_ip} 未存活")
            else:
                print(f"[-] 主机 {target_ip} 响应异常")
        else:
            print(f"[-] 主机 {target_ip} 无响应")
    except Exception as e:
        print(f"[!] 扫描 {target_ip} 时发生错误: {str(e)}")


def parse_ip_range(ip_range):
    """
    解析IP地址范围
    :param ip_range: 用户输入的IP范围（格式：192.168.1.1-100）
    :yield: 生成的IP地址
    """
    if '-' in ip_range:
        base_ip, end = ip_range.split('-', 1)
        octets = base_ip.split('.')
        base_prefix = '.'.join(octets[:3]) + '.'
        start = int(octets[3])
        for i in range(start, int(end) + 1):
            yield f"{base_prefix}{i}"
    else:
        yield ip_range


def main():
    # 配置命令行参数解析
    parser = argparse.ArgumentParser(
        description="TCP ACK主机存活扫描工具",
        epilog="示例：python tcp_ack_scan.py -i 192.168.1.1-100"
    )
    parser.add_argument("-i", "--ip", required=True,
                        help="指定目标IP或IP范围（格式：192.168.1.1-100）")

    args = parser.parse_args()

    # 遍历所有目标IP进行扫描
    for ip in parse_ip_range(args.ip):
        tcp_ack_scan(ip)
        time.sleep(0.2)  # 降低发送频率


if __name__ == "__main__":
    main()