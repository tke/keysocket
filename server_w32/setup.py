from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1, 'optimize': 2, 'compressed':True}},
    windows = [{'script': "server.pyw"}],
    zipfile = None,
)
