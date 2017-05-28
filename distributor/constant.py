#!/usr/bin/env python
# -*- coding: utf-8 -*-

LOCAL_LOG_DIR = "/Users/red/tmp/logs/"

# 需要将apk拷入到container内， 也可以再做image的时候，直接进行从网站下下载（最好的方法）
# 但是目前的"https://fir.im/viphk"还不支持
APP_PATH = "/apk_shell/com.xingin.xhs_4.19.024_419024.apk"
STF_URL = "http://10.12.144.16:7100/api/v1/devices"
TOKEN = "3e5dd447cd334d549c849d19707eb269df74cabd67e5400986a5240023af6421"
STF_DELETE_URL = STF_URL + "/user/devices/"

PLATFORMNAME = 'Android'
TIMEOUT = 60

# 生产docker-compose的时候需要的一些配置信息
APPIUM_CARTIER_IMAGE = "suifengdeshitou/appium-cartier-docker:red"
APK_NAME = 'com.xingin.xhs_4.19.024_419024.apk'
PORTS = 4723
APPIUM_CARTIER_CMD = "bash /app_shell/app.sh"
APP_APK_VOLUMES = "/Users/red/temp/appium:/apk_shell"
DOCKCOMPOSE_VOLUMES = "/Users/red/PycharmProjects/cartier_distributor/resources/dockercomposes/"
APPIUM_CARTIER_LOGS_VOLUMES = LOCAL_LOG_DIR + 'RANDOM:/opt/node/cartier/logs'  # RANDOM为变量在生成的过程中替换

# 要运行的case
CASE_NAME = "test_purchase_good.py"