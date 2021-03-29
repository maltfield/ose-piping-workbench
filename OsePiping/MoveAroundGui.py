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
        self.port_i = self.getPortIndexOfSelection(Gui.Selection.getSelectionEx()[-1])
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
        self.radioPorts = []
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort1"))
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort2"))
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort3"))
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort4"))
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort5"))
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort6"))
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

    def getPortIndexOfSelection(self, selection):
        """Estimate port index of a selected part."""

        if (len(selection.SubObjects) > 0):
            # Only a pipe has ports on creation. The other fitting can be accessed only through their objects.
            part = selection.Object
            sub = selection.SubObjects[-1]
            ports = Port.extractAdvancedPorts(part)
            i = Port.getNearestPortIndex(part.Placement, ports, sub.CenterOfMass)
            FreeCAD.Console.PrintMessage("Select Port {}\n".format(i + 1))
            return i
        return -1

    def updatePart(self, doc):
        # Only react to activ document.
        self.document = doc
        self.part = Gui.Selection.getSelectionEx()[-1].Object
        # Change selected port only if a port was selected.
        port_i = self.getPortIndexOfSelection(Gui.Selection.getSelectionEx()[-1])
        if port_i >= 0:
            self.port_i = port_i
        self.updateWidgets()

    def updateWidgets(self):
        self.labelPartName.setText(self.part.Name)
        self.showPorts(self.part, self.port_i)

    def setupCallbacks(self):
        QtCore.QObject.connect(self.buttonReverse, QtCore.SIGNAL("clicked()"), self.onReverseClicked)
        QtCore.QObject.connect(self.dialDegree, QtCore.SIGNAL("valueChanged(int)"), self.onDialDegreeChanged)
        QtCore.QObject.connect(self.buttonZeroAngle, QtCore.SIGNAL("clicked()"), self.onZeroAngleClicked)
        QtCore.QObject.connect(self.editDegree, QtCore.SIGNAL("editingFinished()"), self.onEditDegreeChanged)
        for radioPort in self.radioPorts:
            QtCore.QObject.connect(radioPort, QtCore.SIGNAL("clicked()"), self.onPortRadioSelected)
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

        settings.setValue("radioPort1", self.radioPorts[0].isChecked())
        settings.setValue("radioPort2", self.radioPorts[1].isChecked())
        settings.setValue("radioPort3", self.radioPorts[2].isChecked())
        settings.setValue("radioPort4", self.radioPorts[3].isChecked())
        settings.setValue("radioPort5", self.radioPorts[4].isChecked())
        settings.setValue("radioPort6", self.radioPorts[5].isChecked())

        settings.setValue("radioX", self.radioX.isChecked())
        settings.setValue("radioY", self.radioY.isChecked())
        settings.setValue("radioZ", self.radioZ.isChecked())

        settings.setValue("editDegree", str(self.editDegree.text()))
        settings.setValue("editShift", str(self.editShift.text()))
        settings.sync()

    @staticmethod
    def isTrue(v):
        # For some reasons settings.value("radioPort1", False) returns a string.
        # "true" or "false" if radioPort1 was previously saved.
        # We convert it to boolean.
        # note bool("false") is True. That is why we will use == "true" instead.
        # Just in case, I added also a comparison with True and "True".
        if v is True or v == 'True' or v == 'true':
            return True
        return False

    def restoreInput(self):
        settings = QtCore.QSettings(MoveAroundPanel.QSETTINGS_APPLICATION, "MoveAroundPanel")
        # Restore only Input if no valid port is selected on initialization.
        if self.port_i < 0:
            self.radioPorts[0].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort1", False)))
            self.radioPorts[1].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort2", False)))
            self.radioPorts[2].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort3", False)))
            self.radioPorts[3].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort4", False)))
            self.radioPorts[4].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort5", False)))
            self.radioPorts[5].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort6", False)))
            self.onPortRadioSelected()

            self.radioX.setChecked(MoveAroundPanel.isTrue(settings.value("radioX", False)))
            self.radioY.setChecked(MoveAroundPanel.isTrue(settings.value("radioY", False)))
            self.radioZ.setChecked(MoveAroundPanel.isTrue(settings.value("radioZ", False)))
            self.onAxisRadioSelected()

        self.editDegree.setText(settings.value("editDegree", "0"))
        self.editShift.setText(settings.value("editShift", "0mm"))
        self.onEditDegreeChanged()

    def showPorts(self, part, port_i):
        if Port.supportsAdvancedPort(part):
            nports = len(part.Ports)
        else:
            nports = 0

        for i in range(0, nports):
            self.radioPorts[i].setEnabled(True)
        for i in range(nports, len(self.radioPorts)):
            self.radioPorts[i].setEnabled(False)

        if port_i >= 0:
            self.radioPorts[port_i].setChecked(True)

    def onPortRadioSelected(self):
        for i in range(0, 6):
            if self.radioPorts[i].isChecked():
                self.port_i = i
                FreeCAD.Console.PrintWarning("onPortRadioSelected Selected Port {}.\n".format(self.port_i + 1))

    def onAxisRadioSelected(self):
        if self.radioX.isChecked() or self.radioY.isChecked() or self.radioZ.isChecked():
            self.port_i = -1

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

        if 0 <= self.port_i < nports:
            return FreeCAD.Rotation(self.part.Ports[self.port_i], angle)

        return  # Return None.

    def getShiftDirection(self):
        """Return shift direction as a normalized Vector.

        :return: Shift direction as a Vector.
        :return: None, if the directon could not be determined.
        """
        ports = Port.extractAdvancedPorts(self.part)

        nports = len(ports)

        if self.radioX.isChecked():
            return FreeCAD.Vector(1, 0, 0)
        elif self.radioY.isChecked():
            return FreeCAD.Vector(0, 1, 0)
        elif self.radioZ.isChecked():
            return FreeCAD.Vector(0, 0, 1)

        if 0 <= self.port_i < nports:
            # Move towards the normal of the Port.
            # Take in account the current rotation
            # of the part.
            v = self.part.Placement.Rotation.multVec(ports[self.port_i].getNormal())
            return v / v.Length
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
