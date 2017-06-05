#!/usr/bin/env python
# -*- coding: utf-8 -*-

from yattag import Doc, indent
import os


def generate_cartierEJ_html(log_dir=None,
                            cartierEJ_log="cartier.log",
                            error_log="error.log",
                            res_html="result.html"):
    """
    Use cartierEJ log and screenshot to generate log html

    :param log_dir: log path
    :param cartierEJ_log: log info
    :param error_log: error log info
    :param res_html: html we need
    :return:
    """
    doc, tag, text = Doc().tagtext()
    doc.asis("<!DOCTYPE html> ")

    with tag("html"):

        with tag("head"):
            doc.asis('<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')

        with tag("h1", style="font-size:30px;text-align: center;"):
            text("Show logs of test case")

        if log_dir is None:
            with tag("h2"):
                text("The log directory doesn't set!")
        elif os.path.isdir(log_dir) is False:
            with tag("h2"):
                text("The log directory your ref is not directory!")
        else:
            with tag("body"):
                for logfile in os.listdir(log_dir):
                    with tag("table"):
                        device_name = logfile
                        with tag("th", style="font-size:24px;text-align: center;"):
                            text("Test case of " + device_name)
                        logfile = os.path.join(log_dir, logfile)
                        for file_log in os.listdir(logfile):
                            temp = file_log
                            abs_address = os.path.join(logfile, file_log)
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
                                            doc.stag('img', src=file, alt="screen shot picture", width="300px")
                                            i += 1
                                        if i == 1:
                                            text("No screen shot pics need to be show!")
                            else:
                                if temp == cartierEJ_log:
                                    with tag("tr"):
                                        with tag("td", style="font-size:20px; color:#FF0000;text-align: center;"):
                                            text("*******************Show cartier.log*********************")
                                    with open(abs_address) as logFile:
                                        for line in logFile.readlines():
                                            with tag("tr"):
                                                with tag("td"):
                                                    text(line)
                                elif temp == error_log:
                                    with tag("tr"):
                                        with tag("td", style="font-size:20px; color:#FF0000;text-align: center;"):
                                            text("*******************Show errors.log*********************")
                                    with open(abs_address) as logFile:
                                        for line in logFile.readlines():
                                            with tag("tr"):
                                                with tag("td", style="color:#FF0000;"):
                                                    text(line)
                                else:
                                    pass
    result = indent(
        doc.getvalue(),
        indentation='    ',
        newline='\r\n',
        indent_text=True
    )

    with open(res_html, "w+") as h:
        h.write(result)
    return result


if __name__ == "__main__":
    print generate_cartierEJ_html("/Users/red/tmp/logs")
