from maya import cmds, mel

def createAlembicExportMenu():
    mainWindow = mel.eval("$tmpVar = $gMainWindow")
    menuWidget = 'MtoU_alembicExportMenu'
    menuLabel = 'alembicExportTools'
    
    if cmds.menu(menuWidget, label=menuLabel, exists=1, parent=mainWindow):
        cmds.deleteUI(cmds.menu(menuWidget, e=1, deleteAllItems=1))
        
        
    menu = cmds.menu(menuWidget, label=menuLabel, parent=mainWindow, tearOff=1)
    
    # Shader tools
    cmds.menuItem(label='Shaders', divider=True)
    cmds.menuItem(label='Rename Shading Groups', command='import renameShadingGroup; renameShadingGroup.run()', annotation='Renames shading groups to their respective materials. The user may select the shaders or objects. Select nothing to rename all shading groups.')
    cmds.menuItem(label='Set Shaders to Face Sets', command='import setShadersTool; setShadersTool.SetShader()', annotation='Sets shaders to the faces of the selected objects. This allows the shaders to be connected in Unreal automatically.')
    
    # Export Tools
    cmds.menuItem(label='Export', divider=True)
    cmds.menuItem(label='Create Export Set', command='import alembicSelectionSet; alembicSelectionSet.run()', annotation='Makes a selection set with a specific naming convention for quick export.')
    cmds.menuItem(label='Export Alembic Cache', command='import alembicExportUI; alembicExportUI.AlembicExportUI().showWindow()', annotation='Opens the export window. Exports are based on selection or found export sets.')
    
    