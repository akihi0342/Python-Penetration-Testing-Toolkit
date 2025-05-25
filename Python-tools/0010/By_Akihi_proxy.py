# urllib代理设置
# 导入必要的模块
# from urllib.error import URLError
# from urllib.request import ProxyHandler, build_opener

# 定义代理地址
# proxy = '127.0.0.1:1087'  # 代理地址
# proxy = 'username:password@IP:port'
# proxy_handler = ProxyHandler({
#     'http': 'http://' + proxy,
#     'https': 'https://' + proxy
# })
# opener = build_opener(proxy_handler)
# try:
#     response = opener.open('http://httpbin.org/get')  # 测试ip的网址
#     print(response.read().decode('utf-8'))
# except URLError as e:
#     print(e.reason)

# requests代理设置
# 导入requests模块
import requests

# 定义代理地址
# proxy = '127.0.0.1:1087'  # 代理地址
# proxies = {
#     'http': 'http://' + proxy,
#     'https': 'https://' + proxy
# }
# try:
#     response = requests.get('http://httpbin.org/get', proxies=proxies)
#     print(response.text)
# except requests.exceptions.ConnectionError as e:
#     print('error:', e.args)

# from selenium import webdriver
# proxy = '127.0.0.1:1087'
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=http://' + proxy)
# browser = webdriver.Chrome(chrome_options=chrome_options)
# browser.get('http://httpbin.org/get')

# 代理爬虫
import json
import time
from datetime import datetime, timedelta

# 定义获取数据的函数
def get_data(url):
    # 定义代理地址
    proxy = '127.0.0.1:1087'
    # 构建代理字典
    proxies = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    }
    # 定义请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
    try:
        # 打印请求的URL
        print(url)
        # 发送请求，设置超时时间为3秒
        response = requests.get(url, headers=headers, proxies=proxies, timeout=3)
        # 检查响应状态码是否为200
        if response.status_code == 200:
            # 打印响应内容
            print(response.text)
            return response.text
        return None
    except requests.exceptions.ConnectionError as e:
        # 打印连接错误信息
        print('error:', e.args)

# 定义解析数据的函数
def parse_data(html):
    try:
        # 将JSON字符串解析为Python字典
        data = json.loads(html)['cmts']
        comments = []
        for item in data:
            # 构建评论字典
            comment = {
                'id': item['id'],
                'nickName': item['nickName'],
                'cityName': item.get('cityName', ''),
                'content': item['content'].replace('\n', ' ', 10),
                'score': item['score'],
                'startTime': item['startTime']
            }
            comments.append(comment)
        return comments
    except (KeyError, json.JSONDecodeError):
        return []

# 定义保存数据到文本文件的函数
def save_to_txt():
    # 获取当前时间并格式化为字符串
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(start_time)
    # 定义结束时间
    end_time = '2018-08-10 00:00:00'
    while start_time > end_time:
        # 构建请求URL
        url = f'http://m.maoyan.com/mmdb/comments/movie/1203084.json?_v_=yes&offset=0&startTime={start_time.replace(" ", "%20")}'
        try:
            # 调用get_data函数获取数据
            html = get_data(url)
        except Exception as e:
            # 出现异常时，等待0.5秒后重试
            time.sleep(0.5)
            html = get_data(url)
        else:
            # 没有异常时，等待0.1秒
            time.sleep(0.1)

        # 调用parse_data函数解析数据
        comments = parse_data(html)
        print(comments)
        if comments:
            # 获取末尾评论的时间
            start_time = comments[14]['startTime']
            # 将时间字符串转换为datetime对象
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            # 时间减去1秒
            start_time = start_time + timedelta(seconds=-1)
            # 将datetime对象转换为字符串
            start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')

            for item in comments:
                # 将评论信息写入文本文件
                with open('data.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{item['id']},{item['nickName']},{item['cityName']},{item['content']},{item['score']},{item['startTime']}\n")

if __name__ == '__main__':
    # 调用保存数据到文本文件的函数
    save_to_txt()