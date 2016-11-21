#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile
import plistlib
import re

class IPA:

    def __init__(self, file):
        self.zip = zipfile.ZipFile(file)
        self.__plist = None

    @property
    def bundle_display_name(self):
        return self.plist.get('CFBundleDisplayName')

    @property
    def bundle_name(self):
        return self.plist.get('CFBundleName')

    @property
    def bundle_identifier(self):
        return self.plist.get('CFBundleIdentifier')

    @property
    def bundle_version(self):
        return self.plist.get('CFBundleShortVersionString')

    @property
    def app_icon(self):
        pattern = re.compile(r'Payload/[^/]*.app/AppIcon60x60@3x.png')
        for path in self.zip.namelist():
            m = pattern.match(path)
            if m is not None:
                return self.zip.read(m.group())

    @property
    def plist(self):
        if self.__plist:
            return self.__plist

        pattern = re.compile(r'Payload/[^/]*.app/Info.plist')
        for path in self.zip.namelist():
            m = pattern.match(path)
            if m is not None:
                # print(m)
                data = self.zip.read(m.group())
                self.__plist = plistlib.loads(data)
        return self.__plist



def main():
    pass

if __name__ == '__main__':
    main()
