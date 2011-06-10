"""
/***************************************************************************
 ipythonDialog
                                 A QGIS plugin
 An enhanced QGIS console powered by IPython
                             -------------------
        begin                : 2011-02-06
        copyright            : (C) 2011 by Charlie Sharpsteen
        email                : source@sharpsteen.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import sys

# IPython needs sys.argv to be defined
if not hasattr(sys, 'argv'):
    sys.argv = []

from PyQt4.QtCore import Qt, QCoreApplication
from PyQt4.QtGui import QDockWidget, QWidget, QVBoxLayout

from IPython.frontend.qt.console.ipython_widget import IPythonWidget
from IPython.frontend.qt.kernelmanager import QtKernelManager
from IPython.utils.localinterfaces import LOCALHOST

class IPythonConsole(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent)
        self.setObjectName("IPython Console")
        self.setWindowTitle(QCoreApplication.translate("IPython Console", "IPython Console"))
        self.setAllowedAreas(Qt.BottomDockWidgetArea)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)

        self.kernel_manager = QtKernelManager()
        self.kernel_manager.start_kernel()
        self.kernel_manager.start_channels()

        self.console = IPythonWidget(local_kernel=LOCALHOST)
        self.console.kernel_manager = self.kernel_manager
        print dir(self.console)

        self.layout.addWidget(self.console)
        self.setWidget(self.container)

