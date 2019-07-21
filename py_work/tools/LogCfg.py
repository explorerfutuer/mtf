#!/usr/bin/python
#coding:utf-8

# NOTSET(0）、DEBUG(10）、INFO(20）、WARNING(30）、ERROR(40）、CRITICAL(50)
# 使用json进行配置,json 配置文件最后的字典不需要逗号

import sys
import logging
import logging.config
import os
import json
import traceback

from tools import LogTip


class LogCfg:
    def __init__(self , _strLogName , _strLogCfg):
        self.bState = False
        self.strLogCfg = _strLogCfg
        self.strLogName = _strLogName
        self.strLogFile = ""
        fdCfg = None
        try:
            fdCfg = open(_strLogCfg , "r")
        except :
            LogTip("[__init__] " + traceback.format_exc())
            LogTip("[__init__] 配置文件" + _strLogCfg + "无效")
            return None
        if fdCfg is not None:
            fdCfg.close()
        self.bState = self.InitCfg()
        if not self.bState :
            LogTip("[__init__] LogCfg初始化[失败]")
            return False
        LogTip("LogCfg初始化[成功]")
    def JsonCfg(self , _dictCfg):
        # 确保日志目录存在
        self.strLogFile = _dictCfg["handlers"]["rotatefile"]["filename"]
        #LogTip("[JsonCfg] strLogFile=" + str(self.strLogFile))
        try:
            os.makedirs(self.strLogFile) # 将日志文件视为路径创建出来
            os.rmdir(self.strLogFile)
        except FileExistsError:
            pass
        except:
                LogTip("[JsonCfg] " + traceback.format_exc())
        # 偷梁换柱，将配置文件中的日志名RotateFileLogger改为self.strLogName
        _dictCfg["loggers"][self.strLogName] = _dictCfg["loggers"].pop("RotateFileLogger")
        #LogTip("[JsonCfg] strLogName = " + str(self.strLogName))
    def InitCfg(self):
        fdJson = None
        bRet = False
        try:
            fdJson = open(self.strLogCfg , "r")
        except :
            LogTip("[InitCfg] " + traceback.format_exc())
            fdJson = None
        if fdJson is not None:
            dictCfg = None
            try:
                strCfg = fdJson.read()
                dictCfg = json.loads(strCfg)
                self.JsonCfg(dictCfg)
                logging.config.dictConfig(dictCfg)
                bRet = True
            except :
                LogTip("[InitCfg] Load Json Failed " + traceback.format_exc())
                LogTip("[InitCfg] " + str(dictCfg))
                bRet = False
            fdJson.close()
            self.rfLog = logging.getLogger(self.strLogName)
            return bRet
    def LogDebug(self , _strTip):
        self.rfLog.debug(_strTip)
    def LogInfo(self , _strTip):
        self.rfLog.info(_strTip)
    def LogWarn(self , _strTip):
        self.rfLog.warn(_strTip)
    def LogError(self , _strTip):
        self.rfLog.error(_strTip)
    def LogCritical(self , _strTip):
        self.rfLog.critical(_strTip)

if "__main__" == __name__:
    tLog = LogCfg("MainTest" , "./logcfg.json")
    tLog.LogInfo("info test")
    tLog.LogDebug("debug test")
    tLog.LogWarn("warn test")
    tLog.LogError("error test")
    tLog.LogCritical("critical test")

"""
json 格式 =>

{
    "version": 1,
    "formatters": {
        "json_format": {
	    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
 	}
    },
    "handlers": {
        "rotatefile": {
	    "class": "logging.handlers.RotatingFileHandler",
	    "filename": "./tmplog/t.log",  # 日志输出路径
	    "level": "DEBUG",
	    "formatter": "json_format"
            "maxBytes": 10485760, # 日志文件大小
            "backupCount": 10 # 文件写回滚的数目
	}
    },
    "loggers":{
        "RotateFileLogger": {  # 日志对象名称
	    "handlers": ["rotatefile"],
	    "level": "DEBUG"
	}
    }
}

"""
