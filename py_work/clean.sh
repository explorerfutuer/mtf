#!/bin/bash

find . -name __pycache__ | xargs rm -rf
rm -f ./unittest/TestReport.html
rm -rf ./unittest/debug
rm -rf ./unittest/data
rm -rf ./unittest/cfgmtf
