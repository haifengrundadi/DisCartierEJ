#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
该多线程主要的目的是为了，处理多台设备运行。
"""

import Queue
import threading
import time
import os
import logging
import subprocess
from conftest import disconnectRemoteSession

logger = logging.getLogger(__name__)
q = Queue.Queue(0)
NUM_WORKERS = 3


class MyThread(threading.Thread):
    """
        A worker thread.
    """

    def __init__(self, input):
        self._jobq = input
        threading.Thread.__init__(self)

    def run(self):
        """
            Get a job and process it.
            Stop when there's no more jobs
        """
        while True:
            if self._jobq.qsize() > 0:
                job = self._jobq.get()
                serial = job["serial"]
                file = job["file"]
                self._process_job(file, serial)
            else:
                break

    def _process_job(self, file, serial):
        """
            Do useful work here.
        """
        logger.info(self.name + "\t begin to run devices is  " + serial)
        thread_name = self.name
        doJob(thread_name, file, serial)


def doJob(thread_name, file, serial):
    """
        do work function 1
    """
    time.sleep(2)
    logger.info(thread_name + " begin to do job and the docker_compose address is " + file)
    # change into directory and docker-compose up
    os.chdir(file)
    # print os.getcwd()
    if os.path.isdir(file):
        dc_files = os.listdir(file)
        for temp in dc_files:
            if temp.endswith(".yml"):
                try:
                    subprocess.call(["docker-compose up"], shell=True)
                except Exception as err:
                    logger.error(err)
                finally:
                    disconnectRemoteSession(serial)
                    logger.info("release session.")
            else:
                pass
    else:
        os.system("This is not directory.")


def putJobs(base_path):
    """
        put jobs in queue
    """
    logger.info("Begin to put jobs in queue......!")
    base_path = os.path.abspath(base_path)
    files = os.listdir(base_path)
    for file in files:
        serial = file
        file = os.path.join(base_path, file)
        dict = {"file": file, "serial": serial}
        q.put(dict)
    logger.info("put " + str(q.qsize()) + " job.....")
    return q


if __name__ == '__main__':
    print "begin..."
    # put some work to q
    # q = putJobs(docker_composes_files_path)
    # # print total job q's size
    # print "job q'size", q.qsize()
    # # start threads to work
    # for x in range(NUM_WORKERS):
    #     MyThread(q).start()
    # #     # if q is not empty, wait
    # # while q.qsize()>0:
    # #    time.sleep(0.1)
