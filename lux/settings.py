
# First we set the SIP API to force PyQt to use the more modern
# QStrings and QVariants that are transparently converted into python
# strings.
#
# Note: in order for this change to take effect, you need to import
# settings.py *before* importing any other QT headers into your
# program.  It's easiest to put this import statement at the very top
# of your main program file.
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtCore

class LuxSettings(QtCore.QSettings):
    """
    The settings class manages state that persists between program
    instances.  This settings class is fully re-entrant, and settings
    can even be shared across multiple running instances of the
    program.

    For more information, refer to the section on "Accessing Settings
    from Multiple Threads or Processes Simultaneously" at
    http://www.opendocs.net/pyqt/pyqt4/html/qsettings.html
    """

    def __init__(self):
        QtCore.QSettings.__init__(self, QtCore.QSettings.IniFormat,
                                  QtCore.QSettings.UserScope,
                                  'False Profit LLC', 'Fiat Lux')
        self.__initialised = True  # for __setattr__

    # To make the code cleaner, we will expose all of the Qt settings
    # as attributes of the settings class. 
    def __getattr__(self, key):
        if (not self.contains(key)):
            raise AttributeError("Settings object does not contain the key \"" + str(key) + "\"")

        return self.value(key)

    def __setattr__(self, key, value):
        # this test allows attributes to be set in the __init__ method
        if not self.__dict__.has_key('_Settings__initialised'):
            return dict.__setattr__(self, key, value)

        # Otherwise, we delegate attributes to qsettings
        return self.setValue(key, value)

    
