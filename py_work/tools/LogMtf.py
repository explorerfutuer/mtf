#!/usr/python
#coding:utf-8

from LogCfg import LogCfg
from LogCode import LogCode
from GlobalCfg import  g_strLogName

class I_Log:
    def __init__(self):
        pass
    def LogDebug(self , _str):
        pass
    def LogInfo(self , _str):
        pass
    def LogWarn(self , _str):
        pass
    def LogError(self , _str):
        pass
    def LogCritical(self , _str):
        pass

class LogMtf(I_Log):
    def __init__(self , _obj , _strLogName = g_strLogName):
        self.m_Log = None
        self.strLogName = _strLogName
        self.Init(_obj)
    def Init(self , _obj):
        self.m_Log = LogCfg(self.strLogName , _obj) # 配置文件路径
        # self.m_Log = LogCode(_strLogName , _obj)  # 日志输出路经
        self.m_Log.LogDebug("Init LogMtf Successful")
        return True
    def LogDebug(self , _str):
        self.m_Log.LogDebug(_str)
        return True
    def LogInfo(self , _str):
        self.m_Log.LogInfo(_str)
        return True
    def LogtWarn(self , _str):
        self.m_Log.LogWarn(_str)
        return True
    def LogError(self , _str):
        self.m_Log.LogError(_str)
        return True
    def LogCritical(self , _str):
        self.m_Log.LogCritical(_str)
        return True
        
g_Log = LogMtf("./cfgmtf/log.json" , g_strLogName)
