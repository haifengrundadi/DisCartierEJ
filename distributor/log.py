# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""小红书日志模块"""
import os
import logging.config
import yaml

# 项目路径抽象
PROJECT_PATH = os.path.dirname(os.path.abspath('.'))

RESOURCE_PATH = os.path.join(PROJECT_PATH, "resources")

_LOGGER_CONFIG_PATH = os.path.join(RESOURCE_PATH, "logger_config.yml")

_LOG_FILE_DIRECTORY = os.path.join(RESOURCE_PATH, "logs")

# 如果文件不存在，创建文件目录
if not os.path.exists(_LOG_FILE_DIRECTORY):
    os.mkdir(_LOG_FILE_DIRECTORY)

with open(_LOGGER_CONFIG_PATH, 'r') as f:
    log_config = yaml.load(f)
logging.config.dictConfig(log_config['logging'])

# 全局变量
LOGGER = logging.getLogger('')

if __name__ == '__main__':
    LOGGER.info("Root logger")
