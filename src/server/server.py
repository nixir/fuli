#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
# insert lib path
sys.path.insert(0, '../libs')
import json
import math
import pymongo
from flask import Flask, request
from flask import render_template
from flask.ext.bootstrap import Bootstrap
import db


app = Flask(__name__)
bootstrap = Bootstrap(app)


def get_pagination(page, total, range_num=3):
    page_list = []
    # left
    for i in xrange(range_num, 0, -1):
        cur_page = page - i
        if cur_page > 0:
            page_list.append(cur_page)

    # current
    page_list.append(page)

    # right
    for i in xrange(1, range_num + 1):
        cur_page = page + i
        if page < cur_page <= total:
            page_list.append(cur_page)

    prev_page = max(1, page - 1)
    next_page = min(total, page + 1)

    ret = {
        'first_page': 1, 'last_page': total, 'page_list': page_list,
        'prev_page': prev_page, 'next_page': next_page, 'cur_page': page,
    }
    return ret


@app.route('/page/<page>')
def page(page):
    ln = 10
    try:
        page = int(page)
    except ValueError:
        page = 1

    timeline = db.get_collection('timeline')
    db_items = timeline.find(
        skip=(page - 1) * ln,
        limit=ln,
        sort=[('date', pymongo.DESCENDING)],
    )
        #{'date': {'$exist': True}},
    items = []
    for item in db_items:
        try:
            item['date'] = str(item['date'].strftime('%Y-%m-%d'))
        except:
            pass
        item['_id'] = str(item['_id'])
        items.append(item)

    # pagination
    total = int(math.ceil(float(timeline.find().count()) / ln))
    pagination = get_pagination(page, total)

    return render_template(
        'timeline.html',
        items=items,
        pagination=pagination,
    )


@app.route('/')
def index():
    return page(1)

if __name__ == '__main__':
    app.run(debug=True, host="192.168.3.104", port=8888)
