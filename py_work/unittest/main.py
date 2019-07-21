#!/usr/bin/python
#coding:utf-8

import os, sys, traceback, signal

# 返回Python的根目录
def  LoadThirdParty(_strRootName = "py_work"):
    # 测试用例路径
    strPwd = os.getcwd()
    strRootDir = ""
    iPos = strPwd.find(_strRootName)
    if iPos == -1:
        strRootDir = "../"
    else:
        strRootDir = strPwd[:iPos] + "py_work"
        importpath=[]
        for root , dirs , files in os.walk(strRootDir):
            importpath.append(root)
            sys.path.append(root)
    return strRootDir

g_strRootDir = LoadThirdParty()
import unittest
import HTMLTestRunner

# 将文件名转换为类名
def TransFileName2ClassName(_strFileName):
    posSuffix = _strFileName.find('.py')
    strFileMainName = _strFileName[:posSuffix]
    strSecNames = strFileMainName.split('_')
    strClassName = ''
    for strElement in strSecNames:
        strClassName += strElement.title() + '_'
    else:
        strClassName += 'Test'
    return strFileMainName , strClassName

def ImportTestModule(_strCasePath , _strFilter = ""):
    testFileList = []
    for root , dirs , files in os.walk(_strCasePath):
        if root.find('case') == -1:
            continue
        for filename in files :
            if ((len(_strFilter) > 0 and filename.find(_strFilter) != -1) or len(_strFilter) == 0) \
            and filename.endswith('.py') \
            and filename.find('mjf') == -1:
                testFileList.append(filename)
    testNameList = []
    importModulesList = []
    importClassList = []
    testFileList.sort()
    for strFileName in testFileList:
        names = TransFileName2ClassName(strFileName)
        testNameList.append(names)
        strModule = names[0]
        dyModule = __import__(strModule)
        clsObj = getattr(dyModule , names[1])
        importModulesList.append(dyModule)
        importClassList.append([names[1] , clsObj])
    return importClassList

if __name__ == '__main__':
    strFilter = ""
    if len(sys.argv) > 1:
        strFilter = sys.argv[1]
    testClsLists = ImportTestModule(g_strRootDir + "/unittest/case" , strFilter)
    suite = unittest.TestSuite()
    for clsObj in testClsLists:
        suite.addTest(clsObj[1]('testRun'))
    fp = open('./TestReport.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, verbosity=2, title="MTF", description='TestReport')
    result = runner.run(suite)
