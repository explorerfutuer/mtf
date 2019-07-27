#!/usr/bin/python
#coding:utf-8

import unittest
import time
import os
from tools import PrintTip
from Mtf_Thread_Ctrl import MtfWorker
from Mtf_Thread_Ctrl import I_Task
from Mtf_Thread_Ctrl import MtfWorkerGroup


# 线程池基本单元-线程，MtfWorker单元测试
# 给定MtfWorker的基本使用

class Test_Task(I_Task):
    def __init__(self , _objCB = None):
        self.objCallBack = _objCB
        self.listNum = []
        self.iResult = 0
    def SetTask(self , _obj):
        self.listNum = _obj
    def DoTask(self):
        iSum = 0
        try:
            for iTmpNum in self.listNum:
                iSum += iTmpNum
        except:
            iSum = 0
        self.iResult = iSum
    def DoneTask(self):
        self.objCallBack.testSetResult(self.objCallBack , self.iResult) # 此处不太符合常理，？？？？
        
#  测试1+2+...+100 = 5050
class D001_Thread_Manage_Test(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.testTask = Test_Task(_objCB = self)
        self.testWorkerGrp = MtfWorkerGroup(_iPermanent = 1 , _strGrpName = "testWorkerGroup")
        self.testWorkerGrp.Start()
        self.listNum = [1 , 2 , 3, 4]
        self.iTestResult = 0
        self.iExpectResult = 10
        self.bReciveResult = False
        self.iMaxTimeout = 3
    def testSetResult(self , _iRes):
        self.bReciveResult = True
        self.iTestResult = _iRes
        PrintTip("Test Result=" + str(_iRes))
    def testRun(self):
        tupleTask = (self.testTask , self.listNum)
        self.testWorkerGrp.AcceptTask(tupleTask)
        iEpoll = 0
        while not self.bReciveResult and iEpoll < self.iMaxTimeout :
            time.sleep(0.5)
            iEpoll += 0.5
        if self.bReciveResult == False and iEpoll >= self.iMaxTimeout:
            self.testWorkerGrp.UntilStop()
            PrintTip("wait thread pool execute task timeout")
            self.assertTrue(False)
        if self.iTestResult != self.iExpectResult:
            PrintTip("Expect 1+2+3+4=10 Test Result=" + str(self.iTestResult))
            self.assertTrue(False)
        if len(self.testWorkerGrp.dictLeisureWorkers) == 1 and len(self.testWorkerGrp.dictBusyWorkers) == 0:
            pass
        else:
            PrintTip("worked worker status invalid")
        self.testWorkerGrp.UntilStop()
    @classmethod
    def tearDown(self):
        pass
