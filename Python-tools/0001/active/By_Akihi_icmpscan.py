#!/usr/bin/python
#coding:utf-8
from scapy.all import *
from random import randint
import argparse
import time

# 定义扫描函数，用于向目标IP发送ICMP请求并根据响应判断主机状态
def Scan(ip):
    try:
        # 生成随机的IP ID、ICMP ID和ICMP序列号
        ip_id = randint(1, 65535)
        icmp_id = randint(1, 65535)
        icmp_seq = randint(1, 65535)
        # 构造ICMP数据包
        packet = IP(dst=ip, ttl=64, id=ip_id)/ICMP(id=icmp_id, seq=icmp_seq)/b'rootkit'
        # 发送数据包并等待响应，超时时间为1秒
        result = sr1(packet, timeout=1, verbose=False)
        if result:
            # 获取响应数据包中的源IP地址
            scan_ip = result[IP].src
            print(f"{scan_ip} ---> 主机处于开启状态")
        else:
            print(f"{ip} ---> 主机处于关闭状态")
    except Exception as e:
        print(f"扫描 {ip} 时发生错误: {e}")

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="使用ICMP协议扫描目标主机的状态")
    # 添加IP地址参数
    parser.add_argument('-i', type=str, dest='IP', help='指定目标主机的IP地址，可以是单个IP或IP范围（如192.168.1.1-120）')
    args = parser.parse_args()
    ip = args.IP
    if ip:
        print(f"开始扫描 {ip} ...\n")
        # 判断是否为IP范围
        if '-' in ip:
            try:
                # 分割IP范围
                start_ip = ip.split('-')[0]
                end_ip = int(ip.split('-')[1])
                start_last_octet = int(start_ip.split('.')[3])
                base_ip = '.'.join(start_ip.split('.')[:3])
                # 循环扫描IP范围内的所有主机
                for i in range(start_last_octet, end_ip + 1):
                    target_ip = f"{base_ip}.{i}"
                    Scan(target_ip)
                    time.sleep(0.2)
            except ValueError:
                print("IP范围格式错误，请使用正确的格式，如192.168.1.1-120。")
        else:
            # 扫描单个IP
            Scan(ip)
        print("\n扫描完成！\n")
    else:
        print("请提供目标主机的IP地址，使用 -i 参数。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("用户中断扫描，正在终止所有线程...")