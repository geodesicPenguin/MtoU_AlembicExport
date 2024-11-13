#constants.py

"""
To edit and query from constants.json

The constant variables below are as follows:
exportSetName -> The naming convention all the alembicExport tools use when looking for selection sets.
duplicateObjectName -> The name given to all objects when exported to the .abc file. Unimportant, but editable if desired.
defaultArgList -> The arguments for the alembic export. All default flags in the string are what works best in Unreal.
"""


import json
import os


fileDir = os.path.dirname(os.path.realpath(__file__))
CONSTANTS_FILE = os.path.join(fileDir, 'constants.json')
CONSTANTS = ['exportSetName', 'duplicateObjectName', 'defaultArgList']

# Do not edit these. If you want different values, edit the constants.json file.
DEFAULT_VALUES = ['abcExport', 
                  'PLACEHOLDER', 
                  '-stripNamespaces -uvWrite -writeFaceSets -writeVisibility -worldSpace -dataFormat ogawa']
        

def defaultConstants():
    for i in range(3):
        defaultFile = setConstant(CONSTANTS[i], DEFAULT_VALUES[i])
        
    return defaultFile


def setConstant(constantVariable, newValue):
    if constantVariable in CONSTANTS:
    
        with open(CONSTANTS_FILE) as f:
            fileInfo = json.load(f)
            
        fileInfo[constantVariable] = newValue
        
        with open(CONSTANTS_FILE, 'w') as f:
            json.dump(fileInfo, f, indent = 1)
            
    return fileInfo


def getConstants():

        with open(CONSTANTS_FILE) as f:
            fileInfo = json.load(f)
            
        return fileInfo
    
    
    