#!/usr/bin/python
#coding:utf-8

import datetime
import time
import traceback
from LogMtf  import  g_Log

def LogTip(_strTip):
    print(_strTip)
    g_Log.LogDebug(_strTip)

def PrintTip(_strTip):
    print(_strTip)
# 跟时间戳返回日期字符串
def TimeStamp2StrDT(_timestamp , _strFormat = "%Y-%m-%d %H:%M:%S"):
    structTM = time.localtime(_timestamp)
    return time.strftime(_strFormat , structTM)
def StrDT2TimeStamp(_strDateTime , _strFormat = "%Y-%m-%d %H:%M:%S"):
    structTM = time.strptime(_strDateTime , _strFormat)    
    timestamp = time.mktime(structTM)
    return timestamp
# 返回当前时间的偏移量的日期
def NowOffset(_iSec = 0 , _strFormat = "%Y-%m-%d %H:%M:%S"):
    nowTimesstamp = time.time()
    tmpTimeStamp = nowTimesstamp + _iSec
    structTM = time.localtime(tmpTimeStamp)
    return time.strftime(_strFormat , structTM)
# 字符串的日期格式转换为时间元组
def StrDT2Tuple(_strDateTime , _strFormat = "%Y-%m-%d %H:%M:%S"):
    try:
        structTM = time.strptime(_strDateTime , _strFormat)
        return (structTM.tm_year , structTM.tm_mon , structTM.tm_mday , structTM.tm_hour , structTM.tm_min , structTM.tm_sec)
    except :
        print("时间转换失败DateTime=%s , Format=%s" %(_strDateTime , _strFormat))
        return (0 , 0 , 0 , 0 , 0 , 0)
# 睡眠指定的时间
def Sleep_ms(_ims):
    isecond = _ims / 1000
    time.sleep(isecond)

