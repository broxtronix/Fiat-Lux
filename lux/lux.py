"""
Main application for Fiat Lux
"""
import sys
import os, time
import os.path

# It's important that we import the settings before anything else Qt
# related, because the settings sets the SIP API to version 2.
# Hopefully this won't matter in the future when the transition to SIP
# 2 is complete.
from settings import *
settings = LuxSettings()

# allow eggs to be dropped into application folder, as well as script
# overrides, etc.
sys.path = ['.'] + sys.path

# create the application
from PyQt4 import QtCore, QtGui
app = QtGui.QApplication(sys.argv)

# set up my application
QtCore.QCoreApplication.setOrganizationName(organization_name)
QtCore.QCoreApplication.setOrganizationDomain(organization_domain)
QtCore.QCoreApplication.setApplicationName(application_name)

# set defaults
if (not settings['app'].contains('resource_path') or
    not os.path.exists(os.path.join(settings['app'].resource_path, 'splash.png'))):
    # load resource location
    cwd = os.getcwd()
    if not sys.argv[0]:
        resource_path = cwd
    else:
        resource_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    settings['app'].resource_path = resource_path

# Show the splash screen
splash_path = os.path.join(settings['app'].resource_path, 'splash.png')
splash = QtGui.QSplashScreen(QtGui.QPixmap(splash_path))
splash.show()

# Start up the LUX main engine.  This starts a thread that runs lux plugins.
import lux_engine
lux_engine = lux_engine.LuxEngine()
lux_engine.start()

# Start up the LUX main engine.  This starts a thread that runs lux plugins.
import xenon_lux
audio_engine = xenon_lux.LuxAudioEngine("lux_audio_engine")

# Start up the rest of the GUI
import mainwindow
mainWindow = mainwindow.MainWindow()
mainWindow.show()

#time.sleep(1)
splash.finish(mainWindow)

# run the application
result=app.exec_()

# exit
lux_engine.exit()
sys.exit(result)
