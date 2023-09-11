#alembicSelectionSet.py
"""
Adds whatever is selected to a new selection set.
This selection set is used when it is time to export assets to Unreal in the form of Alembic files.
"""

#idea:
# in the menu, holding shift (option box) allows you to custom name the set
# IE; instead of EXPORT_SET it would be leftArm_EXPORT_SET, preview for the viewer to see too

import constants

from maya import cmds

exportVars = constants.getConstants()
EXPORT_SET_NAME = exportVars['exportSetName']

def userSelection():
    selection = cmds.ls(sl=1)
    if not selection:
        cmds.error('Select something first!',noContext=1)
        

def createSelectionSet():
    selectionSet = EXPORT_SET_NAME
    allSets = cmds.ls(sets=1)

    if selectionSet in allSets:
        confirm = cmds.confirmDialog(title='Alembic Selection Set', message=f'Found an existing "{selectionSet}" selection set. Overwrite?',button=['Yes','No'],cancelButton='No')
        if confirm == 'No':
            return
        else: cmds.delete(selectionSet)
    
    cmds.sets(name=selectionSet)
    print(end=f'{selectionSet} created.')
    
    return True


def run():
    userSelection()
    createSelectionSet()
