#!/usr/bin/python
#coding:utf-8

import tools
import unittest
import time

class B000_Tools_Datetime_Test(unittest.TestCase):
    @classmethod
    def setUp(self):
        pass
    def testDateTimeFormatShort(self):
        strTestDT = "20190713173000"
        timestamp = tools.StrDT2TimeStamp(strTestDT , "%Y%m%d%H%M%S")
        if timestamp != 1563010200:
            print("[StrDT2TimeStamp]字符串日期20190713173000转换为时间戳1563010200失败，测试结果为" + str(timestamp))
            self.assertFalse(True)
        strDT = tools.TimeStamp2StrDT(timestamp , "%Y%m%d%H%M%S")
        if strDT != strTestDT :
            print("[TimeStamp2StrDT]时间抽1563010200转换为日期20190713173000失败，测试转换结果为" + strDT)
        tupleDT = tools.StrDT2Tuple(strTestDT , "%Y%m%d%H%M%S")
        if not(tupleDT[0] == 2019 and tupleDT[1] == 7 and tupleDT[2] == 13 and tupleDT[3] == 17 and tupleDT[4] == 30 and tupleDT[5] == 0 ):
            print("[StrDT2Tuple]字符串日期2019-07-13 17:30:00转换为年月时分秒失败，year:%d , month:%d , mday:%d , hour:%d , minute:%d , second:%d" % tupleDT)
            self.assertFalse(True)
    def testDateTimeFormatStandard(self):
        strTestDT = "2019-07-13 17:30:00"
        timestamp = tools.StrDT2TimeStamp(strTestDT)
        if timestamp != 1563010200:
            print("[StrDT2TimeStamp]字符串日期2019-07-13 17:30:00转换为时间戳1563010200失败，测试结果为" + str(timestamp))
            self.assertFalse(True)
        strDT = tools.TimeStamp2StrDT(timestamp)
        if strDT != strTestDT :
            print("[TimeStamp2StrDT]时间抽1563010200转换为日期2019-07-13 17:30:00失败，测试转换结果为" + strDT)
            self.assertFalse(True)
        tupleDT = tools.StrDT2Tuple(strTestDT)
        if not (tupleDT[0] == 2019 and tupleDT[1] == 7 and tupleDT[2] == 13 and tupleDT[3] == 17 and tupleDT[4] == 30 and tupleDT[5] == 0 ):
            print("[StrDT2Tuple]字符串日期2019-07-13 17:30:00转换为年月时分秒失败，year:%d , month:%d , mday:%d , hour:%d , minute:%d , second:%d" % tupleDT)
            self.assertFalse(True)
    def testToolsSleep(self):
        begTimeStamp = time.time()
        isleeptime_ms = 2*1000
        tools.Sleep_ms(isleeptime_ms)
        endTimeStamp = time.time()
        elapsetime = endTimeStamp - begTimeStamp
        if elapsetime - 2 > 0.5:
            print("[Sleep_ms(2000)]误差有点大，测试值:" +  str(elapsetime))
            self.assertFalse(True)
    def testNowDateTime(self):
        strNowDT = tools.NowOffset()
        nowstamp = tools.StrDT2TimeStamp(strNowDT)
        tmptimestamp = time.time()
        elapsetime = tmptimestamp - nowstamp
        if elapsetime > 2:
            print("[NowOffset]获取当前时间是失败，[%s][%d][%d]" % (strNowDT , nowstamp , tmptimestamp))
            self.assertFalse(True)
    def testRun(self):
        self.testDateTimeFormatStandard()
        self.testDateTimeFormatShort()
        self.testToolsSleep()
        self.testNowDateTime()
    @classmethod
    def tearDown(self):
        pass
