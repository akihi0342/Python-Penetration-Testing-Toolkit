import socket

def start_client():
    # 创建一个 TCP 套接字对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 尝试连接到服务器
        client_socket.connect(('127.0.0.1', 8002))
        while True:
            # 获取用户输入，作为要发送给服务器的内容
            message = input('输入要发送的内容：')
            # 编码并发送消息给服务器
            client_socket.sendall(message.encode())
            # 从服务器接收数据，最大接收 1024 字节
            data = client_socket.recv(1024)
            if not data:
                # 如果没有接收到数据，说明服务器已关闭连接
                break
            # 解码接收到的数据
            data = data.decode()
            print(f'收到消息：{data}')
            if message.lower() == 'bye':
                # 如果用户输入 'bye'，则结束通信
                break
    except ConnectionRefusedError:
        print('服务器未找到或未开启')
    except Exception as e:
        print(f'客户端出现错误：{e}')
    finally:
        # 关闭客户端套接字
        client_socket.close()

if __name__ == "__main__":
    start_client()