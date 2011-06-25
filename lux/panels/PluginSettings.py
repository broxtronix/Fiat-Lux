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
        self.video_engine = lux_engine.video_engine

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
        self.randomModeButton.setChecked(self.settings['plugins'].refreshWithDefault('random_mode', False));
        self.manualModeButton.setChecked(self.settings['plugins'].refreshWithDefault('manual_mode', True));

        self.videoMode.setChecked(self.settings['video'].refreshWithDefault('videoMode', False));
        self.thresholdSlider.setValue(self.settings['video'].refreshWithDefault('threshold', 0.2 * 99.0));
        self.blurSlider.setValue(self.settings['video'].refreshWithDefault('blur', 1.5 / 5.0 * 99.0));
        self.minAreaSlider.setValue(self.settings['video'].refreshWithDefault('minArea', 100 / (640*480) * 99.0));
        self.maxAreaSlider.setValue(self.settings['video'].refreshWithDefault('maxArea', 99.0));
        self.maxNumSlider.setValue(self.settings['video'].refreshWithDefault('maxNum', 10));

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

    def on_videoMode_toggled(self, state):
        self.settings['video'].videoMode = state

    def on_thresholdSlider_valueChanged(self, value):
        self.settings['video'].threshold = value / 99.0;
        self.video_engine.setContourThreshold(value / 99.0)
        self.thresholdLabel.setText('%0.2f' % (value / 99.0))

    def on_blurSlider_valueChanged(self, value):
        v = value / 99.0 * 5.0;
        self.settings['video'].blur = v;
        self.video_engine.setContourBlurSigma(v);
        self.blurLabel.setText('%0.2f' % (v))

    def on_minAreaSlider_valueChanged(self, value):
        v = value / 99.0 * 640*480;
        self.settings['video'].minArea = v;
        self.video_engine.setContourMinArea(v);
        self.minAreaLabel.setText('%0.2f' % (v))

    def on_maxAreaSlider_valueChanged(self, value):
        v = value / 99.0 * 640*480;
        self.settings['video'].maxArea = v;
        self.video_engine.setContourMaxArea(v);
        self.maxAreaLabel.setText('%0.2f' % (v))

    def on_maxNumSlider_valueChanged(self, value):
        self.settings['video'].maxNum = value;
#        self.video_engine.setContourNumConsidered(value);
        self.maxNumLabel.setText('%d' % value)

    def on_modeSelection_currentIndexChanged(self, index):
        # Ignore signals with string arguments
        if (type(index) is not int):
            return

#        self.video_engine.setContourMode(index)
        self.settings['video'].contourMode = index

    def on_methodSelection_currentIndexChanged(self, index):
        # Ignore signals with string arguments
        if (type(index) is not int):
            return

#        self.video_engine.setContourMethod(index)
        self.settings['video'].contourMethod = index

