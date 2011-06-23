"""
The Output Settings panel
"""
from PyQt4 import Qt, QtCore, QtGui, QtOpenGL
from PyQt4.QtCore import *
from settings import LuxSettings
import CalibrationPanel

class CalibrationSettings(QtGui.QWidget, CalibrationPanel.Ui_calibrationPanel):
    """
    A window that has the various calibration functions
    """

    def __init__(self, parent, output_engine):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.output_engine = output_engine
        
        self.settings = LuxSettings()
        self.resetDefaults()
        self.update()

    def resetDefaults(self):

        # Preamp Calibration
	self.preampCalibration.setChecked(False)
	self.laserCalibration.setChecked(False)
	self.preampCalibrationGain.setValue(self.settings['calibration'].valueWithDefault('preampCalibrationGain', 1.0) * 100)
	self.preampCalibrationGain.setValue(self.settings['calibration'].valueWithDefault('preampCalibrationOffset', 0.0) * 100)
	self.preampCalibrationFrequency.setValue(self.settings['calibration'].valueWithDefault('preampCalibrationFrequency', 10000.0) * 100.0 / 30000.0)

    # --------------------------------------------------------------------
    #                               ACTIONS 
    # --------------------------------------------------------------------

    def on_preampCalibration_toggled(self, state):
        self.settings['calibration'].preampCalibration = state
        if (state and self.settings['calibration'].laserCalibration):
            self.laserCalibration.setChecked(False)
        self.output_engine.setPreampCalibration(state)
    
    def on_preampCalibrationGain_valueChanged(self, value):
        self.settings['calibration'].preampCalibrationGain = value / 100.0
        self.output_engine.setPreampCalibrationGain(value / 100.0)

    def on_preampCalibrationOffset_valueChanged(self, value):
        self.settings['calibration'].preampCalibrationOffset = value / 100.0;
        self.output_engine.setPreampCalibrationOffset(value / 100.0)

    def on_preampCalibrationFrequency_valueChanged(self, value):
        self.settings['calibration'].preampCalibrationFrequency = value / 100.0 * 30000.0
        self.output_engine.setPreampCalibrationFrequency(value / 100.0 * 30000.0)


    def on_laserCalibration_toggled(self, state):
        self.settings['calibration'].laserCalibration = state
        if (state and self.settings['calibration'].preampCalibration):
            self.preampCalibration.setChecked(False)
        self.output_engine.setLaserCalibration(state)

    def on_laserCalibrationRedIntensity_valueChanged(self, value):
        self.settings['calibration'].laserCalibrationRedIntensity = value / 100.0
        self.output_engine.setLaserCalibrationRedIntensity(value / 100.0)
        self.laserCalibrationRedLabel.setText('%0.2f' % (value / 100.0))

    def on_laserCalibrationGreenIntensity_valueChanged(self, value):
        self.settings['calibration'].laserCalibrationGreenIntensity = value / 100.0
        self.output_engine.setLaserCalibrationGreenIntensity(value / 100.0)
        self.laserCalibrationGreenLabel.setText('%0.2f' % (value / 100.0))

    def on_laserCalibrationBlueIntensity_valueChanged(self, value):
        self.settings['calibration'].laserCalibrationBlueIntensity = value / 100.0
        self.output_engine.setLaserCalibrationBlueIntensity(value / 100.0)
        self.laserCalibrationBlueLabel.setText('%0.2f' % (value / 100.0))

    def on_laserCalibrationXFreq_valueChanged(self, value):
        self.settings['calibration'].laserCalibrationXFrequency = value / 100.0 * 30000.0
        self.output_engine.setLaserCalibrationXFrequency(value / 100.0 * 30000.0)
        self.laserCalibrationXFreqLabel.setText('%0.2f' % (value / 100.0 * 30000))

    def on_laserCalibrationYFreq_valueChanged(self, value):
        self.settings['calibration'].laserCalibrationYFrequency = value / 100.0 * 30000.0
        self.output_engine.setLaserCalibrationYFrequency(value / 100.0 * 30000.0)
        self.laserCalibrationYFreqLabel.setText('%0.2f' % (value / 100.0 * 30000))

