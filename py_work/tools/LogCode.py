#/usr/bin/python
#coding:utf-8

import logging
from logging.handlers import RotatingFileHandler

# NOTSET(0) , DEBUG(10) , INFO(20) , WARN(30) , ERROR(40) , CRITICAL(50).
class LogCode:
    def __init__(self , _strCategory , _strPath , _iRotateSize = 1024*1024*10 , _iFileCnt = 20):
        self.m_Log = logging.getLogger(_strCategory)
        tmpLogFormat = logging.basicConfig(level = logging.INFO , format = '%(message)s')
        tmpHandler = RotatingFileHandler(_strPath , maxBytes = _iRotateSize , backupCount = _iFileCnt)
        tmpHandler.setFormatter(tmpLogFormat)
        self.m_Log.addHandler(tmpHandler)
        self.m_Log.propagate = False
    def LogDebug(self , _strTip):
        self.m_Log.debug(_strTip)
    def LogInfo(self , _strTip):
        self.m_Log.info(_strTip)
    def LogWarn(self , _strTip):
        self.m_Log.warn(_strTip)
    def LogError(self , _strTip):
        self.m_Log.error(_strTip)
    def LogCritical(self , _strTip):
        self.m_Log.critical(_strTip)
    def SetLevel(self , _ilevel):
        if _ilevel == 0:
            self.m_Log.setLevel(logging.NOTSET)
        elif _ilevel == 1:
            self.m_Log.setLevel(logging.DEBUG)
        elif _ilevel == 2:
            self.m_Log.setLevel(logging.INFO)
        elif _ilevel == 3:
            self.m_Log.setLevel(logging.WARN)
        elif _ilevel == 4:
            self.m_Log.setLevel(logging.ERROR)
        elif _ilevel == 5:
            self.m_Log.setLevel(logging.CRITICAL)
        else:
            self.m_Log.setLevel(logging.DEBUG)
