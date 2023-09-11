#install.py

"""
A drag-n-drop installer for Maya.

When run, it adds a .mod file to the maya/modules directiory.
This allows the tools menu to be loaded at each startup.
"""

from maya import cmds

def onMayaDroppedEvent():
    addModule()

def addModule():
    pass

def createMenu():
    pass

def addMenu():
    """Adds the menu immediately so there's no need to restart Maya."""
    
def successDialog():
    pass

