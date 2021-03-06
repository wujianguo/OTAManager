#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import json
import urllib.parse
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.escape
import AppModel

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")

class LinkHandler(tornado.web.RequestHandler):
    
    def get(self, name):
        image_url = "https://coding.net/static/project_icon/scenery-12.png"
        description = "description"
        button = "button"
        self.render("test.html", name=name, image_url=image_url, description=description, button=button)


class AppleAssociationHandler(tornado.web.RequestHandler):
    
    def get(self):
        ret = {
            "applinks": {
                "apps": [],
                "details": [
                    {
                        "appID": "ZEDNAR7A4E.com.haixue.app.nim",
                        "paths": [ "/link/*"]
                    }
                ]
            }
        }
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(ret)) 

class InstallHandler(tornado.web.RequestHandler):

    def get(self, owner, name):
        try:
            app = AppModel.query(owner, name)
            plist_url = '{0}://{1}/{2}/{3}.plist'.format("https", self.request.host, owner, name)
            qrcode = 'http://qr.topscan.com/api.php?w=200&text={0}'.format(urllib.parse.quote(self.request.full_url()))
            self.render("install.html", name=name, description='在safari打开并点击安装', url=plist_url, qrcode=qrcode)
        except:
            self.set_status(404)

class PListHandler(tornado.web.RequestHandler):

    def get(self, owner, name):
        try:
            app = AppModel.query(owner, name)
            self.render("install.plist", name=name, ipa=app.get('ipa_url'), icon=app.get('icon_url'), identifier=app.get('identifier'), version=app.get('version'))
        except:
            self.set_status(404)

class AppHandler(tornado.web.RequestHandler):

    def get(self, owner, name):
        try:
            app = AppModel.query(owner, name)
            plist_url = '{0}://{1}/{2}/{3}.plist'.format("https", self.request.host, owner, name)
            html_url = '{0}://{1}/install/{2}/{3}'.format("https", self.request.host, owner, name)
            ret = app.json_data()
            ret.update({'code': 0, 'msg': '', 'html_url': html_url, 'plist_url': plist_url})
            # ret = {'code': 0,
            #     'msg': '',
            #     'html': html_url,
            #     'plist_url': plist_url,
            #     'icon_url': app.get('icon'),
            #     'ipa_url': app.get('ipa'),
            #     'display_name': app.get('displayName'),
            #     'identifier': app.get('identifier'),
            #     'version': app.get('version'),
            #     'owner': app.get('owner'),
            #     'name': app.get('name'),
            #     'created_at': str(app.created_at),
            #     'updated_at': str(app.updated_at)
            #     }
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(ret))
        except:
            self.set_status(404)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps({'code': 404, 'msg': 'not found'}))

    def post(self, owner, name):
        file_metas = self.request.files['file']
        for meta in file_metas:
            app = AppModel.App(owner, meta['filename'], meta['body'], name)
            app.save()
            plist_url = '{0}://{1}/{2}/{3}.plist'.format("https", self.request.host, owner, name)
            html_url = '{0}://{1}/install/{2}/{3}'.format("https", self.request.host, owner, name)
            ret = app.json_data()
            ret.update({'code': 0, 'msg': '', 'html_url': html_url, 'plist_url': plist_url})
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(ret))
            break

class AppsHandler(tornado.web.RequestHandler):

    def get(self, owner):
        self.write("hello2")

    def post(self, owner):
        file_metas = self.request.files['file']
        for meta in file_metas:
            app = AppModel.App(owner, meta['filename'], meta['body'], None)
            app.save()
            name = app.get('name')
            plist_url = '{0}://{1}/{2}/{3}.plist'.format("https", self.request.host, owner, name)
            html_url = '{0}://{1}/install/{2}/{3}'.format("https", self.request.host, owner, name)
            ret = app.json_data()
            ret.update({'code': 0, 'msg': '', 'html_url': html_url, 'plist_url': plist_url})
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(ret))
            break


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "public"),
    "template_path": os.path.join(os.path.dirname(__file__), "views"),
    "gzip": True,
    "debug": True
}

application = tornado.web.Application([
    # (r"/", MainHandler),
    (r"/apple-app-site-association", AppleAssociationHandler),
    (r"/link/(.*)", LinkHandler),
    (r"/install/(.*)/(.*)", InstallHandler),
    (r"/(.*)/(.*).plist", PListHandler),
    (r"/api/(.*)/(.*)", AppHandler),
    (r"/api/(.*)", AppsHandler),
], **settings)

app = tornado.wsgi.WSGIAdapter(application)


def main():
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
