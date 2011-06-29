"""
Main application for Fiat Lux
"""
import sys
import os, time
import os.path
import traceback

# Set this to 1 to enable console exceptions.
DEV_MODE = 0

# It's important that we import the settings before anything else Qt
# related, because the settings sets the SIP API to version 2.
# Hopefully this won't matter in the future when the transition to SIP
# 2 is complete.
from settings import *
settings = LuxSettings()

# allow eggs to be dropped into application folder, as well as script
# overrides, etc.
sys.path = ['.'] + sys.path

# Create the application.  Note thet we set the plugin path explicitly
# here so that the app doesn't get confused once we bundle it using
# py2app.
from PyQt4 import QtCore, QtGui
app = QtGui.QApplication(sys.argv)
QtGui.QApplication.setLibraryPaths([QtGui.QApplication.applicationDirPath() + '../PlugIns'])

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

# Start the main lux engine.  There is a very good chance that there
# will sometimes be buggy code coming in via the plugins here, so we
# must be proactive about catching errors.
try:
    # Initialize the audio engine
    from audio import audio_engine

    # Create the video engine
    print '\t--> Starting Video Engine'
    from video import video_engine

    # Create the output engine
    import xenon_lux
    output_engine = xenon_lux.LuxOutputEngine("lux_output")

    # Start up the LUX main engine.  This starts a thread that runs lux plugins.
    import lux_engine
    lux_engine = lux_engine.LuxEngine(audio_engine, video_engine, output_engine)
    lux_engine.start()

    # Start up the rest of the GUI
    import mainwindow
    mainWindow = mainwindow.MainWindow(lux_engine, output_engine)
    mainWindow.show()

    splash.finish(mainWindow)

    # run the application
    result=app.exec_()
    lux_engine.exit()

except:
    # First, disable the laser output.  We don't want to put any eyes out! 
    output_engine.setOutputInitialized(False)
    
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_string = '-' * 60 + '\n'
    error_string += "An exception occurred:\n\n"
    error_string += traceback.format_exc()
    error_string +=  '-' * 60
    if (DEV_MODE):
        print error_string
    else:
        QtGui.QMessageBox.critical(None, 'Plugin Error',  error_string)
finally:

    print "An exception occurred that could not be handled.  Exiting.\n";
    sys.exit(0);

    
