"""
The Plugin Settings panel
"""
from PyQt4 import Qt, QtCore, QtGui, QtOpenGL
from PyQt4.QtCore import *
from settings import LuxSettings
import PluginPanel
import random
        
class PluginSettings(QtGui.QWidget, PluginPanel.Ui_pluginPanel):
    """
    A window that has the various display-specific settings
    """

    def __init__(self, parent, lux_engine):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        
        self.settings = LuxSettings()
        self.lux_engine = lux_engine

        (self.plugin_keys, self.plugin_names, self.plugin_descriptions) = self.lux_engine.list_plugins()


        # Populate the pull-down menu and select the previous plugin
        # we were using, if it is available.
        prev_plugin = None
        if self.settings['plugins'].contains('current_plugin'):
            prev_plugin = self.settings['plugins'].current_plugin

        self.current_plugin_idx = -1
        for name in self.plugin_names:
            self.manualSelectionBox.addItem(name)
            
        idx = self.manualSelectionBox.findText(prev_plugin)
        if idx != -1:
            self.manualSelectionBox.setCurrentIndex(idx)

        # start up an update timer with an interval of 1000ms.  We
        # will use this to check whether it is time for a new random
        # plugin.
        self.timerId = self.startTimer(1000)

        # Read previous state from the settings file
        self.randomModeButton.setChecked(self.settings['plugins'].valueWithDefault('random_mode', False));
        self.manualModeButton.setChecked(self.settings['plugins'].valueWithDefault('manual_mode', True));

        self.connect(self.prevButton, QtCore.SIGNAL('clicked()'), self.prevClicked)
        self.connect(self.nextButton, QtCore.SIGNAL('clicked()'), self.nextClicked)
        self.connect(self.randomButton, QtCore.SIGNAL('clicked()'), self.randomClicked)
        
        self.update()
        
    # --------------------------------------------------------------------
    #                          EVENT HANDLING
    # --------------------------------------------------------------------

    # If the user has selected random mode, mix things up! 
    def timerEvent(self, event):
        if self.randomModeButton.isChecked() and (random.random() < 0.1):
            self.randomClicked()

    # --------------------------------------------------------------------
    #                               ACTIONS 
    # --------------------------------------------------------------------

    def on_randomModeButton_toggled(self, state):
        self.settings['plugins'].random_mode = state
        self.manualModeButton.setChecked(not state)
        self.manualSelectionBox.setEnabled(False)

    def on_manualModeButton_toggled(self, state):
        self.settings['plugins'].manual_mode = state
        self.randomModeButton.setChecked(not state)
        self.manualSelectionBox.setEnabled(True)
    
    def prevClicked(self):
        new_idx = self.current_plugin_idx - 1
        if new_idx < 0:
            new_idx = len(self.plugin_keys) - 1
        self.manualSelectionBox.setCurrentIndex(new_idx)

    def nextClicked(self):
        new_idx = self.current_plugin_idx + 1
        if new_idx >= len(self.plugin_keys):
            new_idx = 0
        self.manualSelectionBox.setCurrentIndex(new_idx)

    def randomClicked(self):
        new_idx = random.randint(0, len(self.plugin_keys)-1)
        self.manualSelectionBox.setCurrentIndex(new_idx)

    def on_manualSelectionBox_currentIndexChanged(self, index):
        # Ignore signals with string arguments
        if (type(index) is not int):
            return
        # Ignore if this is just the same argument
        if (index == self.current_plugin_idx):
            return

        self.current_plugin_idx = index
        self.lux_engine.select_plugin(self.plugin_keys[self.current_plugin_idx])
        self.descriptionLabel.setText(self.plugin_descriptions[self.current_plugin_idx])
        self.settings['plugins'].current_plugin = self.plugin_names[self.current_plugin_idx]
        print 'saved state', self.settings['plugins'].current_plugin
