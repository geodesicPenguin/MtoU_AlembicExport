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
        if min or max is None:
            min = cmds.playbackOptions(q=1, min=1)
            max = cmds.playbackOptions(q=1, max=1)
            self.framerange = f'{min} {max}'
        else: self.framerange = f'{min} {max}'
        
        return self.framerange        
    
    
    def getExportSets(self):
        sets = cmds.ls(f'::*{EXPORT_SET_NAME}*', sets=1)
        
        if not sets:
            cmds.error(f'No valid sets were found. Sets with the phrase {EXPORT_SET_NAME} are needed.', noContext=1)
    
        self.objectsForExport = sets
        
        return self.objectsForExport
    
    
    def getSelected(self):
        selection = cmds.ls(sl=1)
        if not selection:
            cmds.error('Nothing is selected for export.', noContext=1)
        if cmds.filterExpand(selection, selectionMask=31):
            cmds.error('Selecting components is forbidden.', noContext=1)
            
        self.objectsForExport = selection
        
        return self.objectsForExport
    
    
    def setFilepath(self, filepath):
        path = os.path.normpath(filepath)
        fixedPath = path.replace('\\','/')
        self.filepath = fixedPath
        
        return self.filepath

            
    def duplicateObjects(self):
        cmds.select(self.objectsForExport, replace=1)
        duplicates = cmds.duplicate(returnRootsOnly=1, upstreamNodes=1, name=DUPLICATE_OBJECT_NAME)
        self.exportObjects = duplicates
    
    
    def exportFile(self): 
        objects = [f'-root {obj}' for obj in self.exportObjects]
        root = ' '.join(objects)
        job = f'{root} -framerange {self.framerange} {DEFAULT_ABC_ARGS} -file {self.filepath}'
        
        exportCommand = f'AbcExport -j "{job}"'
        mel.eval(exportCommand)
        
        
    def deleteDuplicateObjects(self):
        cmds.delete(self.exportObjects)
        
        
    @classmethod
    def exportSelection(cls, filepath, startFrame = None, endFrame = None):
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
        exporter = cls()
        exporter.setFramerange(startFrame, endFrame)
        exporter.getExportSets()
        exporter.setFilepath(filepath)
        exporter.duplicateObjects()
        exporter.exportFile()
        exporter.deleteDuplicateObjects()
        print(end='Export Completed')
        
        return exporter
        
    
    
    
    
    def completeDialog(self):
        pass
    
    def openFileLocation(self):
        pass