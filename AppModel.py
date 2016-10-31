#!/usr/bin/env python
# -*- coding: utf-8 -*-

import leancloud
import ipa
import io

class App(leancloud.Object):

    def __init__(self, owner=None, file_name=None, file=None, name=None):
        leancloud.Object.__init__(self)
        self.owner = owner
        self.file_name = file_name
        self.file = file
        self.name = name

    def save(self):
        f = io.BytesIO(self.file)
        a = ipa.IPA(f)
        if not self.name:
            self.name = a.bundle_name
        lf = leancloud.File(self.file_name, f)
        pf = leancloud.File(a.bundle_name + 'appicon.png', io.BytesIO(a.app_icon))
        self.set('owner', self.owner)
        self.set('name', self.name)
        self.set('displayName', a.bundle_display_name)
        self.set('identifier', a.bundle_identifier)
        self.set('version', a.bundle_version)
        self.set('icon', pf.url)
        self.set('ipa', lf.url)
        super(App, self).save()

def query(owner, name):
    q = App.query
    q.equal_to('owner', owner)
    q.equal_to('name', name)
    q.add_descending('updatedAt')
    return q.first()
