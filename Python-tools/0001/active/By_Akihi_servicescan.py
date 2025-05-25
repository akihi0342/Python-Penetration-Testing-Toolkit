#!/usr/bin/python3.7
#!coding:utf-8
from optparse import OptionParser
import time
import socket
import re

# 服务特征标志元组，包含协议、服务名称和匹配关键字
SIGNS = (
    # 协议 | 服务名称 | 关键字
    b'FTP|FTP|^220.*FTP',
    b'MySQL|MySQL|mysql_native_password',
    b'oracle-https|^220- ora',
    b'Telnet|Telnet|Telnet',
    b'Telnet|Telnet|^\r\n%connection closed by remote host!\x00$',
    b'VNC|VNC|^RFB',
    b'IMAP|IMAP|^\* OK.*?IMAP',
    b'POP|POP|^\+OK.*?',
    b'SMTP|SMTP|^220.*?SMTP',
    b'Kangle|Kangle|HTTP.*kangle',
    b'SMTP|SMTP|^554 SMTP',
    b'SSH|SSH|^SSH-',
    b'HTTPS|HTTPS|Location: https',
    b'HTTP|HTTP|HTTP/1.1',
    b'HTTP|HTTP|HTTP/1.0',
)

def regex(response, port):
    """
    根据响应内容和端口号识别服务类型
    :param response: 从目标端口获取的响应内容
    :param port: 端口号
    """
    if re.search(b'<title>502 Bad Gateway', response):
        print(f"[{port}] open 服务访问失败!!")
        return
    for pattern in SIGNS:
        protocol, service, keyword = pattern.split(b'|')
        if re.search(keyword, response, re.IGNORECASE):
            print(f"[{port}] open {service.decode()}")
            return
    print(f"[{port}] open 未识别的服务")

def request(ip, port):
    """
    向目标 IP 和端口发送请求并处理响应
    :param ip: 目标 IP 地址
    :param port: 端口号
    """
    response = b''
    # 构造 HTTP 请求
    PROBE = 'GET / HTTP/1.0\r\n\r\n'
    try:
        # 创建 TCP 套接字
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # 设置套接字超时时间
            sock.settimeout(10)
            # 尝试连接目标 IP 和端口
            result = sock.connect_ex((ip, int(port)))
            if result == 0:
                # 若连接成功，发送请求
                sock.sendall(PROBE.encode())
                # 接收响应
                response = sock.recv(256)
                if response:
                    # 调用 regex 函数识别服务类型
                    regex(response, str(port))
    except ConnectionResetError:
        pass
    except Exception as e:
        print(f"连接端口 {port} 时出现错误: {e}")

def main():
    # 创建命令行参数解析器
    parser = OptionParser("用法: %prog -i <目标主机> -p <目标端口>")
    # 获取目标 IP 地址参数
    parser.add_option('-i', type='string', dest='ip', help='指定目标主机')
    # 获取目标端口参数
    parser.add_option('-p', type='string', dest='port', help='指定目标端口，多个端口用逗号分隔')
    # 解析命令行参数
    options, args = parser.parse_args()
    ip = options.ip
    port = options.port
    print(f"扫描报告: {ip}\n")
    # 遍历每个端口
    for port_num in port.split(','):
        request(ip, port_num)
        time.sleep(0.2)
    print("\n扫描完成!...\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("用户中断，终止所有线程...")