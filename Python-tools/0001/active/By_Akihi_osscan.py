#!/usr/bin/python3.7
#!coding:utf-8
import os
import re
import argparse

# 定义TTL扫描函数，用于根据目标主机响应包中的TTL值判断操作系统类型
def ttl_scan(ip):
    # 编译正则表达式，用于匹配TTL信息
    ttl_str_match = re.compile(r'TTL=\d+')
    ttl_num_match = re.compile(r'\d+')
    try:
        # 执行ping命令并获取输出
        result = os.popen(f"ping -n 1 {ip}")
        res = result.read()
        for line in res.splitlines():
            # 查找包含TTL信息的行
            result = ttl_str_match.findall(line)
            if result:
                # 提取TTL值
                ttl = ttl_num_match.findall(result[0])
                if int(ttl[0]) <= 64:
                    # TTL值小于等于64，判断为Linux/Unix系统
                    print(f"{ip} 是 Linux/Unix 系统")
                else:
                    # 否则判断为Windows系统
                    print(f"{ip} 是 Windows 系统")
    except Exception as e:
        print(f"扫描 {ip} 时发生错误: {e}")

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="根据TTL值扫描目标主机的操作系统类型")
    # 添加IP地址参数
    parser.add_argument('-i', type=str, dest='IP', help='指定目标主机的IP地址')
    args = parser.parse_args()
    ip = args.IP
    if ip:
        # 调用TTL扫描函数
        ttl_scan(ip)
    else:
        print("请提供目标主机的IP地址，使用 -i 参数。")

if __name__ == "__main__":
    main()