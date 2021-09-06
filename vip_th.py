# -*- coding: utf-8 -*-
# @Time    : 2021/8/27 9:39 上午
# @Author  : yujian
# @FileName: vip_th.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2021/8/18 1:21 下午
# @Author  : yujian
# @FileName: Vip_tool.py
# @Software: PyCharm
import datetime
import logging

import configparser
import queue
import random
import json
import re
import threading
import time
import asyncio
import aiohttp
import requests
from mysqlhelper import MySQLHelper
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


proxy_queue =queue.Queue()
class IP():
    def __init__(self, id=None, staticip=None, port=None, status=None):
        self.id=id
        self.staticip = staticip
        self.port = port
        #self.attribution = attribution
        self.status = status


class Proxy():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('utils/dataconfig.ini')
        self.helper = MySQLHelper(host=config.get("mysql", 'mysqlconnurl'), port=int(config.get("mysql", 'port')),
                                  user=config.get("mysql", 'user'), password=config.get("mysql", 'passwd'),
                                  database=config.get("mysql", "database"))

    def get_proxy_list(self, Ip=None):
        sql = "select staticip,port,id,status from ipproxy ORDER BY RAND()"
        rs = self.helper.select_all(sql=sql)
        for item in range(len(rs)):
            proxy_queue.put(rs[item])
        return  proxy_queue
    def get_proxy_list1(self):
        sql = "select staticip,port,id,status from ipproxy ORDER BY RAND()"
        rs = self.helper.select_all(sql=sql)
        return  rs

    def update_proxy(self, param):
        sql = 'UPDATE ipproxy SET status = %s ,adsl_ip=%s,attribution =  %s,updatetime= %s WHERE id = %s  '
        rs = self.helper.update(sql=sql, param=param)
        return rs

    def update_status(self, param):
        sql = 'UPDATE ipproxy SET status =%s  WHERE id = %s '
        rs = self.helper.update(sql=sql, param=param)
        return rs

    def check_proxy(self, proxys):
        param = []
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

        ip = "http://" + proxys[0] + ":" + proxys[1]
        proxies = {"http": ip, "https": ip}
        try:
            ret = requests.get('https://www.ip.cn/api/index', headers=headers, params=params, proxies=proxies,
                               verify=False, timeout=5)
            # ret = requests.get(url="https://www.ip.cn/api/index?ip=&type=0", headers=headers, proxies=proxies,)
            if ret.status_code == 200:
                dtime = datetime.datetime.now()
                un_time = int(time.mktime(dtime.timetuple()))
                print(un_time)
                times = datetime.datetime.fromtimestamp(un_time)
                # ret.encoding = ret.apparent_encoding
                print(ret.text)
                ipinfo = json.loads(ret.text)
                param.append(1)
                param.append(ipinfo['ip'])
                param.append(ipinfo['address'].replace(' ', ''))
                param.append(times)
                param.append(proxys[2])

                rs1 = self.update_proxy(param)
                print(rs1)
                #print(ret.text)
                return rs1
            else:
                if proxys[3] != 0:
                    param.append(0)
                    param.append(proxys[2])
                    rs2 = self.update_status(param)
                    print("失效ip状态" + str(rs2))
                    return 2
        except Exception as e:
            if proxys[3] != 0:
                param = []
                param.append(0)
                param.append(proxys[2])
                rs3 = self.update_status(param)
                print("失效ip状态+++++" + str(rs3))
                return 2
            return 2



class Queue_proxy(threading.Thread):
    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        proxy=Proxy()
        proxy_lists=proxy.get_proxy_list1()
        global proxy_queue
        item=0
        while True:
            try:
                if item <= len(proxy_lists):
                    proxy_queue.put(proxy_lists[item])
                    item=item+1
                else:
                    break
            except IndexError:
                break




class vip_Play(threading.Thread):
    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        global proxy_queue
        while True:
            if proxy_queue.not_empty:
                proxys = proxy_queue.get()
                proxy=Proxy()
                stauts=proxy.check_proxy(proxys)
                #print("{}成功".format(proxys)+"状态:{}".format(str(stauts)))
                time.sleep(2)
                proxy_queue.task_done()
               # print('{}验证结束'.format(proxys))
            else:
                break




if __name__ == '__main__':

        # http://httpbin.org/ip1
        # https://www.ip.cn/api/index?ip=&type=0
        start_time = time.time()  # 开始计时
        mc_thread = Queue_proxy('Queue_proxy')
       # mc_thread.setDaemon(True)  # 设置为守护进程，主线程退出时，子进程也kill掉
        mc_thread.start()  # 启动进程
        for i in range(3):  # 设置线程个数（批量任务时，线程数不必太大，注意内存及CPU负载）
            mp_thread = vip_Play('vip_play')
            #mp_thread.setDaemon(True)
            mp_thread.start()
        proxy_queue.join()











