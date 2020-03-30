#!/usr/bin/env python
#coding:utf-8

import os, sys

# 返回Python的根目录
def  LoadThirdParty(_strNodeName = "py_work/"):
    # 测试用例路径
    strPwd = os.getcwd()
    strRootDir = ""
    iPos = strPwd.find(_strNodeName)
    if iPos == -1:
        strRootDir = "../../"
    else:
        strRootDir = strPwd[:iPos] + "py_work"
        importpath=[]
        for root , dirs , files in os.walk(strRootDir + "usetool"):
            importpath.append(root)
            sys.path.append(root)
    return strRootDir
LoadThirdParty()

import unittest
from tool_date_time import *


class TestToolDateTime(unittest.TestCase):
    """tool_date_time 时间格式函数的测试"""
    def test_timestamp2fmtstr(self):
        iTimestamp = 0
        strExpect = '1970-01-01 08:00:00'
        strActual = timestamp2fmtstr(iTimestamp)
        self.assertEqual(strExpect, strActual)
        iTimestamp = 946656000
        strExpect = "2000-01-01 00:00:00"
        strActual = timestamp2fmtstr(iTimestamp)
        self.assertEqual(strExpect, strActual)
        # 指定时间格式测试
        iTimestamp = 946656000
        strFmt = "%Y%m%d%H%M%S"
        strExpect = "20000101000000"
        strActual = timestamp2fmtstr(iTimestamp, strFmt)
        self.assertEqual(strExpect, strActual)
    def test_fmtstr2timestamp(self):
        strDateTime = "1970-01-01 08:00:00"
        iExpect = 0 ;
        iActual = fmtstr2timestamp(strDateTime)
        self.assertEqual(iExpect, iActual)
        strDateTime = "2000-01-01 00:00:00"
        iExpect = 946656000
        iActual = fmtstr2timestamp(strDateTime)
        self.assertEqual(iExpect, iActual)
        # 指定时间格式测试
        strFmt = "%Y%m%d%H%M%S"
        strDateTime = "20000101000000"
        iExpect = 946656000
        iActual = fmtstr2timestamp(strDateTime, strFmt)
        self.assertEqual(iExpect, iActual)
    def test_now_datetime_offset(self):
        pass
    def test_now_datetime(self):
        pass
    def test_strdatetime2tuple(self):
        strDateTime = "1970-01-01 08:00:00"
        tupleExpect = (1970, 1, 1, 8, 0, 0) ;
        bStatus,tupleActual = strdatetime2tuple(strDateTime)
        self.assertEqual(bStatus, True)
        self.assertEqual(tupleExpect, tupleActual)
        strDateTime = "0000-00-00 00:00:00"
        tupleExpect = (0, 0, 0, 8, 0, 0) ;
        bStatus,tupleActual = strdatetime2tuple(strDateTime)
        self.assertEqual(bStatus, False)
        # 指定时间格式测试
        strFmt = "%Y%m%d%H%M%S"
        strDateTime = "20000101000000"
        tupleExpect = (2000, 1, 1, 0, 0, 0) ;
        bStatus,tupleActual = strdatetime2tuple(strDateTime, strFmt)
        self.assertEqual(bStatus, True)
        self.assertEqual(tupleExpect, tupleActual)
    def test_sleep_ms(self):
        begTime = time.time()
        iElapse = 10.0
        sleep_ms(iElapse)
        endTime = time.time()
        iExpect = 10.0 / 1000 ; # 0.01
        iActual = endTime - begTime
        self.assertTrue(iActual - iExpect < 0.005)
if __name__ == '__main__':
    unittest.main()
        
