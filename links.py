"""
Created on Tue Sep  6 09:13:22 2017

@author: 分c君_BingWong
blog：www.fenc.cc
"""

import requests
from requests.exceptions import RequestException
import re
import json

#先用status_code是否等于200判断能否解析到target的html，返回html code
def get_links(url):
    try:
        response = requests.get(url)
        response.encoding = 'gbk'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#用于获取首页指定的某区域中的超链接        
def parse_one_page(url, html):
    pattern = re.compile('<div class="type.*?<a style.*?href="(.*?)".*?>(.*?)</a>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        detail_link = url + item[0]
        for i in parse_detail_page(detail_link):
            print(i)
            write_to_file(i)
            
#获取首页指定的某区域中的超链接后，再进入超链接的页面获取特定的信息        
def parse_detail_page(url):
    detail_html = get_links(url)
    pattern = re.compile('<li>.*?href="(.*?)">(.*?)</a>.*?</li>', re.S)
    items = re.findall(pattern, detail_html)
    
    #这里的yield的用法跟return差不多，不过yield只生成一次，不存储在内存里
    for item in items:
        yield{
            'name': item[1],
            'link': item[0],
        }

#用于写入并保存数据到json文件
def write_to_file(content):
    with open('result.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()
       
def main():
    url = 'http://www.capitalmarket.cn/'
    html = get_links(url)
    parse_one_page(url, html)

if __name__ == '__main__':
    main()