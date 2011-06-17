"""
The Output Settings panel
"""
from PyQt4 import Qt, QtCore, QtGui, QtOpenGL
from PyQt4.QtCore import *
from settings import LuxSettings
import OutputPanel

class ControlPoint(QtGui.QGraphicsEllipseItem):
    def __init__(self, parent = None):
        QtGui.QGraphicsEllipseItem.__init__(self, parent)
        self.form = None

    def itemChange(self, change, value):
        if (change == QtGui.QGraphicsItem.ItemPositionChange and self.form):
            self.form.pointMoved(self)
	return QtGui.QGraphicsEllipseItem.itemChange(self, change, value)

        
class OutputSettings(QtGui.QWidget, OutputPanel.Ui_outputPanel):
    """
    A window that has the various display-specific settings
    """

    ASPECT_1_1 = 0
    ASPECT_4_3 = 1
    ASPECT_16_9 = 2

    def __init__(self, displayWindow, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        
        self.settings = LuxSettings()

        grid_pen = QtGui.QPen(Qt.blue)
	line_pen = QtGui.QPen(Qt.green);
	point_brush = QtGui.QBrush(Qt.red);
	background_brush = QtGui.QBrush(Qt.black);
	
        self.scene = QtGui.QGraphicsScene()
        self.scene.setSceneRect(-1.1,-1.1,2.2,2.2);

        for i in range(-5,6):
            self.scene.addLine(i/5.0, -1.0, i/5.0, 1.0, grid_pen);
            self.scene.addLine(-1.0, i/5.0, 1.0, i/5.0, grid_pen);
	
        self.pts = []
        for i in range(4):
            self.pts.append(ControlPoint())

        for i in range(4):
            self.pts[i].setBrush(point_brush);
            self.pts[i].setRect(-5, -5, 10, 10);
            self.pts[i].setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations, True);
            self.pts[i].setFlag(QtGui.QGraphicsItem.ItemIsMovable, True);
            self.pts[i].setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True);
            self.pts[i].form = self;
            self.scene.addItem(self.pts[i]);
	
        self.pl = QtGui.QGraphicsPolygonItem()
        self.pl.setPen(line_pen);
	self.scene.addItem(self.pl);

	self.calibrationView.setBackgroundBrush(background_brush);
        self.calibrationView.setScene(self.scene)
        self.calibrationView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio);
	self.calibrationView.setRenderHints(QtGui.QPainter.Antialiasing);
        self.affine_matrix = QtGui.QTransform()

        self.currentAspect = -1

        self.resetPoints()
        self.resetDefaults()
        self.update()

    def resetDefaults(self):
        # Laser Power
	self.redIntensitySlider.setValue(self.settings['output'].valueWithDefault('redIntensity', 1.0) * 100);
	self.redOffsetSlider.setValue(self.settings['output'].valueWithDefault('redOffset', 0.0) * 100 + 50);
	self.greenIntensitySlider.setValue(self.settings['output'].valueWithDefault('greenIntensity', 1.0) * 100);
	self.greenOffsetSlider.setValue(self.settings['output'].valueWithDefault('greenOffset', 0.0) * 100 + 50);
	self.blueIntensitySlider.setValue(self.settings['output'].valueWithDefault('blueIntensity', 1.0) * 100);
	self.blueOffsetSlider.setValue(self.settings['output'].valueWithDefault('blueOffset', 0.0) * 100 + 50);

	# Blanking
	self.outputEnable.setChecked(self.settings['output'].valueWithDefault('outputEnable', True));
	self.blankingDisable.setChecked(self.settings['output'].valueWithDefault('blankingDisable', False));
	self.blankingInvert.setChecked(self.settings['output'].valueWithDefault('blankingInvert', False));

        # Scanning
	self.xInvert.setChecked(self.settings['output'].valueWithDefault('xInvert', False))
	self.yInvert.setChecked(self.settings['output'].valueWithDefault('yInvert', False))
	self.xySwap.setChecked(self.settings['output'].valueWithDefault('xySwap', False))
	self.aspectScale.setChecked(self.settings['output'].valueWithDefault('aspectScale', False))
        self.fitSquare.setChecked(self.settings['output'].valueWithDefault('fitSquare', False))
	self.aspectRatio.setCurrentIndex(self.settings['output'].valueWithDefault('aspectRatio',0))
        
        # Set up safe environment every time
        self.settings['output'].xEnable = True
        self.settings['output'].yEnable = True
        self.settings['output'].enforceSafety = True
	self.enforceSafety.setChecked(True);
        self.xEnable.setChecked(True)
	self.yEnable.setChecked(True)
        self.xEnable.setEnabled(False)
	self.yEnable.setEnabled(False)

        # Calibration
        self.lockCalibration.setChecked(self.settings['output'].valueWithDefault('lockCalibration', False))

        # Extract the affine matrix
        if self.settings['output'].contains('affine_matrix'):
            self.affine_matrix = self.settings['output'].affine_matrix
        else: 
            self.affine_matrix.reset()
        self.loadPoints();
	self.updateMatrix();

        # Set the state of the momentaryTestButton
        self.momentaryTestButton.setEnabled(not self.outputEnable.isChecked())

    def resetPoints(self):
	self.affine_matrix.reset()
	self.affine_matrix.scale(1.0, self.getYRatio(self.aspectRatio.currentIndex()))
	self.updateMatrix();
	self.loadPoints();

    def loadPoints(self):
        p0 = QtCore.QPointF(-1,-1);
	p1 = QtCore.QPointF(1,-1);
	p2 = QtCore.QPointF(-1,1);
	p3 = QtCore.QPointF(1,1);

        for i in range(4):
            self.pts[i].setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, False);

        self.pts[0].setPos(self.affine_matrix.map(p0));
	self.pts[1].setPos(self.affine_matrix.map(p1));
	self.pts[2].setPos(self.affine_matrix.map(p2));
	self.pts[3].setPos(self.affine_matrix.map(p3));

        for i in range(4):
            self.pts[i].setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True);
	self.updatePoly();

    def pointMoved(self, point):
	src = QtGui.QPolygonF()
        src.append(QtCore.QPointF(-1,-1))
        src.append(QtCore.QPointF( 1,-1))
        src.append(QtCore.QPointF( 1, 1))
        src.append(QtCore.QPointF(-1, 1))

	dst = QtGui.QPolygonF()
        dst.append(self.pts[0].pos())
        dst.append(self.pts[1].pos())
        dst.append(self.pts[3].pos())
        dst.append(self.pts[2].pos())

	QtGui.QTransform.quadToQuad(src, dst, self.affine_matrix);
	self.loadPoints();
	self.updateMatrix();

        # Save the data into our settings structure
        self.settings['output'].affine_matrix = self.affine_matrix

    def updateMatrix(self):
	smtx = QtGui.QTransform()
	omtx = QtGui.QTransform()
	yratio = self.getYRatio(self.aspectRatio.currentIndex())
	
        if not self.aspectScale.isChecked():
            if self.fitSquare.isChecked():
                smtx.scale(yratio, 1.0)
            else:
                smtx.scale(1.0, 1.0/yratio)

	omtx = smtx * self.affine_matrix
        
        # TODO:Update config here

    def updatePoly(self):
        poly = QtGui.QPolygonF()
        poly.append(self.pts[0].pos())
        poly.append(self.pts[1].pos())
        poly.append(self.pts[3].pos())
        poly.append(self.pts[2].pos())
	self.pl.setPolygon(poly);

    def getYRatio(self, ratio):
        if (ratio == OutputSettings.ASPECT_1_1):
            return 1.0;
        elif (ratio == OutputSettings.ASPECT_4_3):
            return 3.0/4.0;
        elif (ratio == OutputSettings.ASPECT_16_9):
            return 9.0/16.0;
        else:
            return 1.0

    # --------------------------------------------------------------------
    #                            EVENT HANDLING    
    # --------------------------------------------------------------------

    def resizeEvent(self, event):
        self.calibrationView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio);

    def showEvent(self, event):
        self.calibrationView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio);

    # --------------------------------------------------------------------
    #                               ACTIONS 
    # --------------------------------------------------------------------

    def on_enforceSafety_toggled(self, state):
        if not state:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Do not stare into laser with remaining eye")
            msgBox.setInformativeText("Do you really want to disable safety enforcement?")
            msgBox.addButton(QtGui.QMessageBox.Yes)
            msgBox.addButton(QtGui.QMessageBox.No)
            msgBox.setDefaultButton(QtGui.QMessageBox.No)
            ret = msgBox.exec_()
            if ret == QtGui.QMessageBox.Yes:
                self.xEnable.setEnabled(True)
                self.yEnable.setEnabled(True)
                return
            else:
                self.enforceSafety.setChecked(True)
                self.xEnable.setEnabled(False)
                self.yEnable.setEnabled(False)
                return
	
	if state:
            self.xEnable.setChecked(True)
            self.yEnable.setChecked(True)
            self.xEnable.setEnabled(False)
            self.yEnable.setEnabled(False)
	
    def on_outputEnable_toggled(self, state):
        self.settings['output'].outputEnable = state
        self.momentaryTestButton.setEnabled(not state)


    def on_blankingDisable_toggled(self, state):
        self.settings['output'].blankingDisable = state

    def on_blankingInvert_toggled(self, state):
        self.settings['output'].blankingInvert = state

    def on_stopButton_pressed(self):
        self.outputEnable.setChecked(False)

    def on_momentaryTestButton_pressed(self):
        self.settings['output'].outputEnable = True

    def on_momentaryTestButton_released(self):
        self.settings['output'].outputEnable = False

    def on_xEnable_toggled(self, state):
        self.settings['output'].xEnable = state

    def on_yEnable_toggled(self, state):
        self.settings['output'].yEnable = state

    def on_xInvert_toggled(self, state):
        self.settings['output'].xInvert = state

    def on_yInvert_toggled(self, state):
        self.settings['output'].yInvert = state

    def on_xySwap_toggled(self, state):
        self.settings['output'].xySwap = state

    def on_aspectScale_toggled(self, state):
        self.fitSquare.setEnabled(not state)
        self.updateMatrix();

    def on_fitSquare_toggled(self, state):
        self.updateMatrix();

    def on_aspectRatio_currentIndexChanged(self, index):

        # Ignore signals with string arguments
        if (type(index) is not int):
            return

        # Ignore if this is just the same argument
        if (index == self.currentAspect):
            return

        rold = self.getYRatio(self.currentAspect)
        rnew = self.getYRatio(index)
	
        smtx = QtGui.QTransform()
        smtx.scale(1.0, rnew/rold)
 	self.affine_matrix = smtx * self.affine_matrix
	
        self.currentAspect = index
        self.resetPoints();

        # Save the data into our settings structure
        self.settings['output'].aspectRatio = self.currentAspect
        self.settings['output'].affine_matrix = self.affine_matrix

    def on_resetTransform_clicked(self):
        self.resetPoints();

        # Save the data into our settings structure
        self.settings['output'].affine_matrix = self.affine_matrix

    def on_redIntensitySlider_valueChanged(self, value):
        self.settings['output'].redIntensity = value / 100.0;

    def on_redOffsetSlider_valueChanged(self, value):
        self.settings['output'].redOffset = (value-50.0) / 100.0;

    def on_greenIntensitySlider_valueChanged(self, value):
        self.settings['output'].greenIntensity = value / 100.0;

    def on_greenOffsetSlider_valueChanged(self, value):
        self.settings['output'].greenOffset = (value-50.0) / 100.0;

    def on_blueIntensitySlider_valueChanged(self, value):
        self.settings['output'].blueIntensity = value / 100.0;

    def on_blueOffsetSlider_valueChanged(self, value):
        self.settings['output'].blueOffset = (value-50.0) / 100.0;

    def on_lockCalibration_toggled(self, state):
        self.settings['output'].lockCalibration = state
        self.calibrationView.setInteractive(not state);
        self.resetTransform.setEnabled(not state)
        self.aspectRatio.setEnabled(not state)
