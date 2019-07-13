#!/usr/bin/python
#coding:utf-8

import LogCode
import unittest
import tools
import os

class A000_Tool_Logcode_Test(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.strRunDir = os.getcwd()
        self.strTestDir = self.strRunDir + "/TestLogCodemjf001/"
        os.mkdir(self.strTestDir)
    def testRun(self):
        strNowDateTime = tools.NowOffset(0)
        testLog = LogCode.LogCode("TestLogCode" , self.strTestDir + "logcode.log")
        testLog.SetLevel(1)
        testLog.LogDebug(strNowDateTime + " test=>debug")
        testLog.LogInfo(strNowDateTime + " test=>info")
        testLog.LogError(strNowDateTime + " test=>error")
        testLog.LogCritical(strNowDateTime + " test=>critical")
    @classmethod
    def tearDown(self):
        os.chdir(self.strRunDir)
