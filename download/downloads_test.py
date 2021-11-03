# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2021/11/3
description:下载远程文件保存到本地，需要配置下载的源地址（url）和保存地址（save_path)
'''
from typing import List

import requests
import time
import bs4


def get_links(url: str) -> List[str]:
    '''
        获取文件的下载地址
    Args:
        url: url路径

    Returns:
        下载文件的地址
    '''
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    links = []
    for k in soup.find_all('a'):
        if "href" in str(k) and "download" in str(k):
            # 查a标签的href值
            links.append("https://d.shikey.com" + k['href'])
    return links


def save_file_to_local(path: str, save_path: str = 'd://course/') -> None:
    '''
        保存远程的文件流到本地
    Args:
        path: 文件地址
        save_path: 保存文件的目标

    Returns:
        None
    '''
    lines = get_links(path)
    for line in lines:
        try:
            url = line.strip('\n')
            r = requests.get(url)
            path = save_path + url.split("/")[-1]
            with open(path, "wb") as code:
                code.write(r.content)
                print("downloads file over,please waiting next one!")
        except Exception:
            print('download exception.')
    print('already downloaded all files')


if __name__ == '__main__':
    start = time.time()
    # 源下载地址
    url = 'https://d.shikey.com/jike/%E6%9E%81%E5%AE%A2%E6%97%B6%E9%97%B4%E5%B7%B2%E5%AE%8C%E7%BB%93/52%20%E4%BB%A3%E7%A0%81%E7%B2%BE%E8%BF%9B%E4%B9%8B%E8%B7%AF/pdf/'
    # 保存本地地址
    save_path = 'd://course/code/'
    save_file_to_local(url, save_path)
    end = time.time()
    print("download time:" + str(end - start) + "s")
