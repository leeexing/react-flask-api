# -*- coding: utf-8 -*-
"""输出类"""
from flask import jsonify

class ResponseHelper:
    """输出帮助类"""
    @staticmethod
    def return_true_data(data, msg='success', status=True, **kwargs):
        """返回正确结果"""
        return jsonify({
            "result": status,
            "data": data,
            "msg": msg,
            **kwargs
        })

    @staticmethod
    def return_false_data(data=None, msg="error", status=False, **kwargs):
        """返回错误结果"""
        return jsonify({
            "result": status,
            "data": data,
            "msg": msg,
            **kwargs
        })
