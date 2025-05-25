import os

def banner():
    """
    打印欢迎信息。
    """
    print('欢迎来到洛圣都')

def start():
    """
    程序的主循环，显示欢迎信息，执行系统命令。
    """
    banner()
    # 执行whoami命令并输出结果
    info = os.system("whoami\n")
    while True:
        # 获取用户输入的命令
        info = input("\n Btea->")
        if info.lower() == 'exit':
            break
        # 执行用户输入的命令
        os.system(info)

if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")