# MtoU_AlembicExport
Maya to Unreal Alembic Export Tools

I've worked on many cinematic projects in Unreal Engine. Most notably this one [here](https://www.youtube.com/watch?v=GNJtPFXUnm4).

With every project, the team groans as the time comes to export all the animation from Maya and import it into Unreal.
The tools I've made allow the process to be a lot quicker and less technical upfront.

This tool uses ALEMBIC CACHES as the file type of choice. This is because alembics are the most versatile for cinematic animation, as there is no limit on your deformers, like with FBX.

## Features

* Quickly identify desired objects for export within Maya
* Export those objects with the necessary alembic export options that work best in Unreal
* Maya UI for exporting one or multiple export locations
* Unreal UI with a simple drag-n-drop window to batch import animation

## Installation

1. Download and unzip the MtoU_AlembicExport file from [github releases](https://github.com/geodesicPenguin/MtoU_AlembicExport/releases).

MAYA:

2. Drag and drop the DRAG-N_DROP-IN-MAYA.py into Maya's viewport. You'll see the menu appear on the top bar of the Maya window. (Requires Maya restart to work)

UNREAL:

3. Enable Python in your Unreal project. Find out how to do that [here](https://www.youtube.com/watch?v=PMOvQ7mPv8k&list=PLBLmKCAjA25Br8cOVzUroqi_Nwipg-IdP&index=2).
4. Copy the unrealTools folder into the project's Script folder. (Just go to where your .uproject file is saved, there should be a Script folder right next to it)
5. In Unreal on the top bar, go to Tools > Execute Python Script. Browse for the alembicImportUI.py file. The UI will load and you can use Tools > Recent Python Scripts from now on to load the tool quicker.
NOTE: When running the Unreal UI, if the PySide2 module is not found, the tool will install it AUTOMATICALLY on first run. There is an uninstall file available as well, if you want to remove PySide2 from your Unreal Python environment.

