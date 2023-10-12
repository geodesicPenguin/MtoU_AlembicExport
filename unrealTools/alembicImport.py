#alembicImport.py

import unreal as ue
import os 

class AlembicImportTask():
    def __init__(self):
        self.queuedTasks = {}
            
    
    
    def setTaskQueue(self, files, importFolder=None, importType = ue.AlembicImportType.GEOMETRY_CACHE, scale = [1,1,1], rotate = [-90,0,0]):
        """Adds to the queue for all the task objects needed for each file being imported.

        Args:
            files : The filepaths for the desired imported files
            importFolder : The UE folder to import the files to.
            importType : Defaults to ue.AlembicImportType.GEOMETRY_CACHE
            scale : The scale of the imported objects.
            rotate : The rotation of the imported objects.

        Returns:
            self.queuedTasks: The list of all the tasks added.
        """
        if not isinstance(files, list): files = [files] # If importing one file, we make a list out of it to coincide with the following code.
        
        for file in files:
            assetName = os.path.splitext(os.path.basename(file))[0]
            if importFolder is None:
                importFolder = '/Game/'
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
            task.options = self.setOptions(importType, scale, rotate, file)
        
            self.queuedTasks[assetName] = task
        
        return self.queuedTasks
    
    
    def getTaskQueue(self):
        return self.queuedTasks
    
    
    def setAssetPath(self, assetDirectory, assetName): # make this generic for anyone to edit
        """Creates a formatted directory where the asset will be imported.

        Args:
            assetDirectory : The directory to import to.
            assetName : The name of the imported asset.

        Returns:
            assetPath : The resulting joined directory of the directory and asset name.
        """
        assetPath = f'{assetDirectory}/{assetName}'
        if '/Game/' not in assetPath:
            assetPath = f'/Game/{assetPath}'
            
        formattedAssetPath = os.path.normpath(assetPath)
        
        return formattedAssetPath
    
    
    def setOptions(self, importType, scale, rotate, file):
        """The options for the import tasks. 
        All tasks recieve the same options, except for their start frame.
        
        Returns:
            options : The import settings object.
        """
        options = ue.AbcImportSettings()
        
        options.set_editor_property('import_type', importType)
        if importType == ue.AlembicImportType.GEOMETRY_CACHE:
            options.geometry_cache_settings = self.setAbcGeometryCacheSettings()
            
        options.conversion_settings = self.setConversionSettings(scale, rotate)
        options.material_settings = self.setMaterialSettings()
        options.sampling_settings = self.setSamplingSettings(file)
        
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
    
    
    def setConversionSettings(self, scale = [1,1,1], rotate = [90,0,0]): 
        """The settings for the transforms.
        
        Args:
            scale : A list of the three axes (x,y,z) that affect the scale.
            rotate : A list of the three axes (x,y,z) that affect the rotation.

        Returns:
            conversionSettings : The settings object for the transforms.
        """
        conversionSettings = ue.AbcConversionSettings()

        axes = ['x', 'y', 'z']
        
        scaleVector = dict(zip(axes, scale))
        scaleSettings = ('scale', ue.Vector(**scaleVector))
        conversionSettings.set_editor_property(*scaleSettings)
                
        rotationVector = dict(zip(axes, rotate))
        rotationSettings = ('rotation', ue.Vector(**rotationVector))
        conversionSettings.set_editor_property(*rotationSettings)
        
        return conversionSettings
    
    
    def setAbcGeometryCacheSettings(self):
        """The settings used when importing the asset as a gemoetry cache.

        Returns:
            gemoetryCacheSettings: The settings object for the geometry cache.
        """
        geometryCacheSettings = ue.AbcGeometryCacheSettings()
        
        properties = {
            'flatten_tracks' : True,
        }
        
        geometryCacheSettings.set_editor_properties(properties)
        
        return geometryCacheSettings
    
    
    def setSamplingSettings(self, file):
        """The settings for setting up the duration and step of the animation.
        
        Args:
            file : The file to read data from.

        Returns:
            samplingSettings: The settings object for the frame sampling.
        """
        samplingSettings = ue.AbcSamplingSettings()
        
        startFrame = self._getStartFrameFromFile(file)
        
        properties = {
            'frame_start' : startFrame
        }
        
        samplingSettings.set_editor_properties(properties)
        
        return samplingSettings
    
    
    @staticmethod
    def _getStartFrameFromFile(file):
        """Reads the alembic file for the start frame.
        
        Args:
            file : The file to read data from.

        Returns:
            startFrameNumber: The frame the animation will start on. If no frame is found, due to the alembic file not containing the data exported thru Maya, defaults to 0.
        """
        with open(file, 'rb') as f:
            frameNumberLine = str(f.readlines()[-1])
            
            if 'frame_start' not in frameNumberLine:
                ue.log(f'{file} does not contain animation start frame data. Alembic file was not created with the Maya exporter intended for this tool. Defaulting start frame to 0.')
                return 0
            
            frameNumberLine = frameNumberLine.replace("'","").split("=")[-1]
            startFrameNumber = float(frameNumberLine)
        
        return startFrameNumber
    
    
    def runTasks(self):
        """Runs the tasks found within the task queue.
        """
        taskNames = list(self.queuedTasks.keys())
        taskQueue = list(self.queuedTasks.values())
        print('#'*10, f'TASK COUNT: {len(taskQueue)}','', 'ASSETS:',  *taskNames, '#'*10, sep='\n')
        
        ue.AssetToolsHelpers.get_asset_tools().import_asset_tasks(taskQueue)
        
        
    @classmethod
    def runImports(cls, files, importFolder=None, importType = ue.AlembicImportType.GEOMETRY_CACHE, scale = [1,1,1], rotate = [-90,0,0]):
        """Convenience function to set queue and import files in one function.

        Args:
            files : The filepaths for the desired imported files
            importFolder : The UE folder to import the files to.
            importType : Defaults to ue.AlembicImportType.SKELETAL, future versions will have geometry cache and static mesh.
            scale : The scale of the imported objects.
            rotate : The rotation of the imported objects.

        Returns:
            importer : The AlembicImportTask object.
        """
        importer = cls()
        importer.setTaskQueue(files, importFolder, importType, scale, rotate)
        importer.runTasks()
        
        return importer
        
    
        