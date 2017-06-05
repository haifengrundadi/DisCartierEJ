# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    DisCartierEJ log module

    @author Juan Liu
    @date 2017.06.01
"""
import os
import logging.config
import yaml

PROJECT_PATH = os.path.dirname(os.path.abspath('.'))

RESOURCE_PATH = os.path.join(PROJECT_PATH, "resources")

_LOGGER_CONFIG_PATH = os.path.join(RESOURCE_PATH, "logger_config.yml")

_LOG_FILE_DIRECTORY = os.path.join(RESOURCE_PATH, "logs")

if not os.path.exists(_LOG_FILE_DIRECTORY):
    os.mkdir(_LOG_FILE_DIRECTORY)

# load log config
with open(_LOGGER_CONFIG_PATH, 'r') as f:
    log_config = yaml.load(f)

logging.config.dictConfig(log_config['logging'])
LOGGER = logging.getLogger('')

if __name__ == '__main__':
    LOGGER.info("Root logger")
