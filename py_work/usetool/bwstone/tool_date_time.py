#!/usr/bin/env python
#coding:utf-8

import datetime
import time
import traceback


def timestamp2fmtstr(_iTimestamp, _strFmt = '%Y-%m-%d %H:%M:%S'):
    """时间戳 => 指定格式的日期字符串"""
    structTM = time.localtime(_iTimestamp)
    return time.strftime(_strFmt , structTM)

def fmtstr2timestamp(_strDateTime, _strFmt = '%Y-%m-%d %H:%M:%S'):
    """格式化的日期 => 时间戳"""
    structTM = time.strptime(_strDateTime , _strFmt)    
    return  time.mktime(structTM)

def now_datetime_offset(_iSecond = 0, _strFmt = '%Y-%m-%d %H:%M:%S'):
    """获取档当前时刻偏移秒的格式化字符串"""
    nowTimesstamp = time.time()
    tmpTimeStamp = nowTimesstamp + _iSecond
    structTM = time.localtime(tmpTimeStamp)
    return time.strftime(_strFmt , structTM)
def now_datetime():
    return now_datetime_offset()

def strdatetime2tuple(_strDateTime, _strFmt = '%Y-%m-%d %H:%M:%S'):
    """格式化的时间 => 元组（年，月，日，时，分，秒）"""
    try:
        structTM = time.strptime(_strDateTime , _strFmt)
        return True,(structTM.tm_year , structTM.tm_mon , structTM.tm_mday , structTM.tm_hour , structTM.tm_min , structTM.tm_sec)
    except :
        return False,(0 , 0 , 0 , 0 , 0 , 0)

def sleep_ms(_iMilliSecond):
    """休眠指定的毫秒"""
    time.sleep(_iMilliSecond / 1000)

