#! /Users/michael/anaconda3/bin/python
# @Date:   2018-08-13 17:57:15

# 用于控制手机

import os
import settings
import subprocess

class Android:

    def __init__(self):
        """

        """
        self.adb_path = settings.adb_path
        
    def swipe_up(self):
        """
            上划
        """
        cmd ='{adb} shell input swipe {x1} {y1} {x2} {y2}'.format(
            adb = self.adb_path,
            x1 = settings.lower_point[0],
            y1 = settings.lower_point[1],
            x2 = settings.higher_point[0],
            y2 = settings.higher_point[1],
        )
        process = os.popen(cmd)
        output = process.read()
        return output

if __name__ == '__main__':
    adb = Android()
    adb.swipe_up()














