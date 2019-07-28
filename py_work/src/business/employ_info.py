#!/usr/bin/python
#coding:utf-8

from i_serial_sql import I_Mtf_Serial

class Employ_Info(I_Mtf_Serial):
    def __init__(self  , _listAttr = None):
        if _objList is None:
            self.strEmpolyId = ""
            self.strEmpolyName = ""
            self.strEmpolyNickName = ""
            self.strBirthday = ""
            self.strContact1 = ""
            self.strContact2 = ""
            self.strHomeAddress = ""
            self.strWorkAddress = ""
            self.iJobType = 0
            self.iSalaryType = 0
        else:
            self.strEmpolyId = _listAttr[0]
            self.strEmpolyName = _listAttr[1]
            self.strEmpolyNickName = _listAttr[2]
            self.strBirthday = _listAttr[3]
            self.strContact1 = _listAttr[4]
            self.strContact2 = _listAttr[5]
            self.strHomeAddress = _listAttr[6]
            self.strWorkAddress = _listAttr[7]
            self.iJobType = _listAttr[8]
            self.iSalaryType = _listAttr[9]
    def toStrList(self):
        listEmployInfo = []
        listEmployInfo.append(self.strEmpolyId)
        listEmployInfo.append(self.strEmpolyName)
        listEmployInfo.append(self.strEmpolyNickName)
        listEmployInfo.append(self.strBirthday)
        listEmployInfo.append(self.strContact1)
        listEmployInfo.append(self.strContact2)
        listEmployInfo.append(self.strHomeAddress)
        listEmployInfo.append(self.strWorkAddress)
        listEmployInfo.append(str(self.iJobType))
        listEmployInfo.append(str(self.iSalaryType))
