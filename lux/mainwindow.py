"""
Main window for Fiat Lux
"""

from PyQt4 import QtCore, QtGui

import os.path
import display
#from console import IPythonConsole

class SettingsPanel(QtGui.QDockWidget):
    """
    A basic settings panel widget
    """
    def __init__(self, name='', message='', widget=None, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setObjectName(name)
        self.setWindowTitle(name)
        # the default label
        self.label = QtGui.QLabel(message)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        # the stack holding the label and setting page
        self.stack = QtGui.QStackedWidget()
        self.stack.addWidget(self.label)
        # the scroller holding the stack
        self.scroller = QtGui.QScrollArea()
        self.scroller.setWidget(self.stack)
        self.scroller.setWidgetResizable(True)
        # add the scoller
        self.setWidget(self.scroller)

        if widget:
            self.placeWidget(widget)

    def placeWidget(self, widget):
        "Place a widget into this setting panel and make it active"
        index = self.stack.addWidget(widget)
        self.stack.setCurrentIndex(index)

    def removeWidget(self, widget=None):
        "Remove a widget from the setting panel"
        if not widget: widget = self.stack.currentWidget()
        if widget == self.label: return
        self.stack.removeWidget(widget)

    def widget(self):
        return self.stack.currentWidget()

class SettingsPanelManager:
    """
    A manager for all the settings panels
    """
    def __init__(self, parent):
        self._parent = parent
        self._settings = []

    def add(self, panel):
        "Add a settings panel, initially all on the right in a tab"
        if panel not in self._settings:
            if self._settings:
                self._parent.tabifyDockWidget(self._settings[-1],panel)
            else:
                self._parent.addDockWidget(QtCore.Qt.RightDockWidgetArea,
                                           panel)
            self._settings.append(panel)
        else:
            raise Error('Attempting to add the same panel twice')

    def remove(self, panel):
        if panel in self._settings:
            self._parent.removeDockWidget(panel)
            self._settings.remove(panel)
        else:
            raise Error('Attempting to remove a panel that was not added')

    def __getitem__(self, key):
        for panel in self._settings:
            if panel.windowTitle() == key:
                return panel
        return None

    def toggleViewActions(self):
        "Get a list of view actions for all the settings panels"
        actions = [x.toggleViewAction() for x in self._settings]
        for x,y in zip(actions, self._settings):
            x.setText(y.windowTitle())
        return actions

class MainWindow(QtGui.QMainWindow):
    def __init__(self, settings, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        # set application settings
        self.settings = settings

        # set display stuff
        self.zoom = 1.0

        # set our title
        self.setWindowIcon(QtGui.QIcon())
        self.setWindowTitle('Fiat Lux')

        # create the simulation widget
        self.simWidget = display.SimulationDisplay(self.settings, self)
        self.setCentralWidget(self.simWidget)

#        self.ipythonWidget = IPythonConsole(self)
#        self.setCentralWidget(self.ipythonWidget)
        

        # set up the status bar
        self.statusBar_ = QtGui.QStatusBar(self)
        self.zoomStatus = QtGui.QLabel()
        self.zoomStatus.setMargin(2)
        self.setStatus() # set a default status
        self.statusBar_.addWidget(self.zoomStatus)
        self.setStatusBar(self.statusBar_)

        # setup our actions
        self.streamAction = QtGui.QAction(QtGui.QIcon(self.resource('play.png')),
                                          '&Stream',
                                          self)
        self.streamAction.setShortcut(QtCore.Qt.ALT + QtCore.Qt.Key_S)
        self.streamAction.setToolTip('Start/stop streaming frames from the camera.')
        self.streamAction.setCheckable(True)
        self.streamAction.setEnabled(False)
        # self.connect(self.streamAction,
        #              QtCore.SIGNAL('triggered(bool)'),
        #              self.playTriggered)

        # make a pause icon
        self.pauseAction = QtGui.QAction(QtGui.QIcon(self.resource('pause.png')),
                                          '&Pause',
                                          self)
        self.pauseAction.setShortcut(QtCore.Qt.ALT + QtCore.Qt.Key_P)
        self.pauseAction.setToolTip('Pause/resume streaming frames from the camera.')
        self.pauseAction.setCheckable(True)
        self.pauseAction.setEnabled(False)
        # self.connect(self.pauseAction,
        #              QtCore.SIGNAL('triggered(bool)'),
        #              self.pauseTriggered)

        self.recordAction = QtGui.QAction(QtGui.QIcon(self.resource('record.png')),
                                          '&Record',
                                          self)
        self.recordAction.setShortcut(QtCore.Qt.ALT + QtCore.Qt.Key_R)
        self.recordAction.setToolTip('Record the streamed frames to disk.')
        self.recordAction.setCheckable(True)
        self.recordAction.setEnabled(False)
        # self.connect(self.recordAction,
        #              QtCore.SIGNAL('triggered(bool)'),
        #              self.record)

        self.quitAction = QtGui.QAction('&Quit', self)
        self.quitAction.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.quitAction.setToolTip('Exit the program.')
        self.connect(self.quitAction,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.close)

        # add radio buttons
        self.displayPrefix = QtGui.QLabel(' View as: ')
        self.displayPrefix.setAlignment(QtCore.Qt.AlignVCenter)
        self.displayRawButton = QtGui.QRadioButton('Raw image')
        self.displayRawButton.setToolTip('Show the raw image, either coming from\nthe camera sensor or loaded from a file.')
        self.displayPinholeButton = QtGui.QRadioButton('Pinhole 3D (reset focus and pan)')
        self.displayPinholeButton.setToolTip('Show the light field as viewed through a pinhole.\nThis resets the focus and pan settings in the Optics tab.') 
        self.displayApertureButton = QtGui.QRadioButton('3D')
        self.displayApertureButton.setToolTip('Show a rendered 3D light field.')

        # self.connect(self.displayRawButton,
        #              QtCore.SIGNAL('clicked()'),
        #              self.emitDisplayModeChanged)
        # self.connect(self.displayPinholeButton,
        #              QtCore.SIGNAL('clicked()'),
        #              self.emitDisplayModeChanged)
        # self.connect(self.displayApertureButton,
        #              QtCore.SIGNAL('clicked()'),
        #              self.emitDisplayModeChanged)

        # set up the toolbars
        self.controlBar = QtGui.QToolBar(self)
        self.controlBar.setObjectName('Control Bar')
        self.controlBar.addAction(self.streamAction)
        self.controlBar.addAction(self.pauseAction)
        self.controlBar.addAction(self.recordAction)
        self.displayBar = QtGui.QToolBar(self)
        self.displayBar.setObjectName('Display Mode Bar')
        self.displayBar.addWidget(self.displayPrefix)
        self.displayBar.addWidget(self.displayRawButton)
        self.displayBar.addWidget(self.displayPinholeButton)
        self.displayBar.addWidget(self.displayApertureButton)
        self.addToolBar(self.controlBar)
        self.addToolBar(self.displayBar)

        # toolbar view control
        self.viewControlBarAction = self.controlBar.toggleViewAction()
        self.viewControlBarAction.setText('&Controls')
        self.viewDisplayBarAction = self.displayBar.toggleViewAction()
        self.viewDisplayBarAction.setText('&Display mode')

        # set up the settings panels
        self.settingsManager = SettingsPanelManager(self)
        
        # self.settingsManager.add(SettingsPanel(name = "Input",
        #                                        message = "No input selected.\nPlease open an input from the Data menu"
        #                                        ))
        # self.settingsManager.add(SettingsPanel(name = "Output",
        #                                        message = "No output selected.\nPlease choose an output from the Data menu"
        #                                        ))
        self.settingsManager.add(SettingsPanel(name = "Simulation",
                                               message = "",
                                               widget = display.SimulationSettings(self.simWidget)
                                               ))
        # self.settingsManager.add(SettingsPanel(name = "Lenslet",
        #                                        message = "",
        #                                        widget = display.LensletSettings(self.dispWidget)
        #                                        ))
        # self.settingsManager.add(SettingsPanel(name = "Optics",
        #                                        message = "",
        #                                        widget = display.OpticsSettings(self.dispWidget)
        #                                        ))
        
        # # create the open input menu
        # self.inputMenu = QtGui.QMenu('&Open input')
        # self.inputActions = []
        # # add in each input one by one
        # for inputInstance in self.inputs:
        #     inputAction = self.inputMenu.addAction(inputInstance.name)
        #     inputAction.setStatusTip(inputInstance.description)
        #     #inputAction.setCheckable(True)
        #     self.connect(inputAction,
        #                  QtCore.SIGNAL('triggered(bool)'),
        #                  self.openInputInstance)
        #     self.inputActions.append(inputAction)
        # # create the close input action
        # self.closeInputAction = QtGui.QAction('&Close input',
        #                                       self)
        # self.closeInputAction.setStatusTip('Close the currently open input.')
        # self.closeInputAction.setEnabled(False)
        # self.connect(self.closeInputAction,
        #              QtCore.SIGNAL('triggered(bool)'),
        #              self.closeInput)

        # # create the open output menu
        # self.outputMenu = QtGui.QMenu('O&pen output')
        # self.outputActions = []
        # # add in each output one by one
        # defaultOutput = None
        # for outputInstance in self.outputs:
        #     outputAction = self.outputMenu.addAction(outputInstance.name)
        #     outputAction.setStatusTip(outputInstance.description)
        #     #outputAction.setCheckable(True)
        #     if not defaultOutput:
        #         defaultOutput = outputAction
        #     self.connect(outputAction,
        #                  QtCore.SIGNAL('triggered(bool)'),
        #                  self.openOutputInstance)
        #     self.outputActions.append(outputAction)
        # # create the close output action
        # self.closeOutputAction = QtGui.QAction('C&lose output',
        #                                       self)
        # self.closeOutputAction.setStatusTip('Close the currently open output.')
        # self.closeOutputAction.setEnabled(False)
        # self.connect(self.closeOutputAction,
        #              QtCore.SIGNAL('triggered(bool)'),
        #              self.closeOutput)

        # set up the menu bar
        self.menuBar_ = QtGui.QMenuBar(self)
        self.controlMenu = self.menuBar_.addMenu('&Control')
        self.controlMenu.addAction(self.quitAction)
        # self.dataMenu = self.menuBar_.addMenu('&Data')
        # self.dataMenu.addMenu(self.inputMenu)
        # self.dataMenu.addAction(self.closeInputAction)
        # self.dataMenu.addSeparator()
        # self.dataMenu.addMenu(self.outputMenu)
        # self.dataMenu.addAction(self.closeOutputAction)
        # self.viewMenu = self.menuBar_.addMenu('&View')
        # self.viewMenu.addAction(self.viewControlBarAction)
        # self.viewMenu.addAction(self.viewDisplayBarAction)
        # self.viewMenu.addSeparator()
        # for action in self.settingsManager.toggleViewActions():
        #     self.viewMenu.addAction(action)
        self.setMenuBar(self.menuBar_)

        # Load previous window size and position, but set a sensible
        # defaults if those settings aren't available.
        self.move(QtCore.QPoint(40,80))
        self.resize(QtCore.QSize(720,480))
        try:
            self.resize(self.settings.value('main_window/size',self.size()).toSize())
        except Exception:
            pass
        try:
            self.move(self.settings.value('main_window/position',self.pos()).toPoint())
        except Exception:
            pass

        # connect up display mode changes
        # self.connect(self,
        #              QtCore.SIGNAL('displayModeChanged(int)'),
        #              self.dispWidget.processDisplayModeChanged)
        # self.connect(self,
        #              QtCore.SIGNAL('displayModeChanged(int)'),
        #              self.settingsManager['Optics'].widget().processDisplayModeChanged)
        # self.connect(self.settingsManager['Optics'].widget(),
        #              QtCore.SIGNAL('displayModeChanged(int)'),
        #              self.processDisplayModeChanged)
        # self.connect(self.dispWidget,
        #              QtCore.SIGNAL('displayModeChanged(int)'),
        #              self.processDisplayModeChanged)

    def setStatus(self, streaming=None, recording=None, zoom=None, recordNum=None):
        """
        Handle the current status of the program
        """

        if None == zoom:
            zoom = self.zoom
        else:
            self.zoom = zoom
        if zoom >= 1.0:
            self.zoomStatus.setText('Zoom: %dX' % int(zoom))
        else:
            self.zoomStatus.setText('Zoom: 1/%dX' % int(1.0/zoom))

    def resource(self, filename):
        """
        Return the actual location of a resource file
        """
        return os.path.join(self.settings.getString('app/resource_path'),filename)
        
    # def changeZoom(self, newZoom):
    #     """
    #     When zoom level is changed
    #     """
    #     self.setStatus(zoom=newZoom)

    def closeEvent(self, event):
        """
        When main window is closed
        """
        #state = self.saveState()
        #self.settings.setValue('main_window/state', str(state.data()).encode('hex'))
        # save window settings
        self.settings.setValue('main_window/position', self.pos())
        self.settings.setValue('main_window/size', self.size())

        # close the window
        event.accept()

    def keyPressEvent(self, event):
        """
        Handle some shortcut keys
        """
        if event.key() == QtCore.Qt.Key_Plus:
            print 'plus'
        if event.key() == QtCore.Qt.Key_Plus and event.modifiers() == QtCore.Qt.ControlModifier:
            self.dispWidget.changeZoom(1.0)
        elif event.key() == QtCore.Qt.Key_Equal and event.modifiers() == QtCore.Qt.ControlModifier:
            self.dispWidget.changeZoom(1.0)
        elif event.key() == QtCore.Qt.Key_Minus and event.modifiers() == QtCore.Qt.ControlModifier:
            self.dispWidget.changeZoom(-1.0)
