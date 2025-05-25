import socket

def main():
    try:
        # 创建一个 UDP 套接字对象
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 绑定到本地的 8001 端口，接受所有地址的连接
        s.bind(('', 8001))
        print("服务器已启动，等待数据...")

        while True:
            # 接收来自客户端的数据和客户端地址
            data, addr = s.recvfrom(1024)
            # 解码接收到的数据
            message = data.decode()
            # 打印接收到的数据
            print(message)
            # 如果接收到的消息是 'exit'，则退出循环
            if message.lower() == 'exit':
                break

        # 关闭套接字连接
        s.close()
        print("服务器已关闭。")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()