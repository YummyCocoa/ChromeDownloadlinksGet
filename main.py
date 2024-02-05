import re

import requests
from bs4 import BeautifulSoup
import json


def make_windows_url(html):
    titles = re.findall(r'<h3 class="ui floated header">(.*?)<span class="sub header"', html, re.S)
    links = re.findall(r'<a class="ui positive button" href="(.*?)"', html)
    versions = re.findall(r'<span class="sub header" style="margin-top:8px">最新版本：<code style="color:#e6783d">(.*?)</code>', html,re.S)
    sha1 = re.findall(r'<p style="color: #999">SHA1：<code>(.*?)</code></p>',html)
    temp_data = {}

    for i in range(len(titles)):
        title = titles[i].strip()
        x64 = '64' in title
        link = links[i].strip()
        version = versions[i].strip() + ('_x64' if x64 else "")
        sha = sha1[i].strip()
        temp_data[version] = {
            'tag': title,
            'link': link,
            'sha': sha
        }
    return temp_data


url = 'https://www.iplaysoft.com/tools/chrome/'
payload = {}
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Referer": "https://link.zhihu.com/?target=https%3A//www.ipla",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
}
resp = requests.get(url, headers=headers, data=payload, timeout=10)

data = {}

soup = BeautifulSoup(resp.text, 'html.parser')

# 解析Windows版本
win_block = soup.find('div', id='result_win')
data['Windows'] = make_windows_url(str(win_block))

# 解析Windows7版本
win7_block = soup.find('div', id='result_win7')
data['Windows7'] = make_windows_url(str(win7_block))

# 解析macOS版本
mac_block = soup.find('div', id='result_mac')
data['macOS'] = make_windows_url(str(mac_block))

# 将数据保存为JSON文件
with open('chrome_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
