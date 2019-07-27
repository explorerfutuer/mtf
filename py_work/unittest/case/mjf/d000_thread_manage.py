#!/usr/bin/python
#coding:utf-8

import unittest
import time
import os
from tools import PrintTip
from Mtf_Thread_Ctrl import MtfThread
from LogMtf  import  g_Log

# 自定义线程，MtfThread的单元测试
# 给定了MtfThread的基本使用方式

class TestThread(MtfThread):
    def __init__(self):
        MtfThread.__init__(self , _strThreadName = "TestThread")
        self.iResult = 0
        self.iRunData = 0
    def MtfRun(self):
        self.iResult += self.iRunData
        g_Log.LogDebug("MtfRun iRunData=" + str(self.iRunData))
        self.iRunData = 0
    def SetRunData(self , _iData):
        self.iRunData = _iData
        MtfThread.MtfRun(self) # 注意必须要做WakeUp之前修改任务状态
        self.WakeUp()
        g_Log.LogDebug("SetRunData _iData=" + str(_iData))
#  测试1+2+...+100 = 5050
class D000_Thread_Manage_Test(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.listNum = [1 , 2 , 3 , 4]
        self.testThread = TestThread()
        self.testThread.Start()
    def testRun(self):
        for iNum in self.listNum:
            g_Log.LogDebug("Test ------------------ Test")
            self.testThread.SetRunData(iNum) # 有可能发生多次notify但是仅仅唤醒一次导致数据丢失
            while not self.testThread.GetRunStatus():
                time.sleep(0.001)
        self.testThread.UntilStop()
        if self.testThread.iResult != 10:
            PrintTip("Expect 1+2+3+4=10 Test Result=" + str(self.testThread.iResult))
            self.assertTrue(False)
    @classmethod
    def tearDown(self):
        pass
