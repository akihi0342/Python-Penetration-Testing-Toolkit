#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import optparse
from scapy.all import *

# 定义一个函数，用于获取本机的 IP 地址和 MAC 地址
def HostAddress(iface):
    try:
        # 执行 ipconfig /all 命令，并传入指定的网络接口
        ipData = os.popen(f'ipconfig /all {iface}')
        # 读取命令执行结果的所有行
        dataLine = ipData.readlines()

        # 使用正则表达式从结果中搜索 MAC 地址
        mac_match = re.search(r'\w\w-\w\w-\w\w-\w\w-\w\w-\w\w', str(dataLine))
        # 如果找到 MAC 地址，将其赋值给 MAC 变量
        MAC = mac_match.group(0) if mac_match else None

        # 使用正则表达式从结果中搜索 IP 地址
        ip_match = re.search(r'((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)', str(dataLine))
        # 如果找到 IP 地址，将其赋值给 IP 变量
        IP = ip_match.group(0) if ip_match else None

        # 将 IP 地址和 MAC 地址作为元组返回
        return (IP, MAC)
    except Exception as e:
        # 如果发生异常，打印错误信息
        print(f"获取地址信息时出错: {e}")
        return (None, None)

# 定义一个函数，用于进行 ARP 扫描
def ArpScan(iface='eth0'):
    try:
        # 调用 HostAddress 函数获取本机的 MAC 地址
        mac = HostAddress(iface)[1]
        # 调用 HostAddress 函数获取本机的 IP 地址
        ip = HostAddress(iface)[0]

        # 如果未获取到 IP 地址或 MAC 地址，打印错误信息并返回
        if not ip or not mac:
            print("无法获取本机 IP 地址或 MAC 地址，请检查网络接口设置。")
            return

        # 将 IP 地址按点分割成列表
        ipSplit = ip.split('.')
        # 初始化一个空列表，用于存储需要扫描的 IP 地址
        ipList = []

        # 生成需要扫描的 IP 地址列表
        for i in range(1, 255):
            # 拼接 IP 地址
            ipItem = f"{ipSplit[0]}.{ipSplit[1]}.{ipSplit[2]}.{i}"
            # 将拼接好的 IP 地址添加到列表中
            ipList.append(ipItem)

        # 将 MAC 地址的分隔符从 - 替换为 :
        mac = ':'.join(mac.split('-'))

        # 发送 ARP 请求包，并设置超时时间为 2 秒，不显示详细信息
        result = srp(Ether(src=mac, dst='FF:FF:FF:FF:FF:FF')/ARP(op=1, hwsrc=mac, hwdst='00:00:00:00:00:00', pdst=ipList), timeout=2, verbose=False)

        # 获取应答包的结果
        resultAns = result[0].res
        # 初始化一个空列表，用于存储存活主机的信息
        liveHost = []
        # 获取应答包的数量
        number = len(resultAns)

        # 打印扫描结果的标题信息
        print("=====================")
        print("    ARP 探测结果     ")
        print(f"本机 IP 地址: {ip}")
        print(f"本机 MAC 地址: {mac}")
        print("=====================")

        # 遍历应答包结果
        for x in range(number):
            # 获取应答包中的源 IP 地址
            IP = resultAns[x][1][1].fields['psrc']
            # 获取应答包中的源 MAC 地址
            MAC = resultAns[x][1][1].fields['hwsrc']
            # 将存活主机的 IP 地址和 MAC 地址添加到列表中
            liveHost.append([IP, MAC])
            # 打印存活主机的 IP 地址和 MAC 地址
            print(f"IP: {IP}\n\nMAC: {MAC}")
            print("=====================")

        # 打开一个名为 result 的文件，用于存储存活主机的 IP 地址
        with open("result", "w") as resultFile:
            # 遍历存活主机列表
            for host in liveHost:
                # 将存活主机的 IP 地址写入文件，并换行
                resultFile.write(host[0] + "\n")
    except Exception as e:
        # 如果发生异常，打印错误信息
        print(f"扫描过程中出错: {e}")

if __name__ == '__main__':
    # 创建一个命令行参数解析器
    parser = optparse.OptionParser('usage: python %prog -i interfaces \n\n'
                                   'Example: python %prog -i eth0\n')
    # 添加一个命令行参数 -i，用于指定网络接口
    parser.add_option('-i', '--iface', dest='iface', default='', type='string', help='网络接口名称')
    # 解析命令行参数
    (options, args) = parser.parse_args()
    # 调用 ArpScan 函数进行 ARP 扫描
    ArpScan(options.iface)