"""
Main window for Fiat Lux
"""

from PyQt4 import QtCore, QtGui
from settings import LuxSettings
import sys
import os.path
from simulation_display import SimulationDisplay
    
from panels import OutputSettings
from panels import CalibrationSettings
from panels import PluginSettings
#from console import IPythonConsole

# MacOS X supports video capture using syphon.  Other platforms don't (yet!)
if sys.platform == "darwin":
    from video_display import VideoDisplay

# ----------------------------------------------------------------------------------
#                           SETTINGS PANEL MANAGEMENT
# ----------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------
#                               MAIN WINDOW CLASS
# ----------------------------------------------------------------------------------
class MainWindow(QtGui.QMainWindow):
    def __init__(self, lux_engine, output_engine, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.settings = LuxSettings()
        self.lux_engine = lux_engine
        self.output_engine = output_engine
        
        # set our title
        self.setWindowIcon(QtGui.QIcon())
        self.setWindowTitle('Fiat Lux')

        # create the display widgets in a QTabView
        self.displayTabWidget = QtGui.QTabWidget(self)
        self.simWidget = SimulationDisplay(self)
        self.displayTabWidget.addTab(self.simWidget, "Laser Output")
        # MacOS X supports video capture using syphon.  Other platforms don't (yet!)
        if sys.platform == "darwin":
            self.videoWidget = VideoDisplay(lux_engine.video_engine, self)
            self.displayTabWidget.addTab(self.videoWidget, "Video Input")
        self.setCentralWidget(self.displayTabWidget)

        self.displayTabWidget.setCurrentIndex(self.settings['main_window'].valueWithDefault('display_tab', 0))
        self.connect(self.displayTabWidget, QtCore.SIGNAL('currentChanged(int)'), self.displayTabChanged)

        # This might be fun someday...
        #        self.ipythonWidget = IPythonConsole(self)
        #        self.setCentralWidget(self.ipythonWidget)
        

        # set up the status bar
        self.statusBar_ = QtGui.QStatusBar(self)
        self.statusLabel = QtGui.QLabel()
        self.statusLabel.setMargin(2)
        self.setStatus() # set a default status
        self.statusBar_.addWidget(self.statusLabel)
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
        # self.controlBar = QtGui.QToolBar(self)
        # self.controlBar.setObjectName('Control Bar')
        # self.controlBar.addAction(self.streamAction)
        # self.controlBar.addAction(self.pauseAction)
        # self.displayBar = QtGui.QToolBar(self)
        # self.displayBar.setObjectName('Display Mode Bar')
        # self.displayBar.addWidget(self.displayPrefix)
        # self.displayBar.addWidget(self.displayRawButton)
        # self.displayBar.addWidget(self.displayPinholeButton)
        # self.displayBar.addWidget(self.displayApertureButton)
        # self.addToolBar(self.controlBar)
        # self.addToolBar(self.displayBar)

        # toolbar view control
        # self.viewControlBarAction = self.controlBar.toggleViewAction()
        # self.viewControlBarAction.setText('&Controls')
        # self.viewDisplayBarAction = self.displayBar.toggleViewAction()
        # self.viewDisplayBarAction.setText('&Display mode')

        # set up the settings panels
        self.settingsManager = SettingsPanelManager(self)
        
        self.settingsManager.add(SettingsPanel(name = "Plugins",
                                               message = "",
                                               widget = PluginSettings.PluginSettings(self,
                                                                                      self.lux_engine)
                                               ))
        self.settingsManager.add(SettingsPanel(name = "Output",
                                               message = "",
                                               widget = OutputSettings.OutputSettings(self,
                                                                                      self.output_engine)
                                               ))
        self.settingsManager.add(SettingsPanel(name = "Calibration",
                                               message = "",
                                               widget = CalibrationSettings.CalibrationSettings(self,
                                                                                   self.output_engine)
                                               ))

        # set up the menu bar
        self.menuBar_ = QtGui.QMenuBar(self)
        self.viewMenu = self.menuBar_.addMenu('&View')
        for action in self.settingsManager.toggleViewActions():
            self.viewMenu.addAction(action)
        self.setMenuBar(self.menuBar_)

        # Load previous window size and position, but set a sensible
        # defaults if those settings aren't available.
        self.move(QtCore.QPoint(40,80))
        self.resize(QtCore.QSize(720,480))

        # load window settings
        self.resize(self.settings['main_window'].valueWithDefault('size', self.size()))
        self.move(self.settings['main_window'].valueWithDefault('position', self.pos()))

        # load the previous state of the docks and toolbars
        try:
            state = QtCore.QByteArray(self.settings['main_window'].state.decode('hex'))
            self.restoreState(state)
        except AttributeError:
            print "Warning: Could not restore window state."
            # ignore
            pass

    def displayTabChanged(self, index):
        self.settings['main_window'].display_tab = index

    def setStatus(self, streaming=None, recording=None, recordNum=None):
        """
        Handle the current status of the program
        """
        self.statusLabel.setText('')

    def resource(self, filename):
        """
        Return the actual location of a resource file
        """
        return os.path.join(self.settings['app'].resource_path, filename)
        
    def closeEvent(self, event):
        """
        When main window is closed
        """
        state = self.saveState()
        self.settings['main_window'].state = str(state.data()).encode('hex')
        # save window settings
        self.settings['main_window'].position = self.pos()
        self.settings['main_window'].size = self.size()
        self.settings.sync() # Make sure settings sync to disk
        # close the window
        QtGui.QMainWindow.closeEvent(self, event);

    def keyPressEvent(self, event):
        """
        Handle some shortcut keys
        """
        if event.key() == QtCore.Qt.Key_1:
            self.displayTabWidget.setCurrentIndex(0)
        if event.key() == QtCore.Qt.Key_2:
            self.displayTabWidget.setCurrentIndex(1)

