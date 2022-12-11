# -*- coding: utf-8 -*-
# Author: Ruslan Krenzler.
# Date: 10 December 2022
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
from OsePiping.MoveAroundGui import MoveAroundPanel, SelObserver

parseQuantity = FreeCAD.Units.parseQuantity


# See https://github.com/yorikvanhavre/FreeCAD/blob/master/src/Mod/TemplatePyMod/TaskPanel.py
class MoveToPanel:
    QSETTINGS_APPLICATION = "OSE piping workbench"

    def __init__(self):
        self.ui = OsePipingBase.UI_PATH + "/move-to.ui"
        self.document = FreeCAD.activeDocument()
        # The part which needs to be moved.

        self.what_part = None
        self.what_port_i = -1
        # The part where the moved part needs to be moved to.
        self.to_part = None
        self.to_port_i = -1
        self.updateSelection()
        self.selObserver = SelObserver(self)
        Gui.Selection.addObserver(self.selObserver)

    def accept(self):
        # It is not called, because we do not show "OK"-Button.
#        FreeCAD.Console.PrintMessage("accept")
        if self.document is not None:
            self.document.recompute()
        Gui.Selection.removeObserver(self.selObserver)
        self.saveInput()
        return True

    def reject(self):
        # FreeCAD.Console.PrintMessage("reject")
        Gui.Selection.removeObserver(self.selObserver)
        if self.document is not None:
            self.document.recompute()
        self.saveInput()
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
        self.labelInstructions = form.findChild(QtGui.QLabel, "labelInstructions")
        self.labelPartName = form.findChild(QtGui.QLabel, "labelPartName")
        self.radioPorts = []
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort1"))
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort2"))
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort3"))
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort4"))
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort5"))
        self.radioPorts.append(form.findChild(QtGui.QRadioButton, "radioPort6"))
        self.editDegree = form.findChild(QtGui.QLineEdit, "editDegree")
        self.dialDegree = form.findChild(QtGui.QDial, "dialDegree")
        self.buttonReverse = form.findChild(QtGui.QPushButton, "buttonReverse")
        self.buttonZeroAngle = form.findChild(QtGui.QPushButton, "buttonZeroAngle")

        self.labelDestinationPartName = form.findChild(QtGui.QLabel, "labelDestinationPartName")
        self.radioDestinationPorts = []
        self.radioDestinationPorts.append(form.findChild(QtGui.QRadioButton, "radioDestinationPort1"))
        self.radioDestinationPorts.append(form.findChild(QtGui.QRadioButton, "radioDestinationPort2"))
        self.radioDestinationPorts.append(form.findChild(QtGui.QRadioButton, "radioDestinationPort3"))
        self.radioDestinationPorts.append(form.findChild(QtGui.QRadioButton, "radioDestinationPort4"))
        self.radioDestinationPorts.append(form.findChild(QtGui.QRadioButton, "radioDestinationPort5"))
        self.radioDestinationPorts.append(form.findChild(QtGui.QRadioButton, "radioDestinationPort6"))

        self.buttonZeroGap = form.findChild(QtGui.QPushButton, "buttonZeroGap")
        self.editGap = form.findChild(QtGui.QLineEdit, "editGap")

        self.buttonUnselectAll = form.findChild(QtGui.QPushButton, "buttonUnselectAll")
        self.buttonApply = form.findChild(QtGui.QPushButton, "buttonApply")

    def setupUi(self):
        # Call it from OsePipingCommands after Gui.Control.showDialog(panel)
        mw = self.getMainWindow()
        form = mw.findChild(QtGui.QDialog, "MoveToPanel")
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

    def updateSelection(self):
        nsel = len(Gui.Selection.getSelectionEx())
        # First part is the movable object, the next part is
        # the destination. If the are more than two parts,
        # the next-to-last object is the movable part and
        # the last object the destionation part.
        #FreeCAD.Console.PrintMessage("updateSelection Number of selected objects {}.\n".format(nsel))
        if nsel >= 2:
            object_sel = -2
            destination_sel = -1
#            FreeCAD.Console.PrintMessage("updateSelection at least two objects.\n")
        elif nsel == 1:
            # Wait for destination object.
