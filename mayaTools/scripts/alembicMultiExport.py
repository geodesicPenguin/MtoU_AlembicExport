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
        """Sets the framerange.
        """
        if min or max is None:
            min = cmds.playbackOptions(q=1, min=1)
            max = cmds.playbackOptions(q=1, max=1)
            self.framerange = f'{min} {max}'
        else: self.framerange = f'{min} {max}'
        
        return self.framerange
    
    @staticmethod
    def findExportSets():
        """Returns the export sets with the user-defined export set naming convention.
        This is a static method purely so it can be used in the UI.
        """
        sets = cmds.ls(f'::*{EXPORT_SET_NAME}*', sets=1)
        
        return sets
    
    def getExportSets(self):
        """Returns the found export sets. Errors if none found.
        """
        sets = self.findExportSets()
        
        if not sets:
            cmds.error(f'No valid sets were found. Sets with the phrase {EXPORT_SET_NAME} are needed.', noContext=1)
    
        self.exportSets = sets
        
        return self.exportSets
    
    
    def setExportDict(self):
        """Returns the export set dictionary.
        The export set dictionary defines data related to the set like so: 
        {export_set_name : {
            'filepath' : '...project/cache/alembic', 
            'exportObjects' : 'cube1'}
            }
        """
        for set in self.exportSets:
            self.exportDict[set] = {'filepath' : None, 'exportObjects' : None}
        
        return self.exportDict
    
    
    def setFilepath(self, exportSet, filepath):
        """Sets the filepath for the given export set.
        Returns the updated export set dictionary.
        """
        path = os.path.normpath(filepath)
        fixedPath = path.replace('\\','/')
        self.exportDict[exportSet]['filepath'] = fixedPath
        
        return self.exportDict
        
    
            
    def duplicateObjects(self):
        """Duplicate objects are used for the export.
        This prevents export failure due to identical object names, as namespaces are also removed.
        When importing to Unreal, the objects will appear named as the DUPLICATE_OBJECT_NAME constant followed by a number.
        This is a negligible edit and does not affect anything other than the name.
        """
        for set in self.exportSets: 
            cmds.select(set, replace=1)
            duplicates = cmds.duplicate(returnRootsOnly=1, upstreamNodes=1, name=DUPLICATE_OBJECT_NAME)
            self.exportDict[set]['exportObjects'] = duplicates
            
            
    def deleteDuplicateObjects(self):
        """Deletes the duplicate objects.
        """
        for set in self.exportSets:
            cmds.delete(self.exportDict[set]['exportObjects'])
    
    
    def exportFiles(self):
        """Creates the string of exports set by the user.
        Runs the export as a mel command.
        """
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
        """A sort of auto export function.
        Just define the filepath and all else is configured.
        """
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
    def exportSelectionSets(cls, exportSetsOutputDict, startFrame = None, endFrame = None):
        """Requires the exportSetsOutputDict.
        This dictionary defines user-specified data on what to export and where.
        It is formatted like so:
        {'#' : {
            {'enable_#' : True,
            'exportSet_#' : 'export_set_name',
            'output_# : 'save/to/this/filepath.abc'}
        }}
        """
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
        print(end='Export Completed')
        
