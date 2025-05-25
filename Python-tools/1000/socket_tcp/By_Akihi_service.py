import socket

def start_server():
    # 创建一个 TCP 套接字对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 绑定服务器地址和端口，'' 表示绑定所有可用的网络接口
        server_socket.bind(('', 8002))
        # 开始监听，最大连接数为 1
        server_socket.listen(1)
        print('监听端口：8002')
        while True:
            # 接受客户端的连接请求，返回一个新的套接字对象和客户端地址
            conn, addr = server_socket.accept()
            print(f'已连接：{addr}')
            try:
                while True:
                    # 从客户端接收数据，最大接收 1024 字节
                    data = conn.recv(1024)
                    if not data:
                        # 如果没有接收到数据，说明客户端已关闭连接
                        break
                    # 解码接收到的数据
                    data = data.decode()
                    print(f'收到消息：{data}')
                    # 获取用户输入，作为要发送给客户端的内容
                    message = input('输入要发送的内容：')
                    # 编码并发送消息给客户端
                    conn.sendall(message.encode())
                    if message.lower() == 'bye':
                        # 如果用户输入 'bye'，则结束通信
                        break
            except Exception as e:
                print(f'通信过程中出现错误：{e}')
            finally:
                # 关闭与客户端的连接
                conn.close()
    except Exception as e:
        print(f'服务器启动失败：{e}')
    finally:
        # 关闭服务器套接字
        server_socket.close()

if __name__ == "__main__":
    start_server()