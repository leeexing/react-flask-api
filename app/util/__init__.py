# -*- coding: utf-8 -*-
from .response import ResponseHelper

def stripBlank(originStr, sliceStart=0):
    return originStr.replace('\n', '').replace(' ', '')[sliceStart:]