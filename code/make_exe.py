# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
# setup(console=['client.pyw','server.pyw'],options={"py2exe":{"includes":["sip"]}})
# setup(windows=['client.py','server.py'],options={"py2exe":{"includes":["sip"]}})
# setup(windows=['__main__.py'], options={"py2exe":{"includes":["sip"]}})
setup(windows=['aixinwu.py'])

'''
使用方法：
python make_exe.py py2exe
'''
