# -*- coding: utf-8 -*-
# Authors: Ruslan Krenzler
# Date: 17 December 2020
# Move Dodo/Flamingo fittings.
# The name "Modification" is taken from the Draft-Workbench
import FreeCAD
import FreeCADGui
import OsePiping.Port as Port


def all_selected_parts_have_ports():
    for sel in FreeCADGui.Selection.getSelectionEx():
        if not Port.supportsAdvancedPort(sel.Object):
            return False
    return True
