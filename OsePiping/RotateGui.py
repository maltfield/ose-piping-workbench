# -*- coding: utf-8 -*-
# Author: Ruslan Krenzler.
# Date: 18 December 2020
# Rotate pipe or fitting.
# Form implementation generated from reading ui file 'rotate.ui',
# rotate.ui is derived from rotAround.ui from Dodo-Workbench, author Oddtopus.
#
# Created: Fri Dec 18 08:54:23 2020
#      by: pyside2-uic  running on PySide2 5.11.2
#

from PySide import QtCore, QtGui
from PySide import QtGui as QtWidgets
import FreeCAD
import FreeCADGui as Gui
import OsePiping.Port as Port


class MainDialog(QtGui.QDialog):
    QSETTINGS_APPLICATION = "OSE piping workbench"

    def __init__(self, document):
        super(MainDialog, self).__init__()
        self.document = document
        self.initUi()
        self.part = Gui.Selection.getSelectionEx()[-1].Object
        self.labelPartName.setText(self.part.Name)
        self.showPorts(self.part)

    def initUi(self):
        self.result = -1
        self.setupUi(self)

        # Restore previous user input.
        # Ignore exceptions to start GUI even with broken settings.
        try:
            self.restoreInput()
        except Exception as e:
            print("Could not restore old user input!")
            print(e)
        try:
            self.restoreWindowGeometry()
        except Exception as e:
            print("Could not restore old window geometry")
            print(e)
