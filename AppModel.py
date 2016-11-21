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
        lf = leancloud.File(self.name + '.ipa', f)
        lf.save()
        if a.app_icon:
            pf = leancloud.File(self.name + 'appicon.png', io.BytesIO(a.app_icon))
            pf.save()
        else:
            pf = leancloud.File(self.name + 'appicon.png', 'https://dn-J3ta8gqr.qbox.me/38ec7dc7c6edff00.png')
            pf.save()
        icon_url = pf.url
        thumbnail_url = pf.get_thumbnail_url(width=50, height=50)
        self.set('owner', self.owner)
        self.set('name', self.name)
        self.set('displayName', a.bundle_display_name)
        self.set('identifier', a.bundle_identifier)
        self.set('version', a.bundle_version)
        self.set('icon_url', icon_url)
        self.set('icon_thumbnail_url', thumbnail_url)
        self.set('ipa_url', lf.url)
        super(App, self).save()

    def json_data(self):
        ret = {
            'icon_url': self.get('icon_url'),
            'ipa_url': self.get('ipa_url'),
            'display_name': self.get('displayName'),
            'identifier': self.get('identifier'),
            'version': self.get('version'),
            'owner': self.get('owner'),
            'name': self.get('name'),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
            }
        return ret

def query(owner, name):
    q = App.query
    q.equal_to('owner', owner)
    q.equal_to('name', name)
    q.add_descending('updatedAt')
    return q.first()

def main():
    pass

if __name__ == '__main__':
    main()
