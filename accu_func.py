#!/bin/env python
# coding: utf8
#
#
# @file:    accu_func
# @author:  chosen0ne(louzhenlin86@126.com)
# @date:    2015/01/20 21:55:17

import sys
from datetime import datetime


time_fields = set(['st_ctime', 'st_atime', 'st_mtime'])


def datetime_val(field, val):
    if field not in time_fields:
        return val
    d = datetime.fromtimestamp(val)
    return d.strftime('%Y-%m-%d %H:%M:%S')


class AccuFuncCls(object):
    def val(self):
        pass

    def __call__(self, field, finfo):
        pass

    def desp(self):
        pass


class CountFuncCls(AccuFuncCls):
    def __init__(self, field):
        self._count = 0
        self._field = field

    def __call__(self, finfo):
        self._count += 1

    def val(self):
        return self._count

    def desp(self):
        return 'count', '*'


class SumFuncCls(AccuFuncCls):
    def __init__(self, field):
        self._total = 0
        self._field = field

    def __call__(self, finfo):
        self._total += getattr(finfo['stat'], self._field)

    def val(self):
        return self._total

    def desp(self):
        return 'sum', self._field


class MaxFuncCls(AccuFuncCls):
    def __init__(self, field):
        self._max = 0
        self._field = field

    def __call__(self, finfo):
        v = getattr(finfo['stat'], self._field)
        if v > self._max:
            self._max = v

    def val(self):
        return datetime_val(self._field, self._max)

    def desp(self):
        return 'max', self._field


class MinFuncCls(AccuFuncCls):
    def __init__(self, field):
        self._min = sys.maxint
        self._field = field

    def __call__(self, finfo):
        v = getattr(finfo['stat'], self._field)
        if v < self._min:
            self._min = v

    def val(self):
        return datetime_val(self._field, self._min)

    def desp(self):
        return 'min', self._field


class AvgFuncCls(AccuFuncCls):
    def __init__(self, field):
        self._count = 0
        self._total = 0
        self._field = field

    def __call__(self, finfo):
        self._total += getattr(finfo['stat'], self._field)
        self._count += 1

    def val(self):
        return self._total / self._count / 1.0

    def desp(self):
        return 'avg', self._field