#            pass # Do nothing
        self.show()

    def saveWindowGeometry(self):
        settings = QtCore.QSettings(MainDialog.QSETTINGS_APPLICATION, "Rotation")
        settings.setValue("Window/Geometry", self.saveGeometry())
        settings.sync()

    def restoreWindowGeometry(self):
        settings = QtCore.QSettings(MainDialog.QSETTINGS_APPLICATION, "Rotation")
        geometry = settings.value("Window/Geometry", None)
        if geometry is not None:
            self.restoreGeometry(geometry)

    def saveInput(self):
        """Store user input for the next run."""
        settings = QtCore.QSettings(
            MainDialog.QSETTINGS_APPLICATION, "Rotation")

        settings.setValue("radioPort1", self.radioPort1.isChecked())
        settings.setValue("radioPort2", self.radioPort2.isChecked())
        settings.setValue("radioPort3", self.radioPort3.isChecked())
        settings.setValue("radioPort4", self.radioPort4.isChecked())
        settings.setValue("radioPort5", self.radioPort5.isChecked())
        settings.setValue("radioPort6", self.radioPort6.isChecked())

        settings.setValue("radioX", self.radioX.isChecked())
        settings.setValue("radioY", self.radioY.isChecked())
        settings.setValue("radioZ", self.radioZ.isChecked())

        settings.setValue("editDegree", str(self.editDegree.text()))

        settings.sync()

    def restoreInput(self):
        settings = QtCore.QSettings(
            MainDialog.QSETTINGS_APPLICATION, "Rotation")

        self.radioPort1.setChecked(settings.value("radioPort1", False))
        self.radioPort2.setChecked(settings.value("radioPort2", False))
        self.radioPort3.setChecked(settings.value("radioPort3", False))
        self.radioPort4.setChecked(settings.value("radioPort4", False))
        self.radioPort5.setChecked(settings.value("radioPort5", False))
        self.radioPort6.setChecked(settings.value("radioPort6", False))

        self.radioX.setChecked(settings.value("radioX", False))
        self.radioY.setChecked(settings.value("radioY", False))
        self.radioZ.setChecked(settings.value("radioZ", False))

        s = settings.value("editDegree", "0")
        self.editDegree.setText(s)
        self.onEditDegreeChanged()

    def onApplyClicked(self):
        self.saveWindowGeometry()
        self.saveInput()

        angle = self.dialDegree.value()
        if self.radioX.isChecked():
            R = FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), angle)  # Rotation matrix
        elif self.radioY.isChecked():
            R = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), angle)
        elif self.radioZ.isChecked():
            R = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), angle)
        elif self.radioPort1.isChecked():
            R = FreeCAD.Rotation(self.part.Ports[0], angle)
        elif self.radioPort2.isChecked():
            R = FreeCAD.Rotation(self.part.Ports[1], angle)
        elif self.radioPort3.isChecked():
            R = FreeCAD.Rotation(self.part.Ports[2], angle)
        elif self.radioPort4.isChecked():
            R = FreeCAD.Rotation(self.part.Ports[3], angle)
        elif self.radioPort5.isChecked():
            R = FreeCAD.Rotation(self.part.Ports[4], angle)
        elif self.radioPort6.isChecked():
            R = FreeCAD.Rotation(self.part.Ports[5], angle)
        else:
            return  # Do nothing.
        self.part.Placement.Rotation = self.part.Placement.Rotation.multiply(R)

    def showPorts(self, part):
        if Port.supportsAdvancedPort(part):
            nports = len(part.Ports)
        else:
            nports = 0

        if nports >= 1:
            self.radioPort1.setEnabled(True)
        else:
            self.radioPort1.setEnabled(False)

        if nports >= 2:
            self.radioPort2.setEnabled(True)
        else:
            self.radioPort2.setEnabled(False)

        if nports >= 3:
            self.radioPort3.setEnabled(True)
        else:
            self.radioPort3.setEnabled(False)

        if nports >= 4:
            self.radioPort4.setEnabled(True)
        else:
            self.radioPort4.setEnabled(False)

        if nports >= 5:
            self.radioPort5.setEnabled(True)
        else:
            self.radioPort5.setEnabled(False)

        if nports >= 6:
            self.radioPort6.setEnabled(True)
        else:
            self.radioPort6.setEnabled(False)

    def onPortRadioSelected(self):
        pass

    def onAxisRadioSelected(self):
        pass

    def onDialDegreeChanged(self):
        self.editDegree.setText(str(self.dialDegree.value()))

    def onEditDegreeChanged(self):
        try:
            self.dialDegree.setValue(float(self.editDegree.text()))
        except ValueError as ex:
            FreeCAD.Console.PrintError(str(ex) + "\n")

    def onReverseClicked(self):
        v = 360 - self.dialDegree.value()
        self.dialDegree.setValue(v)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(382, 274)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(24, 0))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.labelPartName = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPartName.sizePolicy().hasHeightForWidth())
        self.labelPartName.setSizePolicy(sizePolicy)
        self.labelPartName.setMinimumSize(QtCore.QSize(24, 0))
        self.labelPartName.setFrameShape(QtWidgets.QFrame.Box)
        self.labelPartName.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.labelPartName.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPartName.setObjectName("labelPartName")
        self.gridLayout.addWidget(self.labelPartName, 0, 0, 1, 2)
        self.labelInstructions = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInstructions.sizePolicy().hasHeightForWidth())
        self.labelInstructions.setSizePolicy(sizePolicy)
        self.labelInstructions.setMinimumSize(QtCore.QSize(24, 0))
        self.labelInstructions.setText("")
        self.labelInstructions.setAlignment(QtCore.Qt.AlignCenter)
        self.labelInstructions.setObjectName("labelInstructions")
        self.gridLayout.addWidget(self.labelInstructions, 8, 0, 1, 2)
        self.buttonApply = QtWidgets.QPushButton(Dialog)
        self.buttonApply.setObjectName("buttonApply")
        self.gridLayout.addWidget(self.buttonApply, 9, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.buttonReverse = QtWidgets.QPushButton(Dialog)
        self.buttonReverse.setObjectName("buttonReverse")
        self.verticalLayout_2.addWidget(self.buttonReverse)
        self.dialDegree = QtWidgets.QDial(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dialDegree.sizePolicy().hasHeightForWidth())
        self.dialDegree.setSizePolicy(sizePolicy)
        self.dialDegree.setMinimumSize(QtCore.QSize(24, 0))
        self.dialDegree.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dialDegree.setMaximum(360)
        self.dialDegree.setPageStep(15)
        self.dialDegree.setProperty("value", 90)
        self.dialDegree.setOrientation(QtCore.Qt.Horizontal)
        self.dialDegree.setInvertedAppearance(False)
        self.dialDegree.setInvertedControls(False)
        self.dialDegree.setWrapping(True)
        self.dialDegree.setNotchTarget(15.0)
        self.dialDegree.setNotchesVisible(True)
        self.dialDegree.setObjectName("dialDegree")
        self.verticalLayout_2.addWidget(self.dialDegree)
        self.editDegree = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editDegree.sizePolicy().hasHeightForWidth())
        self.editDegree.setSizePolicy(sizePolicy)
        self.editDegree.setMinimumSize(QtCore.QSize(24, 0))
        self.editDegree.setAlignment(QtCore.Qt.AlignCenter)
        self.editDegree.setObjectName("editDegree")
        self.verticalLayout_2.addWidget(self.editDegree)
        self.gridLayout.addLayout(self.verticalLayout_2, 2, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBoxPorts = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxPorts.sizePolicy().hasHeightForWidth())
        self.groupBoxPorts.setSizePolicy(sizePolicy)
        self.groupBoxPorts.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBoxPorts.setObjectName("groupBoxPorts")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBoxPorts)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(4, -1, 4, -1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.radioPort1 = QtWidgets.QRadioButton(self.groupBoxPorts)
        self.radioPort1.setObjectName("radioPort1")
        self.buttonGroup = QtWidgets.QButtonGroup(Dialog)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radioPort1)
        self.gridLayout_3.addWidget(self.radioPort1, 0, 0, 1, 1)
        self.radioPort2 = QtWidgets.QRadioButton(self.groupBoxPorts)
        self.radioPort2.setObjectName("radioPort2")
        self.buttonGroup.addButton(self.radioPort2)
        self.gridLayout_3.addWidget(self.radioPort2, 0, 1, 1, 1)
        self.radioPort3 = QtWidgets.QRadioButton(self.groupBoxPorts)
        self.radioPort3.setObjectName("radioPort3")
        self.buttonGroup.addButton(self.radioPort3)
        self.gridLayout_3.addWidget(self.radioPort3, 0, 2, 1, 1)
        self.radioPort4 = QtWidgets.QRadioButton(self.groupBoxPorts)
        self.radioPort4.setObjectName("radioPort4")
        self.buttonGroup.addButton(self.radioPort4)
        self.gridLayout_3.addWidget(self.radioPort4, 1, 0, 1, 1)
        self.radioPort5 = QtWidgets.QRadioButton(self.groupBoxPorts)
        self.radioPort5.setObjectName("radioPort5")
        self.buttonGroup.addButton(self.radioPort5)
        self.gridLayout_3.addWidget(self.radioPort5, 1, 1, 1, 1)
        self.radioPort6 = QtWidgets.QRadioButton(self.groupBoxPorts)
        self.radioPort6.setObjectName("radioPort6")
        self.buttonGroup.addButton(self.radioPort6)
        self.gridLayout_3.addWidget(self.radioPort6, 1, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.verticalLayout.addWidget(self.groupBoxPorts)
        self.groupBoxAxis = QtWidgets.QGroupBox(Dialog)
        self.groupBoxAxis.setObjectName("groupBoxAxis")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBoxAxis)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.radioZ = QtWidgets.QRadioButton(self.groupBoxAxis)
        self.radioZ.setObjectName("radioZ")
        self.buttonGroup.addButton(self.radioZ)
        self.gridLayout_4.addWidget(self.radioZ, 0, 2, 1, 1)
        self.radioX = QtWidgets.QRadioButton(self.groupBoxAxis)
        self.radioX.setChecked(True)
        self.radioX.setObjectName("radioX")
        self.buttonGroup.addButton(self.radioX)
        self.gridLayout_4.addWidget(self.radioX, 0, 0, 1, 1)
        self.radioY = QtWidgets.QRadioButton(self.groupBoxAxis)
        self.radioY.setObjectName("radioY")
        self.buttonGroup.addButton(self.radioY)
        self.gridLayout_4.addWidget(self.radioY, 0, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_4)
        self.verticalLayout.addWidget(self.groupBoxAxis)
        self.gridLayout.addLayout(self.verticalLayout, 2, 1, 2, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonApply, QtCore.SIGNAL("clicked()"), Dialog.onApplyClicked)
        QtCore.QObject.connect(self.radioX, QtCore.SIGNAL("clicked()"), Dialog.onAxisRadioSelected)
        QtCore.QObject.connect(self.radioY, QtCore.SIGNAL("clicked()"), Dialog.onAxisRadioSelected)
        QtCore.QObject.connect(self.radioZ, QtCore.SIGNAL("clicked()"), Dialog.onAxisRadioSelected)
        QtCore.QObject.connect(self.radioPort1, QtCore.SIGNAL("clicked()"), Dialog.onPortRadioSelected)
        QtCore.QObject.connect(self.radioPort2, QtCore.SIGNAL("clicked()"), Dialog.onPortRadioSelected)
        QtCore.QObject.connect(self.radioPort3, QtCore.SIGNAL("clicked()"), Dialog.onPortRadioSelected)
        QtCore.QObject.connect(self.radioPort4, QtCore.SIGNAL("clicked()"), Dialog.onPortRadioSelected)
        QtCore.QObject.connect(self.radioPort5, QtCore.SIGNAL("clicked()"), Dialog.onPortRadioSelected)
        QtCore.QObject.connect(self.radioPort6, QtCore.SIGNAL("clicked()"), Dialog.onPortRadioSelected)
        QtCore.QObject.connect(self.radioX, QtCore.SIGNAL("clicked(bool)"), Dialog.onAxisRadioSelected)
        QtCore.QObject.connect(self.buttonReverse, QtCore.SIGNAL("clicked()"), Dialog.onReverseClicked)
        QtCore.QObject.connect(self.dialDegree, QtCore.SIGNAL("valueChanged(int)"), Dialog.onDialDegreeChanged)
        QtCore.QObject.connect(self.editDegree, QtCore.SIGNAL("editingFinished()"), Dialog.onEditDegreeChanged)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Rotate around axis", None, -1))
        self.labelPartName.setText(QtWidgets.QApplication.translate("Dialog", "Part Name", None, -1))
        self.buttonApply.setText(QtWidgets.QApplication.translate("Dialog", "Apply", None, -1))
        self.buttonReverse.setText(QtWidgets.QApplication.translate("Dialog", "Reverse", None, -1))
        self.editDegree.setText(QtWidgets.QApplication.translate("Dialog", "90", None, -1))
        self.groupBoxPorts.setTitle(QtWidgets.QApplication.translate("Dialog", "Port:", None, -1))
        self.radioPort1.setText(QtWidgets.QApplication.translate("Dialog", "1", None, -1))
        self.radioPort2.setText(QtWidgets.QApplication.translate("Dialog", "2", None, -1))
        self.radioPort3.setText(QtWidgets.QApplication.translate("Dialog", "3", None, -1))
        self.radioPort4.setText(QtWidgets.QApplication.translate("Dialog", "4", None, -1))
        self.radioPort5.setText(QtWidgets.QApplication.translate("Dialog", "5", None, -1))
        self.radioPort6.setText(QtWidgets.QApplication.translate("Dialog", "6", None, -1))
        self.groupBoxAxis.setTitle(QtWidgets.QApplication.translate("Dialog", "Axis:", None, -1))
        self.radioZ.setText(QtWidgets.QApplication.translate("Dialog", "Z", None, -1))
        self.radioX.setText(QtWidgets.QApplication.translate("Dialog", "X", None, -1))
        self.radioY.setText(QtWidgets.QApplication.translate("Dialog", "Y", None, -1))
