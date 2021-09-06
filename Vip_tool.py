# -*- coding: utf-8 -*-
# @Time    : 2021/8/18 1:21 下午
# @Author  : yujian
# @FileName: Vip_tool.py
# @Software: PyCharm
import logging

import configparser
import queue
import random
import  json
import re
import time
import asyncio
import aiohttp
import requests
from mysqlhelper import MySQLHelper
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
userlist= [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
def get_headers():
    headers={
    'User-Agent':random.choice(userlist),  # 随机更换请求头
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch'
    }
    return headers





class IP():
    def __init__(self,id=None,staticip=None,port=None,attribution=None,status=None):
        self.staticip=staticip
        self.port=port
        self.attribution=attribution
        self.status=status

class Proxy():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('utils/dataconfig.ini')
        self.helper = MySQLHelper(host=config.get("mysql", 'mysqlconnurl'), port=int(config.get("mysql", 'port')),
                             user=config.get("mysql", 'user'), password=config.get("mysql", 'passwd'),
                             database=config.get("mysql", "database"))

    def get_proxy_list(self):
        sql = "select staticip,port,id,status from ipproxy ORDER BY RAND()"
        rs = self.helper.select_all(sql=sql)
        return  rs

    def update_proxy(self,param):
        sql='UPDATE ipproxy SET status = %s ,adsl_ip=%s,attribution =  %s WHERE id = %s '
        rs=self.helper.update(sql=sql,param=param)
        return rs

    def update_status(self,param):
        sql='UPDATE ipproxy SET status =%s  WHERE id = %s '
        rs=self.helper.update(sql=sql,param=param)
        return rs






if __name__ == '__main__':
    #while(True):
        #http://httpbin.org/ip
        #https://www.ip.cn/api/index?ip=&type=0
        proxy=Proxy()
        rs=proxy.get_proxy_list()
        #param=[1, 1]
        #rs1=proxy.update_proxy(param);
        for get_roxies  in  rs:
            ip="http://"+get_roxies[0]+":"+get_roxies[1]
            proxies = {"http": ip,"https":ip}
            param =[]
            headers = {
                'authority': 'www.ip.cn',
                'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.ip.cn/',
                'accept-language': 'zh-CN,zh;q=0.9',
            }
            params = (
                ('ip', ''),
                ('type', '0'),
            )
            try:
                ret = requests.get('https://www.ip.cn/api/index', headers=headers, params=params,proxies=proxies,verify=False,timeout=5)
                # ret = requests.get(url="https://www.ip.cn/api/index?ip=&type=0", headers=headers, proxies=proxies,)
                if ret.status_code == 200:
                    #ret.encoding = ret.apparent_encoding
                    print(ret.text)
                    ipinfo=json.loads(ret.text)
                    param.append(1)
                    param.append(ipinfo['ip'])
                    param.append(ipinfo['address'].replace(' ',''))
                    param.append(get_roxies[2])
                    rs1=proxy.update_proxy(param)
                    print(proxies)
                    print("成功验证状态"+str(rs1))
                elif ret.status_code != 200:
                    if get_roxies[3] != 0:
                        param.append(0)
                        param.append(get_roxies[2])
                        rs2 = proxy.update_status(param)
                        print(ip+"失效ip状态---"+str(rs1))
            except Exception as e:
                if get_roxies[3]!=0:
                    param=[]
                    param.append(0)
                    param.append(get_roxies[2])
                    rs3 = proxy.update_status(param)
                    print(get_roxies[0]+":"+get_roxies[1])
                    print("失效ip状态####"+ str(rs3))







