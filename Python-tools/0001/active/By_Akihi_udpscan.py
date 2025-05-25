#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UDP主机存活检测工具
原理：发送UDP包，若收到ICMP不可达响应则说明主机存活
"""

import argparse
import time
from scapy.all import *
from scapy.layers.inet import IP, UDP

# 禁用Scapy的警告输出
conf.verb = 0


def udp_scan(target_ip):
    """
    执行UDP扫描
    :param target_ip: 目标IP地址
    """
    try:
        # 构造目标端口为80的UDP包（通常关闭的端口）
        packet = IP(dst=target_ip) / UDP(dport=80)

        # 发送数据包并等待响应（超时1秒）
        response = sr1(packet, timeout=1, verbose=0)

        if response:
            # 检查是否为ICMP协议响应（协议号1）
            if response.haslayer(IP) and response[IP].proto == 1:
                print(f"[+] 主机 {target_ip} 存活")
            else:
                print(f"[-] 主机 {target_ip} 未存活")
        else:
            # 无响应可能是端口开放或主机不响应
            print(f"[?] 主机 {target_ip} 无响应（可能UDP端口开放）")
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
        description="UDP主机存活扫描工具",
        epilog="示例：python udp_scan.py -i 192.168.1.1-100"
    )
    parser.add_argument("-i", "--ip", required=True,
                        help="指定目标IP或IP范围（格式：192.168.1.1-100）")

    args = parser.parse_args()

    # 遍历所有目标IP进行扫描
    for ip in parse_ip_range(args.ip):
        udp_scan(ip)
        time.sleep(0.2)  # 降低发送频率


if __name__ == "__main__":
    main()