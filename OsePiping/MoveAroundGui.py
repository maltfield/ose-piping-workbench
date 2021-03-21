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
import FreeCAD
import FreeCADGui as Gui
import OsePiping.Port as Port
import OsePipingBase


parseQuantity = FreeCAD.Units.parseQuantity


# See https://wiki.freecadweb.org/Code_snippets#Function_resident_with_the_mouse_click_action
# Mabe there is a better way to update selections.
class SelObserver:
    def __init__(self, panel):
        self.panel = panel

    def setPreselection(self, doc, obj, sub):                # Preselection object
        pass  # Do nothing

    def addSelection(self, doc, obj, sub, pnt):               # Selection object
        # doc is the name of the document.
        FreeCAD.Console.PrintMessage("addSelection")
        self.panel.updatePart(FreeCAD.getDocument(doc))

    def removeSelection(self, doc, obj, sub):                # Delete the selected object
        self.panel.updatePart(FreeCAD.getDocument(doc))

    def setSelection(self, doc):                           # Selection in ComboView
        self.panel.updatePart(FreeCAD.getDocument(doc))

    def clearSelection(self, doc):                         # If click on the screen, clear the selection
        self.panel.updatePart(FreeCAD.getDocument(doc))


# See https://github.com/yorikvanhavre/FreeCAD/blob/master/src/Mod/TemplatePyMod/TaskPanel.py
class MoveAroundPanel:
    QSETTINGS_APPLICATION = "OSE piping workbench"

    def __init__(self):
        self.ui = OsePipingBase.UI_PATH + "/move-around.ui"
        self.document = FreeCAD.activeDocument()
        self.part = Gui.Selection.getSelectionEx()[-1].Object
        self.selObserver = SelObserver(self)
        Gui.Selection.addObserver(self.selObserver)

    def accept(self):
        # It is not called, because we do not show "OK"-Button.
        FreeCAD.Console.PrintMessage("accept")
        self.document.recompute()
        Gui.Selection.removeObserver(self.selObserver)
        self.saveInput()
        return True

    def reject(self):
        FreeCAD.Console.PrintMessage("reject")
        self.document.recompute()
        Gui.Selection.removeObserver(self.selObserver)
        return True

    def clicked(self, index):
        pass

    def open(self):
        pass

    def needsFullSpace(self):
        return False

    def isAllowedAlterSelection(self):
        return True

    def isAllowedAlterView(self):
        return True

    def isAllowedAlterDocument(self):
        return False

    def getStandardButtons(self):
        return int(QtGui.QDialogButtonBox.Close)

    def helpRequested(self):
        pass

    def setupChildWidgets(self, form):
        """Find all used widgets in the form and assign them to class varialbes
        for fast access.

        Is here a faster way to do this task?
        """
        self.labelPartName = form.findChild(QtGui.QLabel, "labelPartName")
        self.radioPort1 = form.findChild(QtGui.QRadioButton, "radioPort1")
        self.radioPort2 = form.findChild(QtGui.QRadioButton, "radioPort2")
        self.radioPort3 = form.findChild(QtGui.QRadioButton, "radioPort3")
        self.radioPort4 = form.findChild(QtGui.QRadioButton, "radioPort4")
        self.radioPort5 = form.findChild(QtGui.QRadioButton, "radioPort5")
        self.radioPort6 = form.findChild(QtGui.QRadioButton, "radioPort6")
        self.radioX = form.findChild(QtGui.QRadioButton, "radioX")
        self.radioY = form.findChild(QtGui.QRadioButton, "radioY")
        self.radioZ = form.findChild(QtGui.QRadioButton, "radioZ")
        self.editDegree = form.findChild(QtGui.QLineEdit, "editDegree")
        self.dialDegree = form.findChild(QtGui.QDial, "dialDegree")
        self.buttonReverse = form.findChild(QtGui.QPushButton, "buttonReverse")
        self.buttonZeroAngle = form.findChild(QtGui.QPushButton, "buttonZeroAngle")
        self.buttonApplyShift = form.findChild(QtGui.QPushButton, "buttonApplyShift")

        self.buttonZeroLength = form.findChild(QtGui.QPushButton, "buttonZeroLength")
        self.editShift = form.findChild(QtGui.QLineEdit, "editShift")
        self.buttonApplyRotate = form.findChild(QtGui.QPushButton, "buttonApplyRotate")

    def setupUi(self):
        # Call it from OsePipingCommands after Gui.Control.showDialog(panel)
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QDialog, "MoveAroundPanel")
        self.setupChildWidgets(form)
        self.setupCallbacks()

        self.form = form

        # Restore previous user input.
        # Ignore exceptions in order to start GUI even with broken settings.
        try:
            self.restoreInput()
        except Exception as e:
            print("Could not restore old user input!")
            print(e)

        self.updateWidgets()

    def updatePart(self, doc):
        # Only react to activ document.
        self.document = doc
        self.part = Gui.Selection.getSelectionEx()[-1].Object
        self.updateWidgets()

    def updateWidgets(self):
        self.labelPartName.setText(self.part.Name)
        self.showPorts(self.part)

    def setupCallbacks(self):
        QtCore.QObject.connect(self.buttonReverse, QtCore.SIGNAL("clicked()"), self.onReverseClicked)
        QtCore.QObject.connect(self.dialDegree, QtCore.SIGNAL("valueChanged(int)"), self.onDialDegreeChanged)
        QtCore.QObject.connect(self.buttonZeroAngle, QtCore.SIGNAL("clicked()"), self.onZeroAngleClicked)
        QtCore.QObject.connect(self.editDegree, QtCore.SIGNAL("editingFinished()"), self.onEditDegreeChanged)
        QtCore.QObject.connect(self.radioPort1, QtCore.SIGNAL("clicked()"), self.onPortRadioSelected)
        QtCore.QObject.connect(self.radioPort2, QtCore.SIGNAL("clicked()"), self.onPortRadioSelected)
        QtCore.QObject.connect(self.radioPort3, QtCore.SIGNAL("clicked()"), self.onPortRadioSelected)
        QtCore.QObject.connect(self.radioPort4, QtCore.SIGNAL("clicked()"), self.onPortRadioSelected)
        QtCore.QObject.connect(self.radioPort5, QtCore.SIGNAL("clicked()"), self.onPortRadioSelected)
        QtCore.QObject.connect(self.radioPort6, QtCore.SIGNAL("clicked()"), self.onPortRadioSelected)
        QtCore.QObject.connect(self.radioX, QtCore.SIGNAL("clicked()"), self.onAxisRadioSelected)
        QtCore.QObject.connect(self.radioY, QtCore.SIGNAL("clicked()"), self.onAxisRadioSelected)
        QtCore.QObject.connect(self.radioZ, QtCore.SIGNAL("clicked()"), self.onAxisRadioSelected)
        QtCore.QObject.connect(self.buttonZeroLength, QtCore.SIGNAL("clicked()"), self.onZeroLengthClicked)

        QtCore.QObject.connect(self.buttonApplyRotate, QtCore.SIGNAL("clicked()"), self.onApplyRotateClicked)
        QtCore.QObject.connect(self.buttonApplyShift, QtCore.SIGNAL("clicked()"), self.onApplyShiftClicked)

    def getMainWindow(self):
        "returns the main window"
        # using QtGui.QApplication.activeWindow() isn't very reliable because if another
        # widget than the mainwindow is active (e.g. a dialog) the wrong widget is
        # returned
        toplevel = QtGui.QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                return i
        raise RuntimeError("No main window found")

    def saveInput(self):
        """Store user input for the next run."""
        settings = QtCore.QSettings(MoveAroundPanel.QSETTINGS_APPLICATION, "MoveAroundPanel")

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
        settings.setValue("editShift", str(self.editShift.text()))
        settings.sync()

    def restoreInput(self):
        settings = QtCore.QSettings(
            MoveAroundPanel.QSETTINGS_APPLICATION, "MoveAroundPanel")
        # For some reasons settings.value("radioPort1", False) returns a string.
        # We convert it to boolean.
        self.radioPort1.setChecked(bool(settings.value("radioPort1", False)))
        self.radioPort2.setChecked(bool(settings.value("radioPort2", False)))
        self.radioPort3.setChecked(bool(settings.value("radioPort3", False)))
        self.radioPort4.setChecked(bool(settings.value("radioPort4", False)))
        self.radioPort5.setChecked(bool(settings.value("radioPort5", False)))
        self.radioPort6.setChecked(bool(settings.value("radioPort6", False)))

        self.radioX.setChecked(bool(settings.value("radioX", False)))
        self.radioY.setChecked(bool(settings.value("radioY", False)))
        self.radioZ.setChecked(bool(settings.value("radioZ", False)))

        self.editDegree.setText(settings.value("editDegree", "0"))
        self.editShift.setText(settings.value("editShift", "0mm"))
        self.onEditDegreeChanged()

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

    def onZeroAngleClicked(self):
        self.dialDegree.setValue(0.0)

    def onZeroLengthClicked(self):
        self.editShift.setText("0mm")

    def getRotation(self):
        """Return rotation vector.

        Return rotation vector. Return None if no Rotation
        could be detected. Thes can happen if no check box
        for rotation is selected or a non-existing port is selected.

        return: Rotation matrix or None.
        """
        nports = len(self.part.Ports)

        angle = self.dialDegree.value()
        if self.radioX.isChecked():
            return FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), angle)  # Rotation matrix
        elif self.radioY.isChecked():
            return FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), angle)
        elif self.radioZ.isChecked():
            return FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), angle)
        elif self.radioPort1.isChecked() and nports >= 1:
            return FreeCAD.Rotation(self.part.Ports[0], angle)
        elif self.radioPort2.isChecked() and nports >= 2:
            return FreeCAD.Rotation(self.part.Ports[1], angle)
        elif self.radioPort3.isChecked() and nports >= 3:
            return FreeCAD.Rotation(self.part.Ports[2], angle)
        elif self.radioPort4.isChecked() and nports >= 4:
            return FreeCAD.Rotation(self.part.Ports[3], angle)
        elif self.radioPort5.isChecked() and nports >= 5:
            return FreeCAD.Rotation(self.part.Ports[4], angle)
        elif self.radioPort6.isChecked() and nports >= 6:
            return FreeCAD.Rotation(self.part.Ports[5], angle)
        else:
            return  # Return None.

    def getShiftDirection(self):
        """Return shift direction as a normalized Vector.

        :return: Shift direction as a Vector.
        :return: None, if the directon could not be determined.
        """
        nports = len(self.part.Ports)

        if self.radioX.isChecked():
            return FreeCAD.Vector(1, 0, 0)
        elif self.radioY.isChecked():
            return FreeCAD.Vector(0, 1, 0)
        elif self.radioZ.isChecked():
            return FreeCAD.Vector(0, 0, 1)
        elif self.radioPort1.isChecked() and nports >= 1:
            # Move towards the Port. Take in account the current rotation
            # of the part.
            v = self.part.Placement.Rotation.multVec(self.part.Ports[0])
            return v / v.Length
        elif self.radioPort2.isChecked() and nports >= 2:
            v = self.part.Placement.Rotation.multVec(self.part.Ports[1])
            return v / v.Length
        elif self.radioPort3.isChecked() and nports >= 3:
            v = self.part.Placement.Rotation.multVec(self.part.Ports[2])
            return v / v.Length
        elif self.radioPort4.isChecked() and nports >= 4:
            v = self.part.Placement.Rotation.multVec(self.part.Ports[3])
            return v / v.Length
        elif self.radioPort5.isChecked() and nports >= 5:
            v = self.part.Placement.Rotation.multVec(self.part.Ports[4])
            return v / v.Length
        elif self.radioPort6.isChecked() and nports >= 6:
            v = self.part.Placement.Rotation.multVec(self.part.Ports[5])
            return v / v.Length
        else:
            return  # Return None.

    def getShiftLength(self):
        """Return shift distance.

        :return: Shift distance in Standard FreeCAD units (mm).
        :return: 0.0 if the edit field is empty.
        :return: None, if the text in the edit field could not be parsed.
        """
        txt = self.editShift.text()
        if txt == "":
            return 0.0
        try:
            return FreeCAD.Units.parseQuantity(txt).Value
        except Exception as ex:
            FreeCAD.Console.PrintWarning("Cannot parse the shift string.\n")
            FreeCAD.Console.PrintWarning(str(ex) + "\n")
            return None

    def onApplyRotateClicked(self):
        self.saveInput()
        R = self.getRotation()

        if R is None:
            # Something went wrong, do nothing.
            FreeCAD.Console.PrintWarning("Cannot dermine rotation parameters. Do nothing.\n")
            return

        # FreeCAD.Console.PrintMessage("Rotation: " + str(R) + "\n")
        self.part.Placement.Rotation = self.part.Placement.Rotation.multiply(R)

    def onApplyShiftClicked(self):
        self.saveInput()
        sh_dir = self.getShiftDirection()
        sh_len = self.getShiftLength()

        if sh_dir is None or sh_len is None:
            # Something went wrong, do nothing.
            FreeCAD.Console.PrintWarning("Cannot dermine all shift parameters. Do nothing.\n")
            return

        # FreeCAD.Console.PrintMessage("Shift direction: " + str(sh_dir) + "\n")
        # FreeCAD.Console.PrintMessage("Shift length: " + str(sh_len) + "\n")
        self.part.Placement.Base = self.part.Placement.Base + sh_len * sh_dir
