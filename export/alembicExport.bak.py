#alembicExport.py

from maya import cmds, mel
from subprocess import Popen
import os

class alembicExport():
    def __init__(self):
        pass


    def saveWarning(self):
        """Warning to save before continuing.
        Might delete.
        """
        pass 


    def getCurrentScene(self):
        """Returns the current scene name.
        """
        sceneFile = cmds.file(q=1, sceneName=1, shortName=1)
        self.sceneName = os.path.splitext(sceneFile)[0]
        return self.sceneName


    def getWorkspace(self):
        """Returns the current workspace.
        """
        self.workspace = cmds.workspace(fullName=1)
        return self.workspace
    
    
    def getFramerange(self):
        minTime = cmds.playbackOptions(q=1, min=1)
        maxTime = cmds.playbackOptions(q=1, max=1)
        self.framerange = f'{minTime} {maxTime}'
        
        return self.framerange


    def setOutputFilenames(self, filenames):
        self.alembicFiles = filenames
        
        return self.alembicFiles
    
    
    def setOutputdirectory(self, directory):
        self.outputDirectory = directory
        
        return self.outputDirectory
    

    def defaultOutputDirectory(self):
        """Returns the folder structure that will be created to house the alembic file(s).
        """
        self.outputDirectory = os.path.normpath(os.path.join(self.workspace,'cache','alembic',self.alembicFile))
        return self.outputDirectory
        
        
    def defaultOutputFile(self):
        """Returns the name of the alembic file to be created. The name is based off the scene name.
        TODO: Allow for multiple alembic files to be exported on a selection set basis. This will affect this method becuase we need individual names.
        """

        self.alembicFiles = self.sceneName+'.abc'
            
        return self.alembicFiles
        
        
    def multiFileExport(self):
        exportSetName = 'EXPORT_SET'
        self        
    
        
    def getSelection(self):
        """Returns the current selection.
        """
        self.selection = [cmds.ls(sl=1)]
        return self.selection
        

    def getExportSets(self, separate = False):
        """Returns the found export selection sets.
        These selection sets are pre-made user-defined sets containing what the user wants exported.
        They must be named 'EXPORT_SET'.
        """
        exportSetName = 'EXPORT_SET'
        selectionSets = cmds.ls(f'::{exportSetName}', sets=1)

        if not selectionSets:
            cmds.error(f'No valid sets were found. Sets with the phrase {exportSetName} are needed.', noContext=1)
            
        if separate:
            for set in selectionSets:
               self.selection  
            
        self.selection = [selectionSets]
        
        return self.selection


    def findObjects(self):
        """Finds objects for export. 
        If a selection is active, the selected objects will be exported.
        If nothing is selected, we look for the 'EXPORT_SET' selections sets.
        """
        if cmds.ls(sl=1):
            print(end='EXPORTING SELECTED OBJECTS!') 
            self.getSelection()
        else:
            print(end='EXPORTING OBJECTS FROM FOUND EXPORT SETS')
            self.getExportSets()


    def duplicateObjects(self):
        """Duplicates all objects being exported. Returns duplicate object names.
        This process takes place in order to mitigate a separate issue.
        Keeping namespaces on the objects prevents Unreal from properly recognizing the shading groups, making the suer reassign each shader all over again.
        Since namespaces are removed, the shaders connect automatically, however the alembic exporter fails if any object shares a name.
        """
        cmds.select(self.selection, replace=1)
        duplicateObjects = cmds.duplicate(returnRootsOnly=1, upstreamNodes=1, name='PLACEHOLDER')
        self.exportObjects = cmds.ls(duplicateObjects, long=1)
        
        return self.exportObjects


    def overwriteWarning(self):
        """Asks the user if it is OK to replace a file that already exists."""
        if os.path.exists(self.outputDirectory):
            confirm = cmds.confirmDialog(title='File Found!', message='Overwrite existing file?',button=['Yes','No','Open Location'])
            if confirm == 'No':
                cmds.error('Cancelled', noContext=1)
            if confirm == 'Open Location':
                self.openExportLocation()
                cmds.evalDeferred("print(end='Export stopped.')")
                cmds.error('Cancelling current export.', noContext=1)


    def combinedFileExport(self):
        """Creates the job arguments to export the alembic file(s).
        """
        # Objects
        objectRoots = [f'-root {obj}' for obj in self.exportObjects]
        rootArg = ' '.join(objectRoots)

        # Default Arguments
        defaultArgs = '-stripNamespaces -uvWrite -writeFaceSets -writeVisibility -autoSubd -writeUVSets -wholeFrameGeo -worldSpace -dataFormat ogawa'
        completeArgString = f'-framerange {self.framerange} {defaultArgs} {rootArg} -file {self.alembicFile}'

        cmds.AbcExport(jobArg = completeArgString)

        self.deleteDuplicateObjects()
        
        
    def separateFileExport(self):
        jobs = []
        defaultArgs = '-stripNamespaces -uvWrite -writeFaceSets -writeVisibility -autoSubd -writeUVSets -wholeFrameGeo -worldSpace -dataFormat ogawa'
        for object in self.exportObjects:
            job = f'-root {object} -framerange {self.framerange} {defaultArgs} -file {self.SPECIFIC_NAME_FOR_OBJECT_FOR_FILE}'
            jobs.append(job)
            
        commandString = ['AbcExport']
        commandString.extend(f'-j "{job}"' for job in jobs)
        exportCommand = " ".join(commandString)
        mel.eval(exportCommand)
        
        

    def deleteDuplicateObjects(self):
        """This deletes all duplicate objects."""
        cmds.delete(self.exportObjects)


    def completeWindow(self):
        """Tells the user the job is complete, with a few options pertaining to the file.
        """
        confirm = cmds.confirmDialog(title='Export Succesful', message=f'Exported to:\n{self.outputDirectory}', button=['OK','Open Location'],defaultButton='OK',cancelButton='OK')
        if confirm == 'Open Location':
            self.openExportLocation()


    def openExportLocation(self):
        """Opens the location of the file(s).
        """
        print(end=f'Opening {self.outputDirectory} ...')
        Popen(f'explorer /select,"{self.outputDirectory}"')
        
        
    @classmethod
    def defaultExport(cls):
        classInstance = cls()
        classInstance.getCurrentScene()
        classInstance.defaultOutputFile()
        classInstance.getWorkspace()
        classInstance.defaultOutputDirectory()
        classInstance.overwriteWarning()
        classInstance.findObjects()
        classInstance.duplicateObjects()
        classInstance.alembicExport()
        classInstance.completeWindow()
        return classInstance
    
    
        