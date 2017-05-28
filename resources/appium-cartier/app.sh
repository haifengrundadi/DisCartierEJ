#!/bin/bash/
#echo "Connect to remote devices and start appium"
#read version, devices_url
#adb connect devices_url
#if [adb devices]; then
#	appium
#else
#	sleep 5
#	if [adb devices]; then
#		appium
#	else
#		sleep 10
#		if [adb devices]; then
#			appium
#		else
#			exit
#		fi
#	fi
#fi

adb devices

adb connect {{device_address}}

adb push /apk_shell/app-Fir-release-4.16.020.apk  /opt/node/

appium
