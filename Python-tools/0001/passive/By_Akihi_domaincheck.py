#! /usr/bin/env python
# _*_  coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys

# 使用Bing搜索引擎搜索子域名
def bing_search(site, pages):
    subdomains = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'referer': "http://cn.bing.com/search?q=email+site%3abaidu.com&qs=n&sp=-1&pq=emailsite%3abaidu.com&first=2&FORM=PERE1"
    }
    for i in range(1, int(pages) + 1):
        # 构建Bing搜索URL
        url = f"https://cn.bing.com/search?q=site%3a{site}&go=Search&qs=ds&first={(i - 1) * 10}&FORM=PERE"
        conn = requests.session()
        conn.get('http://cn.bing.com', headers=headers)
        try:
            html = conn.get(url, stream=True, headers=headers, timeout=8)
            soup = BeautifulSoup(html.content, 'html.parser')
            job_bt = soup.findAll('h2')
            for h2 in job_bt:
                link = h2.a.get('href')
                print(link)
                domain = f"{urlparse(link).scheme}://{urlparse(link).netloc}"
                if domain not in subdomains:
                    subdomains.append(domain)
                    print(domain)
        except requests.RequestException:
            continue
    return subdomains

if __name__ == '__main__':
    if len(sys.argv) == 3:
        site = sys.argv[1]
        page = sys.argv[2]
    else:
        print(f"使用方法: {sys.argv[0]} 域名 页数")
        sys.exit(-1)
    subdomains = bing_search(site, page)