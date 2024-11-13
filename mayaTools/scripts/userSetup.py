#userSetup.py

#userSetup for the alembicExport tools

from maya import cmds
import menuBar

def addAlembicExportMenu():
    menuBar.createAlembicExportMenu()
    
    
if __name__ == "__main__":
    cmds.evalDeferred(addAlembicExportMenu)
