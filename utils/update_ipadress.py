# -*- coding: utf-8 -*-
# @Time    : 2021/3/22 2:40 下午
# @Author  : yujian
# @FileName: update_ipadress.py
# @Software: PyCharm
from qqwry import updateQQwry
import os
if __name__ == '__main__':
    #https://github.com/animalize/qqwry-python3
    filename=os.path.abspath(os.path.dirname(__file__))
    filename1=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+'/qqwry.dat'
    print(filename1)
    ret = updateQQwry(filename1)
    print(ret)