#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/12
# @Author : yujian
import logging.config
import os


def get_logger(name, log_config=None, log_level='DEBUG'):
    """
    logger
    :param name: 模块名称
    :param log_file: 日志文件，如无则输出到标准输出
    :param log_level: 日志级别
    :return:
    """
    if log_config is None:
        logger = logging.getLogger(name)
        formatter = logging.Formatter('[%(levelname)7s %(asctime)s %(module)s:%(lineno)4d] %(message)s',
                                      datefmt='%Y%m%d %I:%M:%S')
        handle = logging.StreamHandler()
        handle.setFormatter(formatter)
        logger.addHandler(handle)
    else:
        # 读取日志配置文件内容
        logging.config.fileConfig(log_config)
        # 创建一个日志器logger
        logger = logging.getLogger(name)
    logger.setLevel(log_level.upper())
    return logger


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_config = os.path.join(project_dir, 'logging.config')
#logger = get_logger("fileLogger", log_config=None, log_level='DEBUG')
logger = get_logger("verifyIP", log_config=None, log_level='info')

def set_log_level(log_level='INFO'):
    logger.setLevel(log_level.upper())


if __name__ == '__main__':
    for _ in range(10):
        logger.debug('hi')
        logger.info('hi')
        logger.error('hi')
        logger.warning('hi')
        set_log_level('info')
        logger.debug('hi')  # ignore
        logger.info('hi')
        logger.error('hi')
        logger.warning('hi')
        logger.warning('ddddddddddddddddddddddddd')