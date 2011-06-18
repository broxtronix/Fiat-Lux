from setuptools import setup
import sys, os, shutil

APP = ['lux.py']
DATA_FILES = [('',['splash.png'])]

# plist rewriting to enable the egg
python_lib_folder = 'lib/python%d.%d' % (sys.version_info[0:2])
PLIST = {'PyResourcePackages':
         [python_lib_folder,
          os.path.join(python_lib_folder, 'lib-dynload'),
          os.path.join(python_lib_folder, 'site-packages'),
          ],
         'CFBundleName':"Fiat Lux",
         'CFBundleDisplayName':"Fiat Lux",
         }

OPTIONS = {'argv_emulation': False,
           'plist' : PLIST,
           'iconfile': 'lux.icns',
           'includes': ['sip'],
           'resources' : []
}
			
setup(
	app=APP,
        data_files=DATA_FILES,
	options={'py2app': OPTIONS},
	setup_requires=['py2app'],
)

