#
#
#
#
#
#single

import os
from maya import cmds, mel
import constants

exportVars = constants.getConstants()
EXPORT_SET_NAME = exportVars['exportSetName']
DUPLICATE_OBJECT_NAME = exportVars['duplicateObjectName']
DEFAULT_ABC_ARGS = exportVars['defaultArgList']

class SingleExport():
    def __init__(self):
        pass
    
    def setFramerange(self, min = None, max = None):
        """Sets and returns the framerange.
        """
        if min or max is None:
            min = cmds.playbackOptions(q=1, min=1)
            max = cmds.playbackOptions(q=1, max=1)
            self.framerange = f'{min} {max}'
        else: self.framerange = f'{min} {max}'
        
        return self.framerange        
    
    
    def getExportSets(self):
        """Returns the found export sets. Errors if none found.
        """
        sets = cmds.ls(f'::*{EXPORT_SET_NAME}*', sets=1)
        
        if not sets:
            cmds.error(f'No valid sets were found. Sets with the phrase {EXPORT_SET_NAME} are needed.', noContext=1)
    
        self.objectsForExport = sets
        
        return self.objectsForExport
    
    
    def getSelected(self):
        """Returns the selection.
        """
        selection = cmds.ls(sl=1)
        if not selection:
            cmds.error('Nothing is selected for export.', noContext=1)
        if cmds.filterExpand(selection, selectionMask=31):
            cmds.error('Selecting components is forbidden.', noContext=1)
            
        self.objectsForExport = selection
        
        return self.objectsForExport
    
    
    def setFilepath(self, filepath):
        """Returns the set filepath.
        """
        path = os.path.normpath(filepath)
        fixedPath = path.replace('\\','/')
        self.filepath = fixedPath
        
        return self.filepath

            
    def duplicateObjects(self):
        """Duplicate objects are used for the export.
        This prevents export failure due to identical object names, as namespaces are also removed.
        When importing to Unreal, the objects will appear named as the DUPLICATE_OBJECT_NAME constant followed by a number.
        This is a negligible edit and does not affect anything other than the name.
        """
        cmds.select(self.objectsForExport, replace=1)
        duplicates = cmds.duplicate(returnRootsOnly=1, upstreamNodes=1, name=DUPLICATE_OBJECT_NAME)
        self.exportObjects = duplicates
    
    
    def exportFile(self): 
        """Creates the export string.
        Exports all objects found in each export set into one file.
        Runs the export as a mel command.
        """
        objects = [f'-root {obj}' for obj in self.exportObjects]
        root = ' '.join(objects)
        job = f'{root} -framerange {self.framerange} {DEFAULT_ABC_ARGS} -file {self.filepath}'
        
        exportCommand = f'AbcExport -j "{job}"'
        mel.eval(exportCommand)
        
        
    def deleteDuplicateObjects(self):
        """Deletes the duplicate objects.
        """
        cmds.delete(self.exportObjects)
        
        
    @classmethod
    def exportSelection(cls, filepath, startFrame = None, endFrame = None):
        """Exports all selected objects to given filepath.
        """
        exporter = cls()
        exporter.setFramerange(startFrame, endFrame)
        exporter.getSelected()
        exporter.setFilepath(filepath)
        exporter.duplicateObjects()
        exporter.exportFile()
        exporter.deleteDuplicateObjects()
        print(end='Export Completed')
        
        return exporter
        
    @classmethod
    def exportSelectionSets(cls, filepath, startFrame = None, endFrame = None):
        """Exports all objects within the selection sets fo the given filepath.
        """
        exporter = cls()
        exporter.setFramerange(startFrame, endFrame)
        exporter.getExportSets()
        exporter.setFilepath(filepath)
        exporter.duplicateObjects()
        exporter.exportFile()
        exporter.deleteDuplicateObjects()
        print(end='Export Completed')
        
        return exporter
        
