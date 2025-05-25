#! /usr/bin/env python
#-*- coding:utf-8 -*-
import sys
import getopt
import requests
from bs4 import BeautifulSoup
import re
import time
import threading

# 打印欢迎信息
def banner():
    print('欢迎来到德莱联盟')

# 打印使用规则并退出程序
def usage():
    print('-h: --help 显示帮助信息;')
    print('-u: --url  指定域名;')
    print('-p: --pages 指定搜索页数;')
    print('示例: python emailcheck.py -u "www.baidu.com" -p 100' + '\n')
    sys.exit()

# 主函数，处理输入参数并启动程序
def start(argv):
    url = ""
    pages = ""
    # 检查是否提供了足够的参数
    if len(sys.argv) < 2:
        print("-h 查看帮助信息;\n")
        sys.exit()
    try:
        banner()
        # 解析命令行参数
        opts, args = getopt.getopt(argv, "u:p:h")
    except getopt.GetoptError:
        print('参数输入错误!')
        sys.exit()
    for opt, arg in opts:
        if opt == "-u":
            url = arg
        elif opt == "-p":
            pages = arg
        elif opt == "-h":
            usage()
    # 启动线程处理
    threader(url, pages)

# 自定义线程类，用于获取线程执行结果
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        if self.args[1] < 1:
            return
        # 执行函数并保存结果
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

# 线程管理器，启动漏洞检测
def threader(url, pages):
    launcher(url, pages)

# 漏洞检测启动函数，遍历指定页数
def launcher(url, pages):
    if not pages:
        return
    for page in range(1, int(pages) + 1):
        keyword(url, page)

# 对每个关键字启动线程搜索邮箱
def keyword(url, page):
    threads = []
    email_sum = []
    email_num = []
    # 定义搜索关键字列表
    key_words = ['email', 'mail', 'mailbox', '邮件', '邮箱', 'postbox']
    for key_word in key_words:
        # 创建线程
        t = MyThread(emails, args=(url, page, key_word))
        t.start()
        threads.append(t)
    for t in threads:
        # 等待线程执行完毕
        t.join()
        result = t.get_result()
        if result:
            email_num.append(result)
    for email_list in email_num:
        for email in email_list:
            if email not in email_sum:
                email_sum.append(email)
                print(email)

# 结合Bing和百度搜索结果
def emails(url, page, key_word):
    bing_emails = bing_search(url, page, key_word)
    baidu_emails = baidu_search(url, page, key_word)
    return bing_emails + baidu_emails

# 使用Bing搜索引擎搜索邮箱
def bing_search(url, page, key_word):
    referer = "http://cn.bing.com/search?q=email+site%3abaidu.com&qs=n&sp=-1&pq=emailsite%3abaidu.com&first=1&FORM=PERE1"
    conn = requests.session()
    # 构建Bing搜索URL
    bing_url = f"http://cn.bing.com/search?q={key_word}+site%3a{url}&qs=n&sp=-1&pq={key_word}site%3a{url}&first={(page - 1) * 10}&FORM=PERE1"
    conn.get('http://cn.bing.com', headers=headers(referer))
    try:
        r = conn.get(bing_url, stream=True, headers=headers(referer), timeout=8)
        return search_email(r.text)
    except requests.RequestException:
        return []

# 使用百度搜索引擎搜索邮箱
def baidu_search(url, page, key_word):
    email_list = []
    referer = "https://www.baidu.com/s?wd=email+site%3Abaidu.com&pn=1"
    # 构建百度搜索URL
    baidu_url = f"https://www.baidu.com/s?wd={key_word}+site%3A{url}&pn={(page - 1) * 10}"
    conn = requests.session()
    conn.get(referer, headers=headers(referer))
    try:
        r = conn.get(baidu_url, headers=headers(referer))
        soup = BeautifulSoup(r.text, 'lxml')
        tagh3 = soup.find_all('h3')
        for h3 in tagh3:
            href = h3.find('a').get('href')
            try:
                r = requests.get(href, headers=headers(referer), timeout=8)
                emails = search_email(r.text)
                email_list.extend(emails)
            except requests.RequestException:
                continue
    except requests.RequestException:
        pass
    return email_list

# 从HTML文本中提取邮箱地址
def search_email(html):
    return re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", html, re.I)

# 生成请求头
def headers(referer):
    return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'Referer': referer
    }

if __name__ == '__main__':
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("用户中断操作，正在终止所有线程...")