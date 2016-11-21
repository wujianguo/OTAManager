#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
import os
import leancloud
from gevent.pywsgi import WSGIServer
from cloud import engine

APP_ID = os.environ['LEANCLOUD_APP_ID']
APP_KEY = os.environ['LEANCLOUD_APP_KEY']
MASTER_KEY = os.environ['LEANCLOUD_APP_MASTER_KEY']
PORT = int(os.environ['LEANCLOUD_APP_PORT'])

leancloud.init(APP_ID, app_key=APP_KEY, master_key=MASTER_KEY)
# 如果需要使用 master key 权限访问 LeanCLoud 服务，请将这里设置为 True
leancloud.use_master_key(False)

application = engine
# 使用 `leancloud.HttpsRedirectMiddleware` 这个 WSGI 中间件包装一下原始的提供给 LeanEngine 的 WSGI 函数
# application = leancloud.HttpsRedirectMiddleware(application)

if __name__ == '__main__':
    server = WSGIServer(('localhost', PORT), application)
    server.serve_forever()
