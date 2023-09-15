#install.py
# C:/Program Files/Autodesk/Maya2024/modules;C:/Users/Lucas/Documents/maya/2024/modules;C:/Users/Lucas/Documents/maya/modules;C:/Program Files/Common Files/Autodesk Shared/Modules/maya/2024
"""
A drag-n-drop installer for Maya.

When run, it adds a .mod file to the maya/modules directiory.
This allows the tools menu to be loaded at each startup.
"""

'''TODO
for some reason im getting an os error.
run tool in script editor (maybe sys append it and run?)
check the print statements to diagnos error
'''

VERSION = 1.0

import os
from shutil import copytree, rmtree
from maya import cmds, mel

def onMayaDroppedPythonFile(*args, **kwargs):
    try:
        modulesDir = getModulesPath()       # Gets the path to the modules folder
        toolsDir = checkToolsDir()           # Checks the directory for the tools in the scripts folder
        copyFiles(toolsDir)                 # Copies the directory where this install file comes from, to the new tools directory
        writeModFile(modulesDir, toolsDir)  # Writes the needed .mod file
        createMenu()
        endDialog()
    except Exception as err:
        endDialog(error=err)
        print(err)
        

def getModulesPath():
    """Returns the path to Maya's modules folder.
    This is a separate function in case we want to use a different path in MAYA_MODULE_PATH
    in the future."""
    userAppDir = cmds.internalVar(userAppDir=1)
    modulesDir = os.path.join(userAppDir, 'modules')
    return modulesDir
    

def writeModFile(filepath, toolsDir):
    """Writes the .mod file. Maya needs this file to know to load the menu on startup."""
    fileContents = f'''+ MtoU_alembicExport {VERSION} {toolsDir}
    scripts 
    '''
    
    file = os.path.join(filepath, 'MtoU_alembicExport.mod')
    
    with open(file, 'w') as f:
        f.write(fileContents)


def checkToolsDir():
    """Checks for the existence of the directory for the tools to live in the scripts folder.
    If it exists, we delete it to make room for the files to be copied over."""
    scriptsDir = cmds.internalVar(userScriptDir=1)
    toolsDir = os.path.join(scriptsDir, 'MtoU_alembicExport')
    if os.path.exists(toolsDir):
        rmtree(toolsDir)
        
    return toolsDir


def copyFiles(copyDir):
    """Copies the necessary files to the created directory.""" 
    sourceDir = os.path.split(__file__)[0]
    copytree(src=sourceDir, dst=copyDir)
    print('DONE!!!!')
  
    
def createMenu():
    """Adds the menu immediately so there's no need to restart Maya."""
    mainWindow = mel.eval("$tmpVar = $gMainWindow")
    menuWidget = 'MtoU_alembicExportMenu'
    menuLabel = 'alembicExportTools'
    
    if cmds.menu(menuWidget, label=menuLabel, exists=1, parent=mainWindow):
        cmds.deleteUI(cmds.menu(menuWidget, e=1, deleteAllItems=1))
        
    menu = cmds.menu(menuWidget, label=menuLabel, parent=mainWindow, tearOff=1)
    cmds.menuItem(label='Create Export Set', command='alembicSelectionSet.run()')
    cmds.menuItem(label='Export Alembic Cache', command='amebicExportUI.AlembicExportUI()')

    
    
def endDialog(error=None):
    if error:
        cmds.confirmDialog(title='Failure',
                           message=f'{error}',
                           messageAlign='center')
        Exception
    else:
        cmds.confirmDialog(title='Install Complete',
                        message='''The alembic export tools have been installed.
                        Look for the menu on the top bar.''',
                        buttons=['OK'])

