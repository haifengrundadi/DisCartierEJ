# DisCartierEJ简介

作者：Juan Liu  @Date 2017/05/31

## DisCartierEJ是什么？
DisCartierEJ是一个可以将用户编写的case根据用户需要运行在不同设备（手机等）的框架。例如：用户编写了一个login的case，需要运行在 3 台 Version 高于 5.0 的设备上。

## 为什么有DisCartierEJ？
目前的一台设备上只能运行一个Appium，而一个Appium Server只能对应一个设备。在实践的过程中，常常需要一个case运行在不同类型不同版本的设备上，因而需要一个框架去支持这种需求。

## 为什么叫DisCariterEJ？
由于所有的case都是根据标准开发工具模板CartierEJ编写，因而称之为DisCariterEJ。

## DisCartierEJ的设计思路？
主要利用[STF](https://openstf.io/)(Smartphone Test Farm)来管理各种设备，利用[Docker](https://www.docker.com/)的[Docker-Compose](https://docs.docker.com/compose/)的工具生成满足各种需要的docker-compose.yml文件，一个docker-compose.yml文件对应一个包含case的Appium容器，一个包含case的Appium容器对应一个设备。

## 主要流程

1. DisCartierEJ根据用户的需求会给STF发送请求获取所需要的设备信息（返回的是一个JSON）。
2. 将返回来的信息注入到case中（利用docker-compose.yml模板中的环境变量，间接注入每一个包含case的Appium容器），实现一个包含case的Appium容器对应一个设备。
3. 在各个Appium内部运行case。

## 使用之前的准备
1. 安装[docker](https://www.docker.com/)

## Demo演示

需求：需要将login整个CariterEJ运行在 3 台 Version 高于 5.0 的设备上。

步骤如下:

1. 编写login的CartierEJ代码（可以根据CartierEJ模块进行编写），在本地开发完并且验证成功，将CartierEJ中的contest.py中
desired_caps中的信息替换成如下格式。

		@pytest.fixture(scope="session")
        def desired_caps(request):
            """
            Used to test multi devices
            """
            desired_caps = defaultdict(list)
            desired_caps['platformName'] = 'Android'
            try:
                version = os.environ.get("PLATFORM_VERSION")
                app_name = os.environ.get("APK_NAME")
                devices_name = os.environ.get("DEVICES_NAME")
            except KeyError:
                logger.error("No environment variables for desired caps")
                return None
            if version is None or app_name is None or devices_name is None:
                return None
            desired_caps['platformVersion'] = version
            desired_caps['app'] = app_name
            desired_caps['deviceName'] = devices_name
            desired_caps['newCommandTimeout'] = os.environ.get("NEW_COMMAND_TIME_OUT")
            desired_caps['unicodeKeyboard'] = True
            desired_caps['resetKeyboard'] = True
            desired_caps['noReset'] = False
            return desired_caps


2. 并将这些代码上传到github上或者一个可以从下载得到的代码，比如我的github地址为。

		https://github.com/haifengrundadi/CartierEJ.git

3. 将DisCartierEJ中的Dockerfile中的获取CartierEJ的代码更改为上面的地址。

		...
		#=======================================
        # pull code from git
        #=======================================
        RUN git clone https://github.com/haifengrundadi/CartierEJ.git
        WORKDIR CartierEJ
        RUN pip install -r requirements.txt
        RUN mkdir logs
        WORKDIR tests/smoketest
        CMD ["bash /app_shell/app.sh]
		...

4. 使用Docker 根据Dockerfile 生成一个镜像文件 appium-cartierej-docker:latest


5. 将DisCartierEJ项目中的constant.py中相关变量替换为本地的实际信息。

		#!/usr/bin/env python
        # -*- coding: utf-8 -*-

        # stf_url address
        STF_URL = "http://xxx.xxx.xxx.xxx:7100/api/v1/devices"

        """
        access token of stf

        STF uses OAuth 2.0 for authentication. In order to use the API,
        you will first need to generate an access token. Access tokens
        can be easily generated from the STF UI. Just go to the Settings
        tab and generate a new access token in Keys section.
        Don't forget to save this token somewhere, you will not be able to see it again.
        """
        TOKEN = "..."

        STF_DELETE_URL = "http://xxx.xxx.xxx.xxx:7100/api/v1/user/devices/"

        # some variables in desired_capablities
        PLATFORM_NAME = 'Android'
        NEW_COMMAND_TIMEOUT = 60
        # the apk place in container
        APK_NAME = "/apk_shell/xxx.apk"
        # come infomation needed by docker_compose.yml
        APPIUM_CARTIEREJ_IMAGE = "xxxxxxx"
        PORTS = 4723
        APPIUM_CARTIEREJ_CMD = "bash /app_shell/app.sh"

        # xxxxxx is local file which contains apk
        # You need to change to yourself.
        APP_APK_VOLUMES = "xxxxxxxxxxx:/apk_shell"

        """
        Use device name as directory to save docker_compose.yml and app.sh
        Need abs path
        """
        DOCKER_COMPOSE_VOLUMES = "xxxxxx/DisCartierEJ/resources/dockercomposes/"

        # logs save place in local
        LOCAL_LOG_DIR = "xxxxx"
        APPIUM_CARTIEREJ_LOGS_VOLUMES = LOCAL_LOG_DIR + 'RANDOM:/opt/node/CartierEJ/logs'  # RANDOM为变量在生成的过程中替换

        # case to run
        CASE_NAME = "test_login.py"
6. 运行generator.py的 generator\_docker\_composes 方法会在dockercomposes文件夹下生成各种需要的文件。
7. 运行generator.py的 up\_docker\_composes 方法，会启动所有的容器，也就默认启动了容器中的所有case。