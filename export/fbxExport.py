#fbxExport.py

import maya.cmds as cmds
import maya.mel as mel

from subprocess import Popen
import os

class fbxExport(): #make as class method?
    def __init__(self):
        self.getCameras()
        self.getCurrentScene()
        self.getWorkspace()
        self.fbxOutputFile()
        self.createOutputDirectory()
        self.fbxExport()
        self.completeWindow()

    def getCameras(self):
        shotCamKeyword = 'shot'
        selectedCamerasShapes = cmds.ls(sl=1, cameras=1)
        selectedCamerasTransforms = [obj for obj in cmds.ls(sl=1, transforms=1) if cmds.nodeType(cmds.listRelatives(obj, children=1)) == 'camera']
        selectedCameras = selectedCamerasShapes + selectedCamerasTransforms
        
        if not selectedCameras:
            shotCameras = cmds.ls(f'*{shotCamKeyword}*', cameras=1)
            if not shotCameras:
                cmds.error('Either rename a camera with the keyword "shot" or select a camera.', noContext=1)
            if len(shotCameras) > 1:
                confirm = cmds.confirmDialog(title='Multiple Cameras Found',message='Multiple cameras with naming convention found.\nExport All?',button=['Yes','No'])
                if confirm == 'No':
                    cmds.error('Either select the desired camera, or rename undesired cameras without keyword "shot".', noContext=1)
                self.exportCameras = shotCameras
                return 
        self.exportCameras = selectedCameras
        return 

    def getCurrentScene(self):
        sceneFile = cmds.file(q=1, sceneName=1, shortName=1)
        self.sceneName = os.path.splitext(sceneFile)[0]

    def getWorkspace(self):
        self.workspace = cmds.workspace(fullName=1)

    def fbxOutputFile(self):
        self.fbxFile = self.sceneName+'.fbx'

    def createOutputDirectory(self):
        outputFolder = os.path.join(self.workspace,'cache','fbx')
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        else: 
            confirm = cmds.confirmDialog(title='Overwrite?',message='Overwrite existing file?', button=['Yes','No'])
            if confirm == 'No':
                cmds.evalDeferred("print(end='Cancelled. Did not overwrite.')")
                cmds.error('Either save scene with new name or rename old exported file.',noContext=1)

        self.outputDirectory = os.path.normpath(os.path.join(outputFolder,self.fbxFile))

    def fbxExport(self):
        cmds.select(self.exportCameras)
        cmds.file(self.outputDirectory, force=1, options='v=0', type='FBX Export', preserveReferences=1, exportSelected=1)

    def completeWindow(self):
        confirm = cmds.confirmDialog(title='Export Succesful', message='Done!', button=['OK','Open Location'],defaultButton='OK',cancelButton='OK')
        if confirm == 'Open Location':
            self.openExportLocation()

    def openExportLocation(self):
        print(end=f'Opening {self.outputDirectory} ...')
        Popen(f'explorer /select,"{self.outputDirectory}"')