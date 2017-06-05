#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from collections import defaultdict
from stf_selector.selector import Selector
import config as v

logger = logging.getLogger(__name__)


def get_stf_devices(cond=None):
    """
    According conditions to filter devices on STF and return

    :param cond: conditions to filter devices
    :return: list of devices meeting conditions
    """
    logging.info("Get devices from stf platform.")
    http_stf = Selector(url=v.STF_URL, token=v.TOKEN)
    http_stf.load()
    devices = http_stf.find(cond).devices()
    logger.info("Devices length is : " + str(len(devices)))
    return devices


def get_test_users(test_user_file=None,sep=' ',size=None):
    """
    read test users from test_user_file
    size: need number users
    :return
    users dict (mobile_phone_number, code or password)
    """
    users = []
    with open(test_user_file, mode="r") as f:
        lines = f.readlines()
        if size > len(lines):
            logger.info("No enough devices to test.")
            return
        else:
            count = 0
            for line in lines:
                info = line.split(sep)
                if len(info) == 2:
                    users.append(info)
                else:
                    pass
                count += 1
            return users


def docker_composes_data(users=None,devices=None):
    """
    Generate docker_compose_yml list according to docker_compose data from config file

    :param devices:  devices info
    :return: docker_composes_list
    """
    logger.info("Get docker-composes data use devices info.")
    docker_composes_list = []
    if users is None:
        return
    if devices is not None and len(devices):
        count = 0
        for device in devices:
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
            docker_compose_data = defaultdict(list)

            # Read docker compose data from config file.
            docker_compose_data['APPIUM_CARTIEREJ_IMAGE'] = v.APPIUM_CARTIEREJ_IMAGE
            docker_compose_data['APK_NAME'] = v.APK_NAME
            docker_compose_data['PORTS'] = v.PORTS
            docker_compose_data['APPIUM_CARTIEREJ_CMD'] = v.APPIUM_CARTIEREJ_CMD
            docker_compose_data['APP_APK_VOLUMES'] = v.APP_APK_VOLUMES
            docker_compose_data['DOCKER_COMPOSE_VOLUMES'] = v.DOCKER_COMPOSE_VOLUMES
            docker_compose_data["APPIUM_CARTIEREJ_LOGS_VOLUMES"] = v.APPIUM_CARTIEREJ_LOGS_VOLUMES
            docker_compose_data['PLATFORM_VERSION'] = device.get('version')
            docker_compose_data['APK_NAME'] = v.APK_NAME
            docker_compose_data['DEVICES_NAME'] = url
            docker_compose_data['SERIAL'] = device.get('serial')
            docker_compose_data['CASE_NAME'] = v.CASE_NAME
            docker_compose_data['NEW_COMMAND_TIME_OUT'] = v.NEW_COMMAND_TIMEOUT
            docker_compose_data['MOBILE_PHONE_NUMBER'] = users[count][0]
            docker_compose_data['CODE'] = str(users[count][1]).strip('\r\n')
            docker_composes_list.append(docker_compose_data)
            count += 1
    else:
        logger.info("No devices.")
    return docker_composes_list


def disconnect_remote_session(serial=None):
    """
    Release session

    :param serial:  device name
    :return:
    """
    if serial is None:
        logger.info("No devices disconnect.")
        return False
    else:
        logger.info("Disconnect devices remote session " + str(serial))
        cmd = 'curl -X DELETE -H "Authorization: Bearer ' + v.TOKEN + \
              '" ' + v.STF_DELETE_URL + str(serial)
        try:
            os.system(cmd)
        except Exception as err:
            logger.error(err)
        return True


if __name__ == '__main__':
    disconnect_remote_session("Y15QKBP323GGV")