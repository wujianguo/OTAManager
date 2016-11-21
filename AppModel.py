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
        pf = leancloud.File(self.name + 'appicon.png', io.BytesIO(a.app_icon))
        pf.save()
        self.set('owner', self.owner)
        self.set('name', self.name)
        self.set('displayName', a.bundle_display_name)
        self.set('identifier', a.bundle_identifier)
        self.set('version', a.bundle_version)
        self.set('icon', pf.url)
        self.set('ipa', lf.url)
        super(App, self).save()

    def json_data(self):
        ret = {
            'icon_url': self.get('icon'),
            'ipa_url': self.get('ipa'),
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
