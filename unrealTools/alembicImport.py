#alembicImport.py

# crashes if the asset path has too many / ie: Game//Sequencer

import unreal as ue
import os 

class AlembicImportTask():
    def __init__(self):
        self.tasks = {}

    def fileCheck(self, files):
        fileCheck = {file : os.path.exists(file) for file in files}
        # make it so whatveer files dont excist, 
        # ask the user if they want to remove it from the file list
        # also mmake this a conveniece function somewhere else. Not this file
            
    
    
    def setTaskQueue(self, files, importFolder=None):
        if not isinstance(files, list): files = [files]
        for file in files:
            assetName = os.path.splitext(os.path.split(file)[1])[0]
            if importFolder is None:
                importFolder = '/Game/Sequencer'
                assetPath = self.setAssetPath(importFolder, assetName)
            else:
                assetPath = importFolder
            
            task = ue.AssetImportTask()
            
            properties = {
                'filename'         : file,
                'destination_path' : assetPath,
                'destination_name' : assetName,
                'automated'        : True,
                'save'             : True
            }
            
            task.set_editor_properties(properties)
            task.options = self.setOptions()
        
            self.tasks[assetName] = task

            
        return list(self.tasks.values())
    
    
    def getTaskQueue(self):
        return self.tasks
    
    
    def setAssetPath(self, assetDirectory, assetName): # make this to be like what Jack gave
        assetPath = f'{assetDirectory}/{assetName}'
        if '/Game/' not in assetPath:
            assetPath = f'/Game/{assetPath}'
        return assetPath
    
    
    def setOptions(self):
        """The options for the import tasks. 
        This is a convenience function. 
        All tasks added per class instance will recieve these import options.
        """
        options = ue.AbcImportSettings()
        
        options.set_editor_property('import_type', ue.AlembicImportType.SKELETAL)
        options.conversion_settings = self.setConversionSettings()
        options.material_settings = self.setMaterialSettings()
        
        return options
        
        
    def setConversionSettings(self):
        """The settings for conversion.

        Returns:
           conversionSettings : The settings object needed for the AbcImportSettings object.
        """
        conversionSettings = ue.AbcConversionSettings()
        
        return conversionSettings
    
    
    def setCompressionSettings(self):
        """Potentially not needed. Added for future use-case.

        Returns:
            compressionSettings : The settings object needed for the AbcImportSettings object.
        """
        compressionSettings = ue.AbcCompressionSettings()
        
        return compressionSettings
    
    
    def setMaterialSettings(self):
        """The settings for the materials.

        Returns:
            materialSettings : The settings object needed for the AbcImportSettings object.
        """
        materialSettings = ue.AbcMaterialSettings()
        materialSettings.set_editor_property('find_materials', True)
        
        return materialSettings
    
    def setConversionSettings(self):
        conversionSettings = ue.AbcConversionSettins()

        #scaleSettings = ('scale', ue.Vector(x=1,y=-1,z=1))
        rotationSettings = ('rotation', ue.Vector(x=-90,y=0,z=0))
        conversionSettings.set_editor_property(*rotationSettings)
    
    
    def runTasks(self):
        print(self.tasks,sep='\n')
        taskNames = list(self.tasks.keys())
        taskQueue = list(self.tasks.values())
        print('',f'TASK COUNT: {len(taskQueue)}','', 'ASSETS:',  *taskNames, sep='\n')
        ue.AssetToolsHelpers.get_asset_tools().import_asset_tasks(taskQueue)
        
        
    @classmethod
    def runImports(cls, files, importFolder='/Game/Sequencer'):
        importer = cls()
        importer.setTaskQueue(files, importFolder)
        
        return importer
        
    
        