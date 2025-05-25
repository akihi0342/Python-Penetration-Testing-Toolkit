# -*- coding:utf-8 -*-
import socket
import sys
import getopt

# 打印欢迎信息
def banner():
    print('欢迎来到地狱')

# 打印使用规则并退出程序
def usage():
    print('-h: --help 帮助;')
    print('-p: --port 端口')
    print('-u: --url  域名;')
    print('-s: --type Redis')
    sys.exit()

# 检测Redis未授权访问
def redis_unauthored(url, port):
    result = []
    # 创建一个TCP套接字
    s = socket.socket()
    # Redis INFO命令的十六进制编码
    payload = "\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a"
    # 设置套接字超时时间为10秒
    socket.setdefaulttimeout(10)
    for ip in url:
        try:
            # 尝试连接到指定IP和端口
            s.connect((ip, int(port)))
            # 发送INFO命令
            s.sendall(payload.encode())
            # 接收服务器响应
            recvdata = s.recv(1024).decode()
            if recvdata and 'redis_version' in recvdata:
                # 如果响应中包含redis_version，说明存在未授权访问
                result.append(f'{ip}:{port}:\033[1;32;40msuccess\033[0m')
        except:
            # 连接失败或其他异常，标记为失败
            result.append(f'{ip}:{port}:\033[1;31;40mfailed \033[0m')
        finally:
            # 关闭套接字连接
            s.close()
    return result

# 生成IP地址列表
def url_list(li):
    ss = []
    i = 0
    j = 0
    zi = []
    for s in li:
        a = s.find('-')
        i = i + 1
        if a != -1:
            ss = s.rsplit("-")
            j = i
            break
    for s in range(int(ss[0]), int(ss[1]) + 1):
        li[j - 1] = str(s)
        aa = ".".join(li)
        zi.append(aa)
    return zi

# 处理URL，生成IP地址列表
def url_exec(url):
    i = 0
    zi = []
    group = []
    group1 = []
    group2 = []
    li = url.split(".")
    if url.find('-') == -1:
        group.append(url)
        zi = group
    else:
        for s in li:
            a = s.find('-')
            if a != -1:
                i = i + 1
        zi = url_list(li)
        if i > 1:
            for li in zi:
                zz = url_list(li.split("."))
                for ki in zz:
                    group.append(ki)
            zi = group
            i = i - 1
        if i > 1:
            for li in zi:
                zzz = url_list(li.split("."))
                for ki in zzz:
                    group1.append(ki)
            zi = group1
            i = i - 1
        if i > 1:
            for li in zi:
                zzzz = url_list(li.split("."))
                for ki in zzzz:
                    group2.append(ki)
            zi = group2
    return zi

# 主函数，解析命令行参数并启动程序
def start(argv):
    thread = 1
    url = ""
    type_ = ""
    port = ""
    if len(sys.argv) < 2:
        print("-h 帮助信息;\n")
        sys.exit()
    try:
        banner()
        # 解析命令行参数
        opts, args = getopt.getopt(argv, "-u:-p:-s:-h")
    except getopt.GetoptError:
        print('Error an argument!')
        sys.exit()
    for opt, arg in opts:
        if opt == "-u":
            url = arg
        elif opt == "-s":
            type_ = arg
        elif opt == "-p":
            port = arg
        elif opt == "-h":
            usage()
    launcher(url, type_, port)

# 输出检测结果
def output_exec(output, type_):
    print(f"\033[1;32;40m{type_}......\033[0m")
    print("++++++++++++++++++++++++++++++++++++++++++++++++")
    print("|         ip         |    port   |     status  |")
    for li in output:
        print("+-----------------+-----------+--------------+")
        print(f"|   {li.replace(':', '   |    ')}  | ")
    print("+----------------+------------+---------------+\n")
    print("[*] shutting down....")

# 漏洞检测启动函数
def launcher(url, type_, port):
    # 检测Redis未授权访问
    if type_ == "Redis":
        output = redis_unauthored(url_exec(url), port)
        output_exec(output, type_)

if __name__ == '__main__':
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")