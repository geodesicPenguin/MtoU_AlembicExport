#setShadersTool.py

"""
Sets shaders to objects' faces for the Unreal Alembic Cache.
"""

import maya.cmds as cmds

class SetShader:
    def __init__(self) -> None:
        print(end='Setting shader to face components. . . ')
        cmds.undoInfo(openChunk=1, chunkName='Shader_Set_Action')
        self.getGeometry()
        for self.geometry in self.selectedGeometry:
            self.getShape()
            
            try:
                self.getAssignedShader()
            except RuntimeError as e:
                print(e)
                continue
            
            self.applyShaders()
        cmds.undoInfo(closeChunk=1, chunkName='Shader_Set_Action')
        print(end='Shaders set successfully!')


    def getGeometry(self):
        """Get the selected geometry objects"""
        selection = cmds.ls(sl=1, exactType='transform')
        print(selection)
        if len(selection) <1:
            cmds.error('Select some geometry', noContext=1)

        self.selectedGeometry = selection

    def getShape(self):
        """Get the accompanying shape node to the selected transform."""
        self.shape = cmds.listRelatives(self.geometry, shapes=1)[0]

    def getAssignedShader(self):
        """Get the shader assigned to the given objects."""
        history = cmds.listHistory(self.geometry)
        shadingEngines = cmds.listConnections(history, type='shadingEngine')
        if len(shadingEngines) >1:
            print('Shading groups found:', shadingEngines, sep='\n')
            cmds.error(f'Multiple shading engines already attached to {self.geometry} - skipping! (Nothing more needs to be done to this object)\n', noContext=1)
        shader = shadingEngines[0]

        self.shader = shader

    def setInitialShaderToMesh(self):
        """To set the shader to the faces, we need an alternate shader on the mesh.
        The default standardSurface is assigned."""
        cmds.select(self.geometry, r=1)
        cmds.sets(e=1, forceElement='initialShadingGroup')
        print(end='SET INITIAL!\n'+self.geometry)


    def setShaderToFaces(self):
        """Set a shader to the faces of a mesh object."""
        meshFaces = f'{self.geometry}.f[*]'
        cmds.select(meshFaces,r=1)
        cmds.sets(e=1, forceElement=self.shader)
        print(end='SET MATERIAL!\n'+meshFaces)

    def applyShaders(self):
        """Applies mesh and object shaders. Must be in the afformentioned order.
        Must also do a viepowrt refresh."""
        self.setInitialShaderToMesh()
        self.setShaderToFaces()
        cmds.ogs(reset=1)



