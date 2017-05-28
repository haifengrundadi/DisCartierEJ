#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from stf_selector.selector import Selector, where
import constant as v

logger = logging.getLogger(__name__)


def get_stf_in_use_devices():
    """
    获取正在使用的设备
    """
    http_stf = Selector(url=v.STF_URL, token=v.TOKEN)
    http_stf.load()
    in_use_list = http_stf.find((where("using").exists())
                                & (where("abi").exists())
                                & (where('using') == True)).devices()
    logger.info("in_use_list: " + str(len(in_use_list)))
    return in_use_list


def get_stf_un_use_devices(cond=None):
    """
    获取没有使用的设备
    """
    logging.info("get devices from stf platform.")
    http_stf = Selector(url=v.STF_URL, token=v.TOKEN)
    http_stf.load()
    cond_init = (where("present").exists()) \
                & (where("abi").exists())\
                & (where("using").exists())\
                & (where('present') == True)\
                & (where('using') == False)

    if cond is not None:
        cond_init &= cond

    un_use_list = http_stf.find(cond_init).devices()
    logger.info("un_use_list: " + str(len(un_use_list)))
    return un_use_list


def desired_caps_list():
    """
    连接stf进行获取所需要的信息
    """
    desr_caps_list = []
    un_use_list = get_stf_un_use_devices()
    if un_use_list is not None and len(un_use_list):
        for device in un_use_list:
            print device
            if device.get('remoteConnectUrl') is not None:
                url = device['remoteConnectUrl']
            else:
                url = device['display']['url'][5:]
            port = int(url[-4:])
            if port % 2 == 0:
                port += 1
            else:
                pass
            url = url[:-5] + ":" + str(port)
            desired_caps = {}
            desired_caps['platformName'] = v.PLATFORMNAME
            desired_caps['platformVersion'] = device.get('version')
            desired_caps['app'] = v.APP_PATH
            desired_caps['deviceName'] = url
            desired_caps['newCommandTimeout'] = v.TIMEOUT
            desired_caps['serial'] = device.get('serial')
            desr_caps_list.append(desired_caps)
        return desr_caps_list
    else:
        logger.info(u"没有可用设备")
        return None


def docker_composes_data():
    """
    得到docker-compose的信息
    """
    logger.info("get docker-composes data use devices info.")
    docker_composes_list = []
    un_use_list = get_stf_un_use_devices()
    if un_use_list is not None and len(un_use_list):
        for device in un_use_list:
            if device.get('remoteConnectUrl') is not None:
                url = device['remoteConnectUrl']
            else:
                url = device['display']['url'][5:]
            port = int(url[-4:])
            if port % 2 == 0:
                port += 1
            else:
                pass
            url = url[:-5] + ":" + str(port)
            docker_compose_data = {}
            """下面这些数据可以放到配置文件里"""
            docker_compose_data['APPIUM_CARTIER_IMAGE'] = v.APPIUM_CARTIER_IMAGE
            docker_compose_data['APK_NAME'] = v.APK_NAME
            docker_compose_data['PORTS'] = 4723
            docker_compose_data['APPIUM_CARTIER_CMD'] = v.APPIUM_CARTIER_CMD
            docker_compose_data['APP_APK_VOLUMES'] = v.APP_APK_VOLUMES
            docker_compose_data['DOCKCOMPOSE_VOLUMES'] = v.DOCKCOMPOSE_VOLUMES
            docker_compose_data["APPIUM_CARTIER_LOGS_VOLUMES"] = v.APPIUM_CARTIER_LOGS_VOLUMES
            docker_compose_data['PLATFORM_VERSION'] = device.get('version')
            docker_compose_data['APP_NAME'] = v.APP_PATH
            docker_compose_data['DEVICES_NAME'] = url
            docker_compose_data['SERIAL'] = device.get('serial')
            docker_compose_data['CASE_NAME'] = v.CASE_NAME
            docker_composes_list.append(docker_compose_data)
        return docker_composes_list
    else:
        logger.info(u"没有可用设备")
        return None


def disconnectRemoteSession(serial=None):
    """
    当程序结束时，结束对远程手机的占用
    """
    if serial is None:
        logger.info("no device to disconnect")
    else:
        logger.info("Disconnect device remote session "+str(serial))
        cmd = 'curl -X DELETE -H "Authorization: Bearer ' + v.TOKEN + \
              '" ' + v.STF_DELETE_URL + serial
        try:
            os.system(cmd)
        except Exception as err:
            logger.error(err)


if __name__ == "__main__":
    disconnectRemoteSession("cdf1b667")