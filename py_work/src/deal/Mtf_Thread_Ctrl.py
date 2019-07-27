#!/usr/bin/python
#coding:utf-8

import threading
import traceback
import uuid
import time
from LogMtf  import  g_Log
from tools import PrintTip
"""
  任何使用 MtfThreadManage线程都实现
  I_Task接口
  GuardMutex: 对互斥锁的进行切片封装
  CondMutex: 对信号量进行切片封装

  MtfThread:
    1. 对python的threading.Thread的简单封装
  MtfWorker:
    1. 与MtfWorkerGroup配合使用
  MtfWorkerGroup: 线程池
    1. 管理Worker
    2. 将任务分配到空闲的Worker中
    3. TODO Worker性能策略优化
"""

class GuardMutex:
    def __init__(self , _lock):
        self.mutexLock = _lock
        self.mutexLock.acquire()
        g_Log.LogDebug("lock=" + str(self.mutexLock))
    def __del__(self):
        self.mutexLock.release()
        g_Log.LogDebug("unlock=" + str(self.mutexLock))
class CondMutex:
    def __init__(self , _cond):
        self.condition = _cond
        self.condition.acquire()
        g_Log.LogDebug("cond acquire =" + str(self.condition))
    def Notify(self):
        g_Log.LogDebug("Notify Before" + str(self.condition))
        self.condition.notify()
        g_Log.LogDebug("Notify End" + str(self.condition))
    def NotifyAll(self):
        g_Log.LogDebug("NotifyAll Before" + str(self.condition))
        self.condition.notifyAll()
        g_Log.LogDebug("NotifyAll End" + str(self.condition))
    def Wait(self , _timeout = None):
        g_Log.LogDebug("Wait Beg" + str(self.condition))
        self.condition.wait(timeout = _timeout)
        g_Log.LogDebug("Wait End" + str(self.condition))
    def __del__(self):
        self.condition.release()
        g_Log.LogDebug("cond release =" + str(self.condition))
#########################################
class MtfThread(threading.Thread):
    def __init__(self , _strThreadName = "MtfThread"):
        self.mutexLock = threading.Lock()
        self.notifyLock = threading.Lock()
        self.CondSignal = threading.Condition(self.notifyLock)
        self.iExit = 0 # 0:running 1:exitng 2:exited
        self.bRunDone = False
        threading.Thread.__init__(self , name = _strThreadName)
        g_Log.LogDebug("MtfThread::__init__ ThreadName=%s Init Successful" % self.getName())
    def run(self):
        tmpCond = CondMutex(self.CondSignal)
        while True:
            tmpCond.Wait()
            if self.iExit == 1:
                break
            self.MtfRun()
            self.bRunDone = True
        self.iExit = 2
    def MtfRun(self):
        self.bRunDone = False
    def GetRunStatus(self):
        return self.bRunDone
    def WakeUp(self):
        tmpCond = CondMutex(self.CondSignal)
        self.bRunDone = False # set task status
        tmpCond.Notify()
    def Wait(self):
        return True
        tmpCond = CondMutex(self.CondSignal)
        tmpCond.Wait()
    def Start(self):
        try:
            self.start()
        except:
            g_Log.LogError("MtfThread::Start Exception:" + _str + traceback.format_exc())
    def Stop(self):
        tmpLock = GuardMutex(self.mutexLock)
        tmpCond = CondMutex(self.CondSignal)
        self.iExit = 1
        tmpCond.Notify()
    def UntilStop(self):
        while self.isAlive():
            self.Stop()
            time.sleep(1)
        self.join()
########################################
class I_CallBack:
    def NotifyTaskDone(self):
        pass
class I_Task:
    def __init__(self , _objCB = None):
        self.objCallBack = _objCB
    def SetTask(self , _obj):  #  任务分配
        pass
    def DoTask(self):  # 执行的任务
        pass
    def DoneTask(self): # 任务完成的会掉函数
        if self.objCallBack is not None:
            self.objCallBack.NotifyTaskDone()