#            FreeCAD.Console.PrintMessage("updateSelection Select destination.\n")
            object_sel = -1
            destination_sel = None
        else:
            #FreeCAD.Console.PrintMessage("updateSelection Nothing is selcted.\n")
            self.what_part = None
            self.to_part = None
            return # Do nothing.

        curr_sel = Gui.Selection.getSelection()
        self.what_part = Gui.Selection.getSelectionEx()[object_sel].Object
        # Change selected port only if a port was selected.
        #FreeCAD.Console.PrintMessage("Selected index of the movable object is {} the name is {}.\n".format(object_sel, self.what_part.Name))

        port_i = MoveAroundPanel.getPortIndexOfSelection(Gui.Selection.getSelectionEx()[object_sel])
        #FreeCAD.Console.PrintMessage("Port of the movable object is {}.\n".format(port_i+1))
        if port_i >= 0:
            self.what_port_i = port_i
            FreeCAD.Console.PrintMessage("Set new movable port to {}.\n".format(port_i+1))

        if destination_sel is not None:
            self.to_part = Gui.Selection.getSelectionEx()[destination_sel].Object
            #FreeCAD.Console.PrintMessage("Selected index of the destination object is {} the name is {}.\n".format(destination_sel, self.to_part.Name))
            port_i = MoveAroundPanel.getPortIndexOfSelection(Gui.Selection.getSelectionEx()[destination_sel])
            #FreeCAD.Console.PrintMessage("Port of the destination object is {}.\n".format(port_i+1))
            if port_i >= 0:
                self.to_port_i = port_i
                #FreeCAD.Console.PrintMessage("Set new destionat port {}.\n".format(port_i+1))
        else:
            self.to_part = None
            #FreeCAD.Console.PrintMessage("No destination part is selected.\n")

    def updatePart(self, doc):
        # Only react to activ document.
        self.document = doc
        if doc is not None:
            self.updateSelection()
        else:
            FreeCAD.Console.PrintMessage("No document and no part is selected.\n")
            self.part = None

        self.updateWidgets()

    @staticmethod
    def getPartName(part):
        if MoveToPanel.isSelectedPartSupported(part):
            return part.Name
        else:
            return part.Name + " (not supported)"

    def updateWidgets(self):
        if self.what_part is not None:
            self.labelPartName.setText(MoveToPanel.getPartName(self.what_part))
        else:
            self.labelPartName.setText("Select part to be moved.")

        if self.to_part is not None:
            self.labelDestinationPartName.setText(MoveToPanel.getPartName(self.to_part))
        else:
            self.labelDestinationPartName.setText("Select part where to move to.")

        self.showPorts(self.what_part, self.what_port_i)
        self.showDestinationPorts(self.to_part, self.to_port_i)

        if self.what_part is None:
            self.labelInstructions.setText("Select part to move.")
        elif self.to_part is None:
            self.labelInstructions.setText("Select destionation part.")
        else:
            self.labelInstructions.setText("")

    def setupCallbacks(self):
        QtCore.QObject.connect(self.buttonReverse, QtCore.SIGNAL("clicked()"), self.onReverseClicked)
        QtCore.QObject.connect(self.dialDegree, QtCore.SIGNAL("valueChanged(int)"), self.onDialDegreeChanged)
        QtCore.QObject.connect(self.editDegree, QtCore.SIGNAL("editingFinished()"), self.onEditDegreeChanged)
        QtCore.QObject.connect(self.buttonZeroAngle, QtCore.SIGNAL("clicked()"), self.onZeroAngleClicked)
        for radioPort in self.radioPorts:
            QtCore.QObject.connect(radioPort, QtCore.SIGNAL("clicked()"), self.onPortRadioSelected)

        for radioPort in self.radioDestinationPorts:
            QtCore.QObject.connect(radioPort, QtCore.SIGNAL("clicked()"), self.onDestinationPortRadioSelected)

        QtCore.QObject.connect(self.buttonZeroGap, QtCore.SIGNAL("clicked()"), self.onZeroGapClicked)

        QtCore.QObject.connect(self.buttonUnselectAll, QtCore.SIGNAL("clicked()"), self.onUnselectAllClicked)
        QtCore.QObject.connect(self.buttonApply, QtCore.SIGNAL("clicked()"), self.onApplyClicked)

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
        settings = QtCore.QSettings(MoveToPanel.QSETTINGS_APPLICATION, "MoveToPanel")

        settings.setValue("radioPort1", self.radioPorts[0].isChecked())
        settings.setValue("radioPort2", self.radioPorts[1].isChecked())
        settings.setValue("radioPort3", self.radioPorts[2].isChecked())
        settings.setValue("radioPort4", self.radioPorts[3].isChecked())
        settings.setValue("radioPort5", self.radioPorts[4].isChecked())
        settings.setValue("radioPort6", self.radioPorts[5].isChecked())

        settings.setValue("editDegree", str(self.editDegree.text()))

        settings.setValue("editGap", str(self.editGap.text()))

        settings.setValue("radioDestinationPort1", self.radioDestinationPorts[0].isChecked())
        settings.setValue("radioDestinationPort2", self.radioDestinationPorts[1].isChecked())
        settings.setValue("radioDestinationPort3", self.radioDestinationPorts[2].isChecked())
        settings.setValue("radioDestinationPort4", self.radioDestinationPorts[3].isChecked())
        settings.setValue("radioDestinationPort5", self.radioDestinationPorts[4].isChecked())
        settings.setValue("radioDestinationPort6", self.radioDestinationPorts[5].isChecked())

        settings.sync()

    def restoreInput(self):
        settings = QtCore.QSettings(MoveToPanel.QSETTINGS_APPLICATION, "MoveToPanel")
        # Restore only Input if no valid port is selected on initialization.
        if self.what_port_i < 0:
            self.radioPorts[0].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort1", False)))
            self.radioPorts[1].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort2", False)))
            self.radioPorts[2].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort3", False)))
            self.radioPorts[3].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort4", False)))
            self.radioPorts[4].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort5", False)))
            self.radioPorts[5].setChecked(MoveAroundPanel.isTrue(settings.value("radioPort6", False)))
            self.onPortRadioSelected()

        self.editDegree.setText(settings.value("editDegree", "0"))

        self.editGap.setText(settings.value("editGap", "0mm"))

        # Restore only Input if no valid port is selected on initialization.
        if self.to_port_i < 0:
            self.radioDestinationPorts[0].setChecked(MoveAroundPanel.isTrue(settings.value("radioDestinationPort1", False)))
            self.radioDestinationPorts[1].setChecked(MoveAroundPanel.isTrue(settings.value("radioDestinationPort2", False)))
            self.radioDestinationPorts[2].setChecked(MoveAroundPanel.isTrue(settings.value("radioDestinationPort3", False)))
            self.radioDestinationPorts[3].setChecked(MoveAroundPanel.isTrue(settings.value("radioDestinationPort4", False)))
            self.radioDestinationPorts[4].setChecked(MoveAroundPanel.isTrue(settings.value("radioDestinationPort5", False)))
            self.radioDestinationPorts[5].setChecked(MoveAroundPanel.isTrue(settings.value("radioDestinationPort6", False)))
            self.onDestinationPortRadioSelected()

        self.onEditDegreeChanged()

    def showPorts(self, part, port_i):
        if part is not None and Port.supportsAdvancedPort(part):
            nports = len(part.Ports)
        else:
            nports = 0

        for i in range(0, nports):
            self.radioPorts[i].setEnabled(True)
        for i in range(nports, len(self.radioPorts)):
            self.radioPorts[i].setEnabled(False)

        if port_i >= 0:
            self.radioPorts[port_i].setChecked(True)

    def showDestinationPorts(self, part, port_i):
        if part is not None and Port.supportsAdvancedPort(part):
            nports = len(part.Ports)
        else:
            nports = 0

        for i in range(0, nports):
            self.radioDestinationPorts[i].setEnabled(True)
        for i in range(nports, len(self.radioPorts)):
            self.radioDestinationPorts[i].setEnabled(False)

        if port_i >= 0:
            self.radioDestinationPorts[port_i].setChecked(True)

    def onPortRadioSelected(self):
        for i in range(0, 6):
            if self.radioPorts[i].isChecked():
                self.what_port_i = i
                #FreeCAD.Console.PrintMessage("onPortRadioSelected Selected Port {}.\n".format(self.what_port_i + 1))

    def onDestinationPortRadioSelected(self):
        for i in range(0, 6):
            if self.radioDestinationPorts[i].isChecked():
                self.to_port_i = i
                #FreeCAD.Console.PrintMessage("onDestinationPortRadioSelected Selected Port {}.\n".format(self.to_port_i + 1))

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

    def onZeroGapClicked(self):
        self.editGap.setText("0mm")

    @staticmethod
    def isSelectedPartSupported(part):
        """Check if the selected part is supported for movment.

        If the part is not supported print a warning.
        """
        if part is None:
            FreeCAD.Console.PrintWarning("No part selected. Do nothing.\n")
            return False

        if not Port.supportsAdvancedPort(part):
            FreeCAD.Console.PrintWarning("This part is not supported.\n")
            return False

        return True

    def getRotation(self):
        """Return rotation vector.

        Return rotation vector. Return None if no Rotation
        could be detected. Thes can happen if no check box
        for rotation is selected or a non-existing port is selected.

        return: Rotation matrix or None.
        """
        ports = MoveAroundPanel.getPorts(self.what_part)
        nports = len(ports)

        angle = self.dialDegree.value()
        if 0 <= self.what_port_i < nports:
            return FreeCAD.Rotation(ports[self.what_port_i].getNormal(), angle)
        else:
            return  # Return None.

    def getGlobalDestination(self):
        """Return global position of the destination port."""
        part = self.to_part
        nports = MoveAroundPanel.getPorts(part)

        if 0 <= self.to_port_i < nports:
            v = part.Placement.Rotation.multVec(part.Ports[self.to_port_i])
        else:
            return  # Return None.

        return part.Placement.Base + v

    def getGapDirection(self):
        """Return gap direction as a normalized Vector.

        :return: Gap direction as a Vector.
        :return: None, if the directon could not be determined.
        """
        part = self.what_part
        ports = MoveAroundPanel.getPorts(part)
        nports = len(ports)

        if 0 <= self.what_port_i < nports:
            # Note, the gap direction is in oposited direction to the normal
            # direction.
            v = part.Placement.Rotation.multVec(ports[self.what_port_i].getNormal())
            return -v / v.Length
        else:
            return  # Do nothing.

    def getGapLength(self):
        """Return shift distance.

        :return: Shift distance in Standard FreeCAD units (mm).
        :return: 0.0 if the edit field is empty.
        :return: None, if the text in the edit field could not be parsed.
        """
        txt = self.editGap.text()
        if txt == "":
            return 0.0
        try:
            return FreeCAD.Units.parseQuantity(txt).Value
        except Exception as ex:
            FreeCAD.Console.PrintWarning("Cannot parse the gap string.\n")
            FreeCAD.Console.PrintWarning(str(ex) + "\n")
            return None

    @staticmethod
    def moveTo(part, porti: int, to_part, to_porti: int):
        """Move a part to another part, such that their ports coinside.

        Move a part to antother part. Both parts must be Dodo parts with
        advancedPorts.

        :param part: Part to be moved.
        :param porti: Port index of the moved part, which will connect to another part.
        :param to_part: Part to which another part will be moved.
          This part does not channge its position.
        :param to_porti: Port index where another part will be moved to.
        """
        # Now adjust part to
        # print(obj_of_part.Placement)
        ports = Port.extractAdvancedPorts(part)
        to_ports = Port.extractAdvancedPorts(to_part)
        if (0 <= porti < len(ports)) and (0 <= to_porti < len(to_ports)):
            # FreeCAD.Console.PrintMessage("Move port {} to port {}.\n".format(porti + 1, to_porti + 1))
            port = ports[porti]
            to_port = to_ports[to_porti]
            part.Placement = port.getPartPlacement(to_part.Placement, to_port)
            # FreeCAD.Console.PrintMessage("New placement {}.\n".format(part.Placement))

    def onApplyClicked(self):
        self.saveInput()
        R = self.getRotation()
        gap_len = self.getGapLength()
        # This call only checks, if FreeCAD can understand user input.
        # gap_dir must be recalculated after a rotation.
        gap_dir = self.getGapDirection()

        if R is None or gap_dir is None or gap_len is None:
            # Something went wrong, do nothing.
            FreeCAD.Console.PrintWarning("Cannot dermine all movement parameters. Do nothing.\n")
            return

        # FreeCAD.Console.PrintMessage("Rotation: " + str(R) + "\n")
        # FreeCAD.Console.PrintMessage("Gap direction: " + str(gap_dir) + "\n")
        # FreeCAD.Console.PrintMessage("Shift length: " + str(gap_len) + "\n")

        MoveToPanel.moveTo(self.what_part, self.what_port_i, self.to_part, self.to_port_i)
        # Recalculate gap direction after the rotation.
        gap_dir = self.getGapDirection()
        self.what_part.Placement.Base = self.what_part.Placement.Base + gap_len * gap_dir

    def onUnselectAllClicked(self):
        if self.document != None:
            Gui.Selection.clearSelection(self.document.Name)
