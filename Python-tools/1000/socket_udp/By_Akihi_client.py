import socket
import uuid
import sys

# 定义一个函数，用于获取设备的 MAC 地址
def get_mac_address():
    # 获取设备的节点 ID 并转换为 UUID 对象，然后取其十六进制字符串的最后 12 位
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    # 将十六进制字符串按每两位一组进行分割，并用冒号连接起来，形成标准的 MAC 地址格式
    return ":".join([mac[e:e + 2] for e in range(0, 12, 2)])

def main():
    try:
        # 获取当前主机的 IP 地址
        ip = socket.gethostbyname(socket.gethostname())
        # 调用 get_mac_address 函数获取 MAC 地址
        mac = get_mac_address()
        # 创建一个 UDP 套接字对象
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 构造包含 IP 地址和 MAC 地址的信息字符串
        info = f"ip addr: {ip}\nmac addr: {mac}"
        # 目标服务器的地址和端口
        server_address = ("127.0.0.1", 8001)

        # 发送包含 IP 和 MAC 地址的信息到服务器
        s.sendto(info.encode(), server_address)
        # 检查命令行是否传入了参数
        if len(sys.argv) > 1:
            # 发送命令行参数到服务器
            s.sendto(sys.argv[1].encode(), server_address)

        # 关闭套接字连接
        s.close()
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()