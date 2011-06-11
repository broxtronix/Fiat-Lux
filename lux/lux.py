"""
Main application for Fiat Lux
"""
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui
import sys
import os, time
import os.path

# allow eggs to be dropped into application folder, as well as script
# overrides, etc.
sys.path = ['.'] + sys.path

from settings import Settings

# create the application
app = QtGui.QApplication(sys.argv)

# load up settings
qt_settings = QtCore.QSettings(QtCore.QSettings.IniFormat,
                               QtCore.QSettings.UserScope,
                               'False Profit LLC',
                               'Fiat Lux')
settings = Settings(qt_settings)

# set defaults
if (not settings.contains('app/resource_path') or
    not os.path.exists(os.path.join(settings.getString('app/resource_path'), 'splash.png'))):
    # load resource location
    cwd = os.getcwd()
    if not sys.argv[0]:
        resource_path = cwd
    else:
        resource_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    settings.setValue('app/resource_path',resource_path)

# Show the splash screen
splash_path = os.path.join(settings.getString('app/resource_path'), 'splash.png')
splash = QtGui.QSplashScreen(QtGui.QPixmap(splash_path))
splash.show()

# set up my application
QtCore.QCoreApplication.setOrganizationName('False Profit LLC')
QtCore.QCoreApplication.setOrganizationDomain('false-profit.com')
QtCore.QCoreApplication.setApplicationName('Fiat Lux')

# Start up the LUX main engine.  This starts a thread that runs lux plugins.
import lux_engine
lux_engine = lux_engine.LuxEngine()
lux_engine.start()

# Start up the rest of the GUI
import mainwindow
mainWindow = mainwindow.MainWindow(settings)
mainWindow.show()

#time.sleep(1)
splash.finish(mainWindow)

# run the application
result=app.exec_()

# exit
lux_engine.exit()
sys.exit(result)
