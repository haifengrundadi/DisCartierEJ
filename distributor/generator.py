#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本模块的主要作用是利用/resources/template/dc-compose.yml和我们选择的设备信息，生产一些docker-compose.yml文件。
"""
import logging
import os
import subprocess
import time
from jinja2 import Environment, FileSystemLoader
from conftest import docker_composes_data
from log import LOGGER
import myThread
from constant import LOCAL_LOG_DIR

LOGGER.info("*********Begin******")
logger = logging.getLogger(__name__)
# 资源文件地址
base_res_path = os.path.join(os.pardir, "resources")
# 模板文件地址
template_path = os.path.join(base_res_path, "template")
# 生产的docker-compse.yml文件地址
docker_composes_files_path = os.path.join(base_res_path, "dockercomposes")
# 项目名称
package_name = "distributor"


def generator_docker_composes(template_path, template_name, docker_composes_files_path, data):
    """
    利用模板和变量生产所需要的文件
    """
    logger.info("begin to generator docker-compose.yml")
    if data is None or len(data) == 0:
        logging.info("no devices to generate docker-compose-files")
        return
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(template_name)
    app_template = env.get_template("app-template.sh")
    k = 1
    for docker_compose_data in data:
        app_data = {}
        app_data['APP_NAME'] = docker_compose_data['APP_NAME']
        app_data['DEVICES_NAME'] = docker_compose_data['DEVICES_NAME']
        app_data['CASE_NAME'] = docker_compose_data['CASE_NAME']
        serial = docker_compose_data['SERIAL']
        docker_compose_data['DOCKCOMPOSE_VOLUMES'] = docker_compose_data['DOCKCOMPOSE_VOLUMES'] + \
                                                     serial + ":/app_shell"
        docker_compose_data['CONTAINER_NAME'] = serial
        logs_volumes = docker_compose_data['APPIUM_CARTIER_LOGS_VOLUMES']
        docker_compose_data['APPIUM_CARTIER_LOGS_VOLUMES'] = str(logs_volumes).replace("RANDOM", serial)
        app_res = app_template.render(app_data)
        res = template.render(docker_compose_data)

        devices_path = os.path.join(docker_composes_files_path, serial)
        if not os.path.exists(devices_path):
            os.mkdir(devices_path)
        dc_temp = os.path.join(devices_path, "docker-compose.yml")
        app_temp = os.path.join(devices_path, "app.sh")

        with open(dc_temp, "w") as f:
            f.write(res)
        with open(app_temp, "w") as f:
            f.write(app_res)

        k += 1
    logger.info("Created " + str(len(data)) + " docker-compose.yml.")


def up_docker_composes(base_path):
    """
    启动生成的docker-compose文件
    """
    logger.info("Use 'docker-compose up' to start all docker-compose.yml")
    q = myThread.putJobs(base_path)
    print "job q'size", q.qsize()
    for x in range(myThread.NUM_WORKERS):
        myThread.MyThread(q).start()


def rm_docker_container():
    """
    删除之前的cache
    """
    logger.info("docker rm cache container")
    try:
        subprocess.call(["docker-compose down"], shell=True)
    except Exception as err:
        logger.error(err)
    finally:
        logger.info("release cache.")


def delete_docker_composes(docker_composes_files_path):
    """
    删除之前的docker-compose文件
    """
    logger.info("Delete directory or files")
    for file in os.listdir(docker_composes_files_path):
        file = os.path.join(docker_composes_files_path, file)
        if os.path.isdir(file):
            subprocess.call(["rm", "-rf", file])
        else:
            subprocess.call(["rm", "-f", file])


def delete_logfiles(logdir):
    """
    删除之前case生产的log文件
    """
    delete_docker_composes(logdir)


if __name__ == '__main__':
    logger = logging.getLogger(" ")
    delete_docker_composes(docker_composes_files_path)
    delete_logfiles(LOCAL_LOG_DIR)
    data = docker_composes_data()
    generator_docker_composes(template_path, "dc-template.yml", docker_composes_files_path, data)
    up_docker_composes(docker_composes_files_path)

