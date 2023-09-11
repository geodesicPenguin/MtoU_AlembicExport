#
#
#
#
#
#combined

import os
from maya import cmds, mel
import constants

exportVars = constants.getConstants()
EXPORT_SET_NAME = exportVars['exportSetName']
DUPLICATE_OBJECT_NAME = exportVars['duplicateObjectName']
DEFAULT_ABC_ARGS = exportVars['defaultArgList']

class MultiExport():
    def __init__(self):
        self.exportDict = {}
        
    
    def setFramerange(self, min = None, max = None):
        if min or max is None:
            min = cmds.playbackOptions(q=1, min=1)
            max = cmds.playbackOptions(q=1, max=1)
            self.framerange = f'{min} {max}'
        else: self.framerange = f'{min} {max}'
        
        return self.framerange
    
    @staticmethod
    def findExportSets():
        sets = cmds.ls(f'::*{EXPORT_SET_NAME}*', sets=1)
        
        return sets
    
    def getExportSets(self):
        sets = self.findExportSets()
        
        if not sets:
            cmds.error(f'No valid sets were found. Sets with the phrase {EXPORT_SET_NAME} are needed.', noContext=1)
    
        self.exportSets = sets
        
        return self.exportSets
    
    
    def setExportDict(self):
        for set in self.exportSets:
            self.exportDict[set] = {'filepath' : None, 'exportObjects' : None}
        
        return self.exportDict
    
    
    def setFilepath(self, exportSet, filepath):
        path = os.path.normpath(filepath)
        fixedPath = path.replace('\\','/')
        self.exportDict[exportSet]['filepath'] = fixedPath
        
        return self.exportDict
        

    # def getObjects(self, exportSet, selected = False):
        """disabled for now.
        future functionality could happen where:
        The user makes specific selections and identifies them for
        multi export.
        this can happen later. for now just using the sets
        """
    #     if selected:
    #         selection = cmds.ls(sl=1)
    #     else:
    #         selection = exportSet
            
    #     self.selection = selection
        
    #     return self.selection
    
            
    def duplicateObjects(self):
        for set in self.exportSets: 
            cmds.select(set, replace=1)
            duplicates = cmds.duplicate(returnRootsOnly=1, upstreamNodes=1, name=DUPLICATE_OBJECT_NAME)
            self.exportDict[set]['exportObjects'] = duplicates
            
            
    def deleteDuplicateObjects(self):
        for set in self.exportSets:
            cmds.delete(self.exportDict[set]['exportObjects'])
    
    
    def exportFiles(self):
        jobs = []
        for set in self.exportDict: #it wonr actually be self.exportDict bc we need to dup the objs
            filepath = self.exportDict[set]['filepath'] #wont actually be this bc need to append dir
            objects = [f'-root {obj}' for obj in self.exportDict[set]['exportObjects']]
            root = ' '.join(objects)
            job = f'{root} -framerange {self.framerange} {DEFAULT_ABC_ARGS} -file {filepath}'
            jobs.append(job)
    
        melString = ['AbcExport']
        melString.extend(f'-j "{job}"' for job in jobs)
        exportCommand = ' '.join(melString)
        mel.eval(exportCommand)

    
    @classmethod
    def exportDefaultSelectionSets(cls, filepath, startFrame = None, endFrame = None):
        exporter = cls()
        exporter.setFramerange(startFrame, endFrame)
        exporter.getExportSets()
        exporter.setExportDict()
        for set in exporter.exportSets:
            exporter.setFilepath(set, filepath)
        exporter.duplicateObjects()
        exporter.exportFiles()
        exporter.deleteDuplicateObjects()
        print(end='Export Completed')
        
        return exporter
    
    @classmethod
    def exportSelectionSets(cls, exportSetsOutputDict, startFrame = None, endFrame = None): #{exportSetName : exportSetOutputLocation}
        exporter = cls()
        exporter.setFramerange(startFrame, endFrame)
        exporter.exportSets = [set for set in exportSetsOutputDict if cmds.objExists(set)]
        exporter.setExportDict()
        for set in exportSetsOutputDict:
            filepath = exportSetsOutputDict[set]
            exporter.setFilepath(set, filepath)
        exporter.duplicateObjects()
        exporter.exportFiles()
        exporter.deleteDuplicateObjects()
        print('FINISHED WITH THE PROCESS')
        
    
    # def exportSelectionSetsByName(cls, directory, startFrame = None, endFrame = None):
    #     exporter = cls()
    #     exporter.setFramerange(startFrame, endFrame)
    #     exporter.getExportSets()
    #     exporter.setExportDict()
    #     for set in exporter.exportSets:
    #         filepath = directory + '/' + set.replace(':','_')
    #         exporter.setFilepath(set, directory)
    #     exporter.duplicateObjects()
    #     exporter.exportFiles()
    #     exporter.deleteDuplicateObjects()
    #     print(end='Export Completed')
        
    #     return exporter
        
    
    def successInfo(self):
        """Put all info here related to exports.
        How many files
        what directory
        """
    
    def completeDialog(self):
        """Dialog to tell user the info.
        Directo info from successInfo into here
        Might not use this bc will be using dialog in UI
        """
    
    def openFileLocation(self):
        pass