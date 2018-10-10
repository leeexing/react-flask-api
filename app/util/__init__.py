# -*- coding: utf-8 -*-
import re
from .response import ResponseHelper

def stripBlank(originStr, sliceStart=0):
    """将字符串中的换行符和空格去掉"""
    return originStr.replace('\n', '').replace(' ', '')[sliceStart:]

def repalceBlank2None(originStr, pattern=''):
    """正则表达式也是很溜的啊"""
    return re.sub(r'\\n|\s+', pattern, originStr)