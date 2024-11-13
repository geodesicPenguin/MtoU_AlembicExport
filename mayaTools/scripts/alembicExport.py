"""
This file contains the base export functionality for Alembic files in Maya.
It includes methods for setting the frame range, setting the file path, duplicating objects,
deleting duplicate objects, and adding frame data to the Alembic file for Unreal Engine.
"""


import os
from maya import cmds, mel
import constants
import extraAlembicData

exportVars = constants.getConstants()
EXPORT_SET_NAME = exportVars['exportSetName']
DUPLICATE_OBJECT_NAME = exportVars['duplicateObjectName']
DEFAULT_ABC_ARGS = exportVars['defaultArgList']

class BaseExport():
    def __init__(self):
        pass
    
    def setFramerange(self, min=None, max=None):
        """Sets and returns the framerange."""
        if min or max is None:
            min = cmds.playbackOptions(q=1, min=1)
            max = cmds.playbackOptions(q=1, max=1)
            self.framerange = f'{min} {max}'
        else:
            self.framerange = f'{min} {max}'
        
        return self.framerange
    
    def setFilepath(self, filepath):
        """Returns the set filepath."""
        path = os.path.normpath(filepath)
        fixedPath = path.replace('\\', '/')
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
    
    def deleteDuplicateObjects(self):
        """Deletes the duplicate objects."""
        cmds.delete(self.exportObjects)
    
    def addFrameData(self):
        """Adds the start frame data to the alembic file for Unreal to read when importing."""
        extraAlembicData.writeStartFrame(self.filepath)
