#!/usr/bin/env python
#coding:utf-8

# NOTSET(0）、DEBUG(10）、INFO(20）、WARNING(30）、ERROR(40）、CRITICAL(50)
# 使用json进行配置,json 配置文件最后的字典不需要逗号

import sys
import logging
import logging.config
import os
import json
import traceback

class LogI:
    def __init__(self):
        pass
    def log_debug(self , _str):
        pass
    def log_info(self , _str):
        pass
    def log_warn(self , _str):
        pass
    def log_error(self , _str):
        pass
    def log_critical(self , _str):
        pass

class Logger(LogI):
    def __init__(self, _strLogName , _strLogCfg):
        self.bState = False
        self.strLogName = _strLogName
        self.strLogFile = ""
        self.init_by_jsonfile(_strLogCfg)
        if not self.bState :            
            return False
        self.log_debug("log load successful")
    def ensure_cfg_valid(self, _dictCfg):
        # 确保日志目录存在
        self.strLogFile = _dictCfg["handlers"]["rotatefile"]["filename"]
        try:
            os.makedirs(self.strLogFile) # 将日志文件视为路径创建出来
            os.rmdir(self.strLogFile)
        except FileExistsError:
            pass
        except:
                LogTip("[JsonCfg] " + traceback.format_exc())
        # 偷梁换柱，将配置文件中的日志名RotateFileLogger改为self.strLogName
        _dictCfg["loggers"][self.strLogName] = _dictCfg["loggers"].pop("RotateFileLogger")
    def init_by_jsonfile(self, _strLogCfg):
        self.strLogCfg = _strLogCfg
        fdJson = None
        bRet = False
        try:
            fdJson = open(self.strLogCfg , "r")
        except :
            print("[", self.__class__.__name__ , "] load json file failed", traceback.format_exc())
            fdJson = None
        if fdJson is not None:
            dictCfg = None
            try:
                strCfg = fdJson.read()
                dictCfg = json.loads(strCfg)
                self.ensure_cfg_valid(dictCfg)
                logging.config.dictConfig(dictCfg)
                bRet = True
            except :
                print("[", self.__class__.__name__ , "] convert json failed", traceback.format_exc())
                bRet = False
            fdJson.close()
            self.rfLog = logging.getLogger(self.strLogName)
            self.bState = True
    def log_debug(self , _strTip):
        self.rfLog.debug(_strTip)
    def log_info(self , _strTip):
        self.rfLog.info(_strTip)
    def log_warn(self , _strTip):
        self.rfLog.warn(_strTip)
    def log_error(self , _strTip):
        self.rfLog.error(_strTip)
    def log_critical(self , _strTip):
        self.rfLog.critical(_strTip)

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