#########################################
class MtfWorker(threading.Thread):
    def __init__(self , _objTarget = None,  _strWorkerName = "MtfWorker" , _objGrp = None):
        self.mutexLock = threading.Lock()
        self.notifyLock = threading.Lock()
        self.CondSignal = threading.Condition(self.notifyLock)
        self.objTarget = _objTarget # 线程执行DoTask对象
        self.myEmployedGrp = _objGrp
        self.bExit = False
        self.bWorking = False
        self.strWoekerId = ""
        threading.Thread.__init__(self , name = _strWorkerName)
        g_Log.LogDebug("MtfWorker::__init__ WorkerName=%s Init Successful" % self.getName())
    def run(self):
        tmpCond = CondMutex(self.CondSignal)
        while not self.bExit:
            tmpCond.Wait()
            self.bWorking = True
            if self.bExit:
                break
            self.DoWork()
            self.bWorking = False
    def SetWorkerId(self , _strId):
        self.strWoekerId = _strId
    def GetWorkerId(self):
        return self.strWoekerId
    def SetWork(self , _obj):
        g_Log.LogDebug("MtfWorker::SetWork WorkerName=%s , Task=%s" % (self.getName() , str(_obj)))
        tmpLock = GuardMutex(self.mutexLock)
        if self.bWorking:
            g_Log.LogWarn("%s:i am working now , can't accept new task" % self.getName())
            return False
        self.SetBusy()
        self.objTarget = _obj[0]
        self.objTarget.SetTask(_obj[1])
        tmpCond = CondMutex(self.CondSignal)
        tmpCond.Notify()  # notify run function comming task and wakeup to execute
        return True
    def DoWork(self):
        g_Log.LogDebug("MtfWorker::DoWork WorkerName=" + self.getName())
        self.objTarget.DoTask()
        self.objTarget.DoneTask()
        self.SetLeisure()
    def Start(self):
        g_Log.LogDebug("MtfWorker::Start WorkerName=" + self.getName())
        try:
            self.start()
        except:
            g_Log.LogError("MtfWorker::Start Exception:" + _str + traceback.format_exc())
    def Stop(self):
        g_Log.LogDebug("MtfWorker::Stop WorkerName=" + self.getName())
        tmpLock = GuardMutex(self.mutexLock)
        tmpCond = CondMutex(self.CondSignal)
        self.bExit = True
        tmpCond.Notify()
    def UntilStop(self):
        g_Log.LogDebug("MtfWorker::UntilStop Beg WorkerName=" + self.getName())
        while self.isAlive():
            self.Stop()
            time.sleep(1)
        self.join()
        g_Log.LogDebug("MtfWorker::UntilStop End WorkerName=" + self.getName())
    def RegistGrp(self , _objGrp): # join _objGrp
        g_Log.LogDebug("MtfWorker::RegistGrp WorkerName=" + self.getName())
        if self.myEmployedGrp is not None:
            self.myEmployedGrp.DismissStaff(self)
        self.myEmployedGrp = _objGrp
        self.myEmployedGrp.MarkWorkerLeisure(self)
    def SetBusy(self):  # changing bWorking state to True and rejecting new task
        g_Log.LogDebug("MtfWorker::SetBusy WorkerName=" + self.getName())
        self.bWorking = True
        self.myEmployedGrp.MarkWorkerBusy(self)  # changing my state in group
    def SetLeisure(self):  # changing bWorking state to False and ready to accept new task
        g_Log.LogDebug("MtfWorker::SetLeisure WorkerName=" + self.getName())
        self.bWorking = False
        self.myEmployedGrp.MarkWorkerLeisure(self)

