# OSE piping workbench

OSE Piping Workbench creates pipes and fittings. It is a part of Open Source Ecology and Open Source Ecology Germany. To use all its features install the Dodo-Workbench.

## Installation
Use the FreeCAD built-in [Addon Manager](https://github.com/FreeCAD/FreeCAD-addons#1-builtin-addon-manager) to install this workbench.
To start the Addon Manger select menu **Tools -> Addon Manager**.

[See](https://www.freecadweb.org/wiki/How_to_install_additional_workbenches)

### Linux

````
$ mkdir ~/.FreeCAD/Mod
$ cd ~/.FreeCAD/Mod
$ git clone https://github.com/rkrenzler/ose-piping-workbench.git
````

# Screenshots #
![90°-elbow dialog](doc/workbench-screenshot.png)

# Detailed documentation #
https://wiki.freecadweb.org/OSE_Piping_Workbench

# Optional dependencies
To use all features install [Dodo-Workbench](https://wiki.freecadweb.org/Dodo_Workbench). It brings:

 * Changeable parameters of the pipes and fittings.
 * Convenient moving and connection of the parts.

# Deprecated #
If you still use [Flamingo-Workbench](https://wiki.freecadweb.org/Flamingo_Workbench),
please install [Dodo-Workbench]. The support of Flamingo will be dropped in the future.

# Troubleshooting #
If you get an error message "module ... not found", try to remove all .pyc-files in the ose-piping module. Then restart FreeCAD.

# License #

Copyright (C) 2017 Stephen Kaiser <freesol29@gmail.com>  
Copyright (C) 2018 Ruslan Krenzler

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
