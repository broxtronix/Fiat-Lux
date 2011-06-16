from setuptools import setup
import sys, os

APP = ['lux.py']
DATA_FILES = [('',['splash.png'])]

# plist rewriting to enable the egg
python_lib_folder = 'lib/python%d.%d' % (sys.version_info[0:2])
PLIST = {'PyResourcePackages':
         [python_lib_folder,
          os.path.join(python_lib_folder, 'lib-dynload'),
          os.path.join(python_lib_folder, 'site-packages.zip'),
          ],
         }

OPTIONS = {'argv_emulation': False,
           'plist' : PLIST,
           'includes': ['sip'],
#           'excludes':['PyQt4.QtDesigner','PyQt4.QtNetwork','PyQt4.QtOpenGl','PyQt4.QtScript','PyQt4.QtSql','PyQt4.QtTest','PyQt4.QtWebKit','PyQt4.QtXml','PyQt4.phonon'],
           'resources' : []
}
			
setup(
	app=APP,
        data_files=DATA_FILES,
	options={'py2app': OPTIONS},
	setup_requires=['py2app'],
)