######################################### 
class MtfWorkerGroup(threading.Thread):
    def __init__(self , _iMaxNum = 4 , _iPermanent = 2 , _strGrpName = "MtfWorkerGroup"):
        threading.Thread.__init__(self , name = _strGrpName)
        self.notifyLock = threading.Lock()
        self.CondSignal = threading.Condition(self.notifyLock)
        self.mutexLock = threading.Lock()
        self.iMaxThreadNum = _iMaxNum
        self.iPermanentNum = _iPermanent
        self.iCurrentNum = 0
        self.iAdjustInterval = 60 * 3 # 秒
        self.dictBusyWorkers = {}
        self.dictLeisureWorkers = {}
        self.bExit = False
        g_Log.LogDebug("MtfWorkerGroup::__init__ WorkerGroupName=%s Init Successful" % self.getName())
    def Regist(self , _worker):
        g_Log.LogDebug("MtfWorkerGroup::Regist WorkerName=" + _worker.getName())
        strId = uuid.uuid1()
        _worker.SetWorkerId(strId)
        _worker.RegistGrp(self)
    def MarkWorkerLeisure(self , _worker):
        g_Log.LogDebug("MtfWorkerGroup::MarkWorkerleisure WorkerName=" + _worker.getName())
        strWoekerId = _worker.GetWorkerId()
        self.dictLeisureWorkers[strWoekerId] = _worker
        try:
            self.dictBusyWorkers.pop(strWoekerId)  # does't deal the except that the key does't exists
        except:
            pass
    def MarkWorkerBusy(self , _worker):
        g_Log.LogDebug("MtfWorkerGroup::MarkWorkerBusy WorkerName=" + _worker.getName())
        strWorkerId = _worker.GetWorkerId()
        self.dictBusyWorkers[strWorkerId] = _worker
        try:
            self.dictLeisureWorkers.pop(strWoekerId) # does't deal the except that the key does't exists
        except:
            pass
    def IncreaseAWorker(self , _strName = "MtfWorker"):
        self.iCurrentNum += 1
        strThreadName = _strName + ("-%02d" % self.iCurrentNum)
        mt = MtfWorker(_strWorkerName = strThreadName)
        mt.Start()        
        self.Regist(mt)
    def Start(self):
        g_Log.LogDebug("MtfWorkerGroup::Start WorkerGroupName=" + self.getName())
        iTmp = 0
        while iTmp < self.iPermanentNum:
            self.IncreaseAWorker()
            iTmp += 1
        self.start()
    def Stop(self):
        tmpLock = GuardMutex(self.mutexLock)
        tmpCond = CondMutex(self.CondSignal)
        self.bExit = True
        tmpCond.Notify()
    def UntilStop(self):
        g_Log.LogDebug("MtfWorkerGroup::UntilStop Beg WorkerGroupName=" + self.getName())
        while self.isAlive():
            self.Stop()
            time.sleep(1)
        self.join()
        g_Log.LogDebug("MtfWorkerGroup::UntilStop End WorkerGroupName=" + self.getName())
    def run(self): # the future manage worker pool to provide better function
        tmpCond = CondMutex(self.CondSignal)
        while not self.bExit:
            g_Log.LogDebug("MtfWorkerGroup::run Before Wait WorkerGroupName=" + self.getName())
            tmpCond.Wait(_timeout = self.iAdjustInterval)
            g_Log.LogDebug("MtfWorkerGroup::run After Wait WorkerGroupName=" + self.getName())
        g_Log.LogDebug("MtfWorkerGroup::run clear dict Beg  WorkerGroupName=" + self.getName())
        tmpLock = GuardMutex(self.mutexLock)
        for strId , tmpThead in self.dictLeisureWorkers.items():
            g_Log.LogDebug("Release Leisure Worker Thread " + tmpThead.getName())
            tmpThead.UntilStop()
        for strId , tmpThead in self.dictBusyWorkers.items():
            g_Log.LogDebug("Release Busy Worker Thread " + tmpThead.getName())
            tmpThead.UntilStop()
        self.dictLeisureWorkers.clear()
        self.dictBusyWorkers.clear()
        g_Log.LogDebug("MtfWorkerGroup::run clear dict End WorkerGroupName=" + self.getName())
    def AcceptTask(self , _objTask , _timetout = None):  # _objTask = (objTask,(objTask.SetWork(此方法的参数)))
        g_Log.LogDebug("MtfWorkerGroup::AcceptTask Task=" + str(_objTask))
        bTimeout = False
        iBegTime = time.time()
        anyWorker = None
        while True:
            self.mutexLock.acquire()
            try:
                anyWorker = self.dictLeisureWorkers.popitem()[1]  # 返回元组(key,value)
            except KeyError:
                anyWorker = None
            self.mutexLock.release()
            if anyWorker is not None :
                break
            iElapseTime = time.time() - iBegTime
            if _timetout is not None and iElapseTime > _timetout:
                bTimeout = True
                break
        if anyWorker is not None:
            anyWorker.SetWork(_objTask)
        return bTimeout == False

