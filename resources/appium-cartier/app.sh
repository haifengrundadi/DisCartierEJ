#!/bin/bash/
# -*- coding: utf-8 -*-

adb kill-server

adb devices

adb connect {{DEVICES_NAME}}

adb push {{APK_NAME}} /opt/node/

nohup appium &

sleep 2

# check appium
appium_ready() {
    curl http://appium:4723/wd/hub> /dev/null 2>&1
}

a=0
while !(appium_ready) && ((a<90));
do
    sleep 3
    a=$[$a+3]
    echo "waiting for appium ..."
    nohup appium &
done

py.test -s {{CASE_NAME}}