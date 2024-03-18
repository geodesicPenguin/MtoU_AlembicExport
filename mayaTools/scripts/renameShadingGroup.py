#renameShadingGroup.py

"""
Renames the selected shading group to match the connected material.
"""

import maya.cmds as cmds

def getSelection():
    """Finds the connected materials.
    The user may select the materials directly, or select any objects with the desired materials.
    
    Returns:
        selection : a list of the materials selected directly and/or thru mesh objects"""
    selection = []
    meshSelection = cmds.ls(sl=1, transforms=1)
    materialSelection = cmds.ls(sl=1, materials=1)
    
    if materialSelection:
        selection = materialSelection

    if meshSelection:
        for mesh in meshSelection:
            history = cmds.listHistory(mesh)
            shadingEngines = cmds.listConnections(history, type='shadingEngine')
            for shadingEngine in shadingEngines:
                selection = selection + cmds.listConnections(shadingEngine+'.surfaceShader')

    if not meshSelection and not materialSelection:
        answer = cmds.confirmDialog(message='No objects or material nodes selected, rename ALL shading groups in the scene?',button=['Yes','No'])
        if answer == 'No':
            cmds.error('Cancelled', noContext=1)
        else:
            undeletableMaterials = {'lambert1', 'standardSurface1', 'particleCloud1'}
            allMaterials = set(cmds.ls(materials=1))
            selection = list(allMaterials.difference(undeletableMaterials))

    return selection
        

def renameShadingGroup(materials):
    """Renames the shading groups to their respective materials.
    Args:
        materials : a list of materials"""
    editedShadingGroups = []
    for m in materials:
        shadingGroup = cmds.listConnections(m,type='shadingEngine')
        editedShadingGroups.append(cmds.rename(shadingGroup,f'{m}_SG'))
    return editedShadingGroups

def run():
    """A convenience function to run thru the tool.
    Meant for easy use within a shelf button or dropdown."""
    cmds.undoInfo(openChunk=1)
    selectedMaterials = getSelection()
    shadingGroups = renameShadingGroup(selectedMaterials)
    print('New shading groups:\n','\n'.join(shadingGroups))
    print(end=f'Successfully renamed {len(shadingGroups)} shading group(s)!')
    cmds.undoInfo(closeChunk=1)

    

