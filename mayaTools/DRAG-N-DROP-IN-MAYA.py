#DRAG-N-DROP-IN-MAYA.py
# C:/Program Files/Autodesk/Maya2024/modules;C:/Users/Lucas/Documents/maya/2024/modules;C:/Users/Lucas/Documents/maya/modules;C:/Program Files/Common Files/Autodesk Shared/Modules/maya/2024
"""
A drag-n-drop installer for Maya.

When run, it adds a .mod file to the maya/modules directory.
This allows the tools menu to be loaded at each startup.
It also copies the code to the scripts folder.
"""


VERSION = 1.0

import os
import sys
from shutil import copytree, rmtree
from maya import cmds

from scripts.menuBar import createAlembicExportMenu

def onMayaDroppedPythonFile(*args, **kwargs):
    try:
        modulesDir = getModulesPath()       # Gets the path to the modules folder
        modulesPathExist()                   # Checks if the modules path exists, if not, it creates it
        toolsDir = checkToolsDir()           # Checks the directory for the tools in the scripts folder
        copyFiles(toolsDir)                 # Copies the directory where this install file comes from, to the new tools directory
        writeModFile(modulesDir, toolsDir)  # Writes the needed .mod file
        menu()
        endDialog()
    except Exception as err:
        endDialog(error=err)
        raise err
        

def getModulesPath():
    """Returns the path to Maya's modules folder.
    This is a separate function in case we want to use a different path in MAYA_MODULE_PATH
    in the future."""
    userAppDir = cmds.internalVar(userAppDir=1)
    modulesDir = os.path.join(userAppDir, 'modules')
    return modulesDir


def modulesPathExist():
    """If the modules path doesn't exist, we create it."""
    modulesDir = getModulesPath()
    if not os.path.exists(modulesDir):
        os.makedirs(modulesDir)
    

def writeModFile(filepath, toolsDir):
    """Writes the .mod file. Maya needs this file to know to load the menu on startup."""
    fileContents = f'''+ MtoU_alembicExport {VERSION} {toolsDir}
scripts: .
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
    sourceDir = os.path.join(os.path.dirname(__file__), 'scripts')
    copytree(src=sourceDir, dst=copyDir)
  
    
def menu():
    """This allows for the menu to be available on install, rather than restarting the software."""
    createAlembicExportMenu()
    scripts_path = os.path.join(os.path.dirname(__file__), 'scripts')
    if scripts_path not in sys.path:
        sys.path.append(scripts_path)
    
    
    
def endDialog(error=None):
    if error:
        cmds.confirmDialog(title='Failure',
                           message=f'{error}',
                           messageAlign='center')
    else:
        cmds.confirmDialog(title='Install Complete',
                        message='''The alembic export tools have been installed.
Look for the menu on the top bar.
No restart necessary.''',
                        button=['OK'])

