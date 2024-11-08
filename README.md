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
4. Go to Edit > Project Settings and find the Python tab on the left under Plugins. (Or type Python in the searchbar @ the top)
5. Next to "Additional Paths" hit the + and paste in the path to the unrealTools folder. That way, Unreal will know where to find the code for the import UI.

6. In the Alembic_Import_Tool folder, open Alembic_Import_Tool.ueproject.
7. In Unreal, navigate to the Alembic_Import_UI folder.
8. Right click on the folder and hit "Migrate".
9. Choose the project you'd like to add the tool to.

