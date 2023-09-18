#userSetup.py

#userSetup for the alembicExport tools

from maya import cmds, mel

def createAlembicExportMenu():
    mainWindow = mel.eval("$tmpVar = $gMainWindow")
    menuWidget = 'MtoU_alembicExportMenu'
    menuLabel = 'alembicExportTools'
    
    if cmds.menu(menuWidget, label=menuLabel, exists=1, parent=mainWindow):
        cmds.deleteUI(cmds.menu(menuWidget, e=1, deleteAllItems=1))
        
    menu = cmds.menu(menuWidget, label=menuLabel, parent=mainWindow, tearOff=1)
    cmds.menuItem(label='Create Export Set', command='import alembicSelectionSet; alembicSelectionSet.run()')
    cmds.menuItem(label='Export Alembic Cache', command='import alembicExportUI; alembicExportUI.AlembicExportUI().showWindow()')
    

    
    

if __name__ == "__main__":
    cmds.evalDeferred(createAlembicExportMenu)
