"""
A wrapper for the Qt settings class
"""

from PyQt4 import QtCore

class Error(Exception):
    pass

class Settings:
    def __init__(self, settings):
        self._qt_settings = settings

    def __getattr__(self, name):
        return getattr(self._qt_settings,name)

    def value(self, key, defaultValue=None):
        if defaultValue == None:
            return self._qt_settings.value(key)
        else:
            return self._qt_settings.value(key, QtCore.QVariant(defaultValue))

    def setValue(self, key, value):
        self._qt_settings.setValue(key, QtCore.QVariant(value))

    def setExpression(self, key, value):
        self._qt_settings.setValue(key, QtCore.QVariant(repr(value)))

    def getInteger(self, key, defaultValue=None):
        value, ok = self.value(key, defaultValue).toInt()
        if ok:
            return int(value)
        else:
            raise Error('Unable to decode integer '+str(key)+' in settings')

    def getFloat(self, key, defaultValue=None):
        value, ok = self.value(key, defaultValue).toDouble()
        if ok:
            return float(value)
        else:
            print ('WARNING: Unable to decode float '+
                   str(key) +' in settings. Returning default value.')
            return 1.0
        

    def getString(self, key, defaultValue=None):
        return str(self.value(key, defaultValue).toString())

    def getBool(self, key, defaultValue=None):
        return bool(self.value(key, defaultValue).toBool())

    def getExpression(self, key, defaultValue=None):
        return eval(self.value(key, repr(defaultValue)).toString())
