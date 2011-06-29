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
        self.update()
        self.resetDefaults()

    def resetDefaults(self):

        # Check boxes are a little tricky, and it is safest to
        # explicitly set the state of the output engine here.
        self.settings['calibration'].parameterOverride = False
        self.settings['calibration'].preampCalibration = False
        self.settings['calibration'].laserCalibration = False
	self.parameterOverride.setChecked(False)
	self.preampCalibration.setChecked(False)
        self.output_engine.setPreampCalibration(False)
	self.laserCalibration.setChecked(False)
        self.output_engine.setLaserCalibration(False)

        # The rest of the defaults are handled normally through the
        # slots below.

        # OPENLASE PARAMETERS
        self.olRateSlider.setValue(self.settings['calibration'].refreshWithDefault('olRate', 30000)/1000.0)
        self.olOnSpeedSlider.setValue(self.settings['calibration'].refreshWithDefault('olOnSpeed', 100))
        self.olOffSpeedSlider.setValue(self.settings['calibration'].refreshWithDefault('olOffSpeed', 20))
        self.olStartDwellSlider.setValue(self.settings['calibration'].refreshWithDefault('olStartDwell', 3))
        self.olEndDwellSlider.setValue(self.settings['calibration'].refreshWithDefault('olEndDwell', 3))
        self.olCornerDwellSlider.setValue(self.settings['calibration'].refreshWithDefault('olCornerDwell', 4))
        self.olCurveDwellSlider.setValue(self.settings['calibration'].refreshWithDefault('olCurveDwell', 0))
        self.olStartWaitSlider.setValue(self.settings['calibration'].refreshWithDefault('olStartWait', 8))
        self.olEndWaitSlider.setValue(self.settings['calibration'].refreshWithDefault('olEndWait', 7))

        # PREAMP CALIBRATION
	self.preampCalibrationGain.setValue(self.settings['calibration'].refreshWithDefault('preampCalibrationGain', 1.0 * 100))
	self.preampCalibrationOffset.setValue(self.settings['calibration'].refreshWithDefault('preampCalibrationOffset', 0.0 * 100))
	self.preampCalibrationFrequency.setValue(self.settings['calibration'].refreshWithDefault('preampCalibrationFrequency', 10000.0 * 99.0 / 30000.0))

        # LASER CALIBRATION
        self.laserCalibrationRedIntensity.setValue(self.settings['calibration'].refreshWithDefault('laserCalibrationRedIntensity', 0.0))
        self.laserCalibrationGreenIntensity.setValue(self.settings['calibration'].refreshWithDefault('laserCalibrationGreenIntensity', 0.0))
        self.laserCalibrationBlueIntensity.setValue(self.settings['calibration'].refreshWithDefault('laserCalibrationBlueIntensity', 0.0))
        self.laserCalibrationXFreq.setValue(self.settings['calibration'].refreshWithDefault('laserCalibrationXFrequency', 0.0))
        self.laserCalibrationYFreq.setValue(self.settings['calibration'].refreshWithDefault('laserCalibrationYFrequency', 0.0))

    # --------------------------------------------------------------------
    #                               ACTIONS 
    # --------------------------------------------------------------------

    # OPENLASE PARAMS

    def on_parameterOverride_toggled(self, state):
        self.settings['calibration'].parameterOverride = state
        self.emit(QtCore.SIGNAL('olParamsChanged()'))

    def on_olRateSlider_valueChanged(self, value):
        v = float(value) * 1000.0
        self.settings['calibration'].olRate = v
        self.olRateLabel.setText('%0.0f' % v)
        self.emit(QtCore.SIGNAL('olParamsChanged()'))

    def on_olOnSpeedSlider_valueChanged(self, value):
        self.settings['calibration'].olOnSpeed = value
        self.olOnSpeedLabel.setText('%d' % value)
        self.emit(QtCore.SIGNAL('olParamsChanged()'))

    def on_olOffSpeedSlider_valueChanged(self, value):
        self.settings['calibration'].olOffSpeed = value
        self.olOffSpeedLabel.setText('%d' % value)
        self.emit(QtCore.SIGNAL('olParamsChanged()'))

    def on_olStartDwellSlider_valueChanged(self, value):
        self.settings['calibration'].olStartDwell = value
        self.olStartDwellLabel.setText('%d' % value)
        self.emit(QtCore.SIGNAL('olParamsChanged()'))

    def on_olEndDwellSlider_valueChanged(self, value):
        self.settings['calibration'].olEndDwell = value
        self.olEndDwellLabel.setText('%d' % value)
        self.emit(QtCore.SIGNAL('olParamsChanged()'))

    def on_olCornerDwellSlider_valueChanged(self, value):
        self.settings['calibration'].olCornerDwell = value
        self.olCornerDwellLabel.setText('%d' % value)
        self.emit(QtCore.SIGNAL('olParamsChanged()'))

    def on_olCurveDwellSlider_valueChanged(self, value):
        self.settings['calibration'].olCurveDwell = value
        self.olCurveDwellLabel.setText('%d' % value)
        self.emit(QtCore.SIGNAL('olParamsChanged()'))

    def on_olStartWaitSlider_valueChanged(self, value):
        self.settings['calibration'].olStartWait = value
        self.olStartWaitLabel.setText('%d' % value)
        self.emit(QtCore.SIGNAL('olParamsChanged()'))

    def on_olEndWaitSlider_valueChanged(self, value):
        self.settings['calibration'].olEndWait = value
        self.olEndWaitLabel.setText('%d' % value)
        self.emit(QtCore.SIGNAL('olParamsChanged()'))

    # PREAMP CALIBRATION

    def on_preampCalibration_toggled(self, state):
        self.settings['calibration'].preampCalibration = state
        if (state and self.settings['calibration'].laserCalibration):
            self.laserCalibration.setChecked(False)
        self.output_engine.setPreampCalibration(state)
    
    def on_preampCalibrationGain_valueChanged(self, value):
        self.settings['calibration'].preampCalibrationGain = value
        self.output_engine.setPreampCalibrationGain(value / 99.0)

    def on_preampCalibrationOffset_valueChanged(self, value):
        self.settings['calibration'].preampCalibrationOffset = value
        self.output_engine.setPreampCalibrationOffset(value / 99.0)

    def on_preampCalibrationFrequency_valueChanged(self, value):
        self.settings['calibration'].preampCalibrationFrequency = value
        self.output_engine.setPreampCalibrationFrequency(value / 99.0 * 30000.0)

    # LASER CALIBRATION

    def on_laserCalibration_toggled(self, state):
        self.settings['calibration'].laserCalibration = state
        if (state and self.settings['calibration'].preampCalibration):
            self.preampCalibration.setChecked(False)
        self.output_engine.setLaserCalibration(state)

    def on_laserCalibrationRedIntensity_valueChanged(self, value):
        v = value / 99.0
        self.settings['calibration'].laserCalibrationRedIntensity = value
        self.output_engine.setLaserCalibrationRedIntensity(v)
        self.laserCalibrationRedLabel.setText('%0.2f' % v)

    def on_laserCalibrationGreenIntensity_valueChanged(self, value):
        v = value / 99.0
        self.settings['calibration'].laserCalibrationGreenIntensity = value
        self.output_engine.setLaserCalibrationGreenIntensity(v)
        self.laserCalibrationGreenLabel.setText('%0.2f' % v)

    def on_laserCalibrationBlueIntensity_valueChanged(self, value):
        v = value / 99.0
        self.settings['calibration'].laserCalibrationBlueIntensity = value
        self.output_engine.setLaserCalibrationBlueIntensity(v)
        self.laserCalibrationBlueLabel.setText('%0.2f' % v)

    def on_laserCalibrationXFreq_valueChanged(self, value):
        v = value / 99.0 * 30000.0
        self.settings['calibration'].laserCalibrationXFrequency = value
        self.output_engine.setLaserCalibrationXFrequency(v)
        self.laserCalibrationXFreqLabel.setText('%0.2f' % v)

    def on_laserCalibrationYFreq_valueChanged(self, value):
        v = value / 99.0 * 30000.0
        self.settings['calibration'].laserCalibrationYFrequency = value
        self.output_engine.setLaserCalibrationYFrequency(v)
        self.laserCalibrationYFreqLabel.setText('%0.2f' % v)

