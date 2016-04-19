#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from datetime import datetime, timedelta


def parse_date(date):
    ret_date = None
    if u'小时前' in date:  # 22小时前
        hours = int(date.split(u'小时前', 1)[0])
        now = datetime.now() - timedelta(hours=hours)
        ret_date = datetime(now.year, now.month, now.day, now.hour)
    elif u'天前' in date:  # 4天前
        days = int(date.split(u'天前', 1)[0])
        now = datetime.now() - timedelta(days=days)
        ret_date = datetime(now.year, now.month, now.day)
    elif u'周前' in date or u'个月前' in date:  # 4个月前 (12-06)
        date_str = date.split("(", 1)[1][:-1]
        month, day = date_str.split("-")
        month = int(month)
        day = int(day)
        now = datetime.now()
        ret_date = datetime(now.year, month, day)
        if ret_date > now:
            ret_date = datetime(ret_date.year - 1,
                                ret_date.month, ret_date.day)
    elif u'年前' in date:  # 2年前 (2013-12-29)
        date_str = date.split("(", 1)[1][:-1]
        year, month, day = date_str.split("-")
        year = int(year)
        month = int(month)
        day = int(day)
        ret_date = datetime(year, month, day)

    return ret_date


def join_text(text):
    text_splited = text.split(u"\n")
    return u"".join([x.strip() for x in text_splited])