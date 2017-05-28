#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yattag import Doc, indent
import os


def generate_cartier_html(logDir=None):
    """
        将cariter每次生产的log日志和图片生产一个html
    """
    doc, tag, text = Doc().tagtext()
    doc.asis("<!DOCTYPE html> ")

    with tag("html"):

        # 防止乱码
        with tag("head"):
            doc.asis('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')

        # 显示日志
        with tag("h1",style="font-size:30px;text-align: center;"):
            text("Show logs of test case")

        # 判读日志文件是否有
        if logDir is None:
            with tag("h2"):
                text("The log directory doesn't set!")
        elif os.path.isdir(logDir) is False:
            with tag("h2"):
                text("The log directory your ref is not directory!")
        else:
            with tag("body"):
                # 每一个设备每跑一边case，生成一张表格
                for logfile in os.listdir(logDir):
                    with tag("table"):
                        device_name = logfile
                        with tag("th",style="font-size:24px;text-align: center;"):
                            text("Test case of " + device_name)
                        logfile = os.path.join(logDir, logfile)
                        for file_log in os.listdir(logfile):
                            temp = file_log
                            abs_address = os.path.join(logfile,file_log)
                            if os.path.isdir(abs_address):
                                with tag('tr'):
                                    with tag("td", style="font-size:20px; color:#FF0000;text-align: center;"):
                                        text('*************Show  pictures from screenshot directory*******************')
                                with tag("tr"):
                                    with tag("td"):
                                        i = 1
                                        for file in os.listdir(abs_address):
                                            if i % 3 == 0:
                                                doc.asis("<br/>")
                                            file = os.path.join(os.path.abspath(abs_address), file)
                                            doc.stag('img', src=file, alt="screenshot picture", width="300px")
                                            i += 1
                                        if i == 1:
                                            text("No screenshot pics need to be show!")
                            else:
                                if temp == "cartier.log":
                                    with tag("tr"):
                                        with tag("td", style="font-size:20px; color:#FF0000;text-align: center;"):
                                            text("*******************Show cartier.log*********************")
                                    with open(abs_address) as logFile:
                                        for line in logFile.readlines():
                                            with tag("tr"):
                                                with tag("td"):
                                                    text(line)
                                elif temp == "errors.log":
                                    with tag("tr"):
                                        with tag("td", style="font-size:20px; color:#FF0000;text-align: center;"):
                                            text("*******************Show errors.log*********************")
                                    with open(abs_address) as logFile:
                                        for line in logFile.readlines():
                                            with tag("tr"):
                                                with tag("td",style="color:#FF0000;"):
                                                    text(line)
                                else:
                                    pass

    # 格式化输出，让输出的格式有缩进便于查看
    result = indent(
        doc.getvalue(),
        indentation='    ',
        newline='\r\n',
        indent_text=True
    )

    with open("result.html", "w+") as h:
        h.write(result)
    return result


if __name__ == "__main__":
    print generate_cartier_html("/Users/red/tmp/logs")
