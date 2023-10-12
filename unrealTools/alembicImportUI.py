#alembicImportUI.py


import unreal as ue
import sys
import os

moduleDir = os.path.dirname(__file__)

try:
    import alembicImport
except:
    if moduleDir not in sys.path:
        sys.path.append(moduleDir)
        import alembicImport
try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
except:
    import site
    from subprocess import call
    
    unrealSitePackages = site.getsitepackages()[0]
    
    print('Installing PySide2 at:', unrealSitePackages, end='\n')
    call(['pip','install','PySide2', '--target',unrealSitePackages])

    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
        


class AlembicImportUI(QWidget):
    def __init__(self) -> None:
        super(AlembicImportUI, self).__init__()
        
        self.UI_SETTINGS = ('Unreal', 'AlembicImportUISettings')
        
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle('Alembic Importer')
        self.setGeometry(QRect(100,100, 350, 800))
        self.setAcceptDrops(True) 
    
        self.uiWindow()
    
        self.loadSettings()
        
        
    def uiWindow(self):
        """Creates the contents of the window.
        """
        # main layout
        mainWidget = QGroupBox(self)
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setContentsMargins(30,30,30,30)
        mainLayout.setSpacing(20)
        
        
        # browse button
        browseButton = QPushButton('Browse')
        browseButton.clicked.connect(self.browseListUpdate)
        browseButton.setFixedSize(500,30)
        mainLayout.addWidget(browseButton)
        
        
        # file list 
        fileList = self.createFileListWidget()
        mainLayout.addWidget(fileList)
        
        
        # asset location
        assetLocationBox = QGroupBox('Import Location:')
        assetLocationBox.setStyleSheet('QLabel {color: grey;}')
        mainLayout.addWidget(assetLocationBox)
        assetLocationLayout = QVBoxLayout(assetLocationBox)
        assetLocationLayout.setContentsMargins(15,15,15,15)
        
        
        currentFolder = self.currentContentBrwoserFolder()
        self.assetLocationText = QLineEdit(currentFolder)
        self.assetLocationText.setToolTip('Defaults to the currently active folder in the content browser.')
        assetLocationLayout.addWidget(self.assetLocationText)
        
        # import type
        importTypeBox = QGroupBox('Import Type')
        mainLayout.addWidget(importTypeBox)
        importTypeLayout = QHBoxLayout(importTypeBox)
        self.importTypeComboBox = QComboBox()
        importTypeBox.setContentsMargins(15,15,15,15)
        self.importTypeComboBox.setStyleSheet('QComboBox {background-color: #4a4a4a;}')
        importTypeLayout.addWidget(self.importTypeComboBox)
        self.importTypeComboBox.addItems(['Geometry Cache', 'Skeletal'])
        
        
        # transforms
        transformsBox = QGroupBox('Transforms:')
        transformsBox.setStyleSheet('QGroupBox {background-color: #4a4a4a;}')
        transformsBox.setToolTip('Set the scale and rotate settings.\nThe axes are as follows: X Y Z')
        mainLayout.addWidget(transformsBox)
        transformsLayout = QGridLayout(transformsBox)
        transformsLayout.setContentsMargins(30,30,30,30)
        
        scaleLabel = QLabel ('Scale:')
        
        self.scaleX = QDoubleSpinBox()
        self.scaleY = QDoubleSpinBox()
        self.scaleZ = QDoubleSpinBox()
        
        self.scaleX.setValue(1); self.scaleX.setMinimum(-100); self.scaleX.setMaximum(100)
        self.scaleY.setValue(1); self.scaleY.setMinimum(-100); self.scaleX.setMaximum(100)
        self.scaleZ.setValue(1); self.scaleZ.setMinimum(-100); self.scaleX.setMaximum(100)
        
        for i,wgt in enumerate([scaleLabel, self.scaleX, self.scaleY, self.scaleZ]):
            transformsLayout.addWidget(wgt, 0, i)
            
        rotateLabel = QLabel('Rotate:')
        
        self.rotateX = QDoubleSpinBox()
        self.rotateY = QDoubleSpinBox()
        self.rotateZ = QDoubleSpinBox()
        
        self.rotateX.setMinimum(-360); self.rotateX.setMaximum(360)
        self.rotateY.setMinimum(-360); self.rotateX.setMaximum(360)
        self.rotateZ.setMinimum(-360); self.rotateX.setMaximum(360)
        
        for i,wgt in enumerate([rotateLabel, self.rotateX, self.rotateY, self.rotateZ]):
            transformsLayout.addWidget(wgt, 1, i)
        
        
        # import abcs
        importButton = QPushButton('Import')
        importButton.clicked.connect(self.runAndClose)
        mainLayout.addWidget(importButton)
        
    
    def createFileListWidget(self):
        """Creates the File List Widget.

        Returns:
            dragNdropBox : The widget with all the file list contents.
        """
        dragNdropBox = QGroupBox('Browse or drag Alembic files into the list:')
        dragNdropLayout = QVBoxLayout(dragNdropBox)
        dragNdropLayout.setContentsMargins(20,20,20,20)
        self.fileListWidget = QListWidget()
        self.fileListWidget.itemDoubleClicked.connect(self.removeFileListItem)
        self.fileListWidget.setFixedSize(250,300)
        self.fileListWidget.setStyleSheet('background-color: #202020;')
        dragNdropLayout.addWidget(self.fileListWidget)
        
        return dragNdropBox
    
    
    def removeFileListItem(self):
        """Removes the selected file from the list when double clicked.
        """
        selectedItem = self.fileListWidget.currentItem()
        selectedItemIndex = self.fileListWidget.row(selectedItem)
        self.fileListWidget.takeItem(selectedItemIndex)
    
    
    def saveSettings(self):
        """Saves the UI settings for next use.
        """
        settings = QSettings(*self.UI_SETTINGS)
        
        # window position settings
        position = self.pos()
        settings.setValue('windowPositionSettings', position)
        
        # import type settings
        importType = self.importTypeComboBox.currentIndex()
        settings.setValue('importTypeSettings', importType)
        
        # transform (conversion) settings
        scale = [s.value() for s in [self.scaleX, self.scaleY, self.scaleZ]]
        rotate = [r.value() for r in [self.rotateX, self.rotateY, self.rotateZ]]
        settings.setValue('conversionSettings', (scale, rotate))
        
        # perhaps add in last browsed folder as a setting
    
    
    def loadSettings(self):
        """Loads the UI settings into the window.
        """
        settings = QSettings(*self.UI_SETTINGS)
        
        windowPositionSettings = settings.value('windowPositionSettings', QPoint(300, 300))
        self.move(windowPositionSettings)
        
        importTypeSettings = settings.value('importTypeSettings', 0)
        self.importTypeComboBox.setCurrentIndex(importTypeSettings)
        
        scaleSettings, rotateSettings = settings.value('conversionSettings', ([1,1,1], [90,0,0]))
        
        self.scaleX.setValue(scaleSettings[0])
        self.scaleY.setValue(scaleSettings[1])
        self.scaleZ.setValue(scaleSettings[2])
        
        self.rotateX.setValue(rotateSettings[0])
        self.rotateY.setValue(rotateSettings[1])
        self.rotateZ.setValue(rotateSettings[2])

        
    def closeEvent(self, event):
        """Sends the signal to save the settings before closing the window.
        """
        self.saveSettings()
        event.accept()
    
        
    def dragEnterEvent(self, event):
        """Functionality for the File List Widget to recieve files by dragging them in. 
        """
        if event.mimeData().hasUrls():
            event.accept()
            
            
    def dropEvent(self, event):
        """Functionality for the File List Widget to update with the dropped files.
        """
        urls = event.mimeData().urls()
        if urls:
            self.dragNdropListUpdate(urls)
    
    
    def dragNdropListUpdate(self, urls):
        """Updates the list with the files.

        Args:
            urls : The filepaths of the incoming files.
        """
        filesDict = {}
        if urls:
            for url in urls:
                filepath = url.toLocalFile()
                if not self.fileChecker(filepath):
                    continue
                filename = os.path.split(filepath)[1]
                filesDict[filepath] = filename
   
        
   
        for filePath, fileName in filesDict.items():
            if not self.fileListWidget.findItems(fileName, Qt.MatchWildcard):
                item = QListWidgetItem(fileName)
                itemDataRole = Qt.UserRole+1
                item.setData(itemDataRole, filePath)
                self.fileListWidget.addItem(item)
            else:
                ue.log('Skipping duplicate files.')
                
                
    def fileChecker(self, filepath):
        """Checks files for the Alembic extension.
        True if Alembic, False if not.

        Args:
            filepath : the filepath
        """
        ext = os.path.splitext(filepath)[-1]
        if ext != '.abc':
            ue.log(f'{filepath} is an incorrect file type. Alembic files only.')    
            
            return False
        
        return True           

                
    def browseListUpdate(self):
        """Updates the File List Widget after browsing for new items.
        """
        filesDict = {}
        filepaths = self.browseDialog()
        print(filepaths)
        for filepath in filepaths:
            filename = os.path.split(filepath)[-1]
            filesDict[filepath] = filename
            
        for filePath, fileName in filesDict.items():
            if not self.fileListWidget.findItems(fileName, Qt.MatchWildcard):
                item = QListWidgetItem(fileName)
                itemDataRole = Qt.UserRole+1
                item.setData(itemDataRole, filePath)
                self.fileListWidget.addItem(item)
            else:
                ue.log('Skipping duplicate files.')
        
    
    def browseDialog(self): 
        """The file browser.
        """
        title = 'Select Animation Files for Import'
        fileFilter = 'Animation Files (*.abc)'
        startingDirectory = ue.Paths.get_project_file_path()
        selection = QFileDialog.getOpenFileNames(self,
                                                title,
                                                startingDirectory,
                                                fileFilter)[0]
        
        return selection

        
    def currentContentBrwoserFolder(self):
        """Returns the current content browser folder.
        """
        currentFolder = ue.EditorUtilityLibrary.get_current_content_browser_path()
        
        return currentFolder
    
        
    def getImportLocation(self):
        """Looks at the import location text box for where to import to.
        """
        importFolder = self.assetLocationText.text()
        if importFolder == '':
            raise ValueError('No import folder given.')

        return importFolder 
        
        
    def getFiles(self):
        """Looks at the File List Widget for all the given files.
        """
        listItems = [self.fileListWidget.item(x).data(Qt.UserRole+1) for x in range(self.fileListWidget.count())]
        
        return listItems
    
    
    def getImportType(self):
        """Gets the user-specified import type.
        """
        importTypeIndex = self.importTypeComboBox.currentIndex()
         
        if importTypeIndex == 0:
            importType = ue.AlembicImportType.GEOMETRY_CACHE
        if importTypeIndex == 1:
            importType = ue.AlembicImportType.SKELETAL
            
        return importType
    
    
    def getScale(self):
        """Gets the user-specified scale values.
        """
        scale = [s.value() for s in [self.scaleX, self.scaleY, self.scaleZ]]
        
        return scale
    
    
    def getRotate(self):
        """Gets the user-specified rotation values.
        """
        rotate = [r.value() for r in [self.rotateX, self.rotateY, self.rotateZ]]
        
        return rotate
            

    def runTaskQueue(self):
        """Creates the import task queue, adds the user-given data and imports.
        """
        files = self.getFiles()
        importFolder = self.getImportLocation()
        importType = self.getImportType()
        scale = self.getScale()
        rotate = self.getRotate()
        
        alembicImport.AlembicImportTask.runImports(files=files, 
                                                   importFolder=importFolder,
                                                   importType=importType,
                                                   scale=scale, 
                                                   rotate=rotate)
        
    def runAndClose(self):
        """Runs the task queue and closes the window.
        """
        self.runTaskQueue()
        self.close()



    
app = None
if not QApplication.instance():
    app = QApplication(sys.argv)
    
qApp.setStyleSheet("""
QWidget {
    background-color: #282828;
    color: white;
    border: none;
}

QToolBar {
    background-color: #282828;
    border: none;
}

QToolButton {
    background-color: transparent;
    border: none;
    padding: 4px;
    margin: 4px;
    color: white;
}

QToolButton:hover {
    background-color: #606060;
}

QToolButton:pressed {
    background-color: #404040;
}

QLabel {
    color: white;
}

QLineEdit {
    background-color: #444444;
    color: white;
    border: 1px solid #606060;
    border-radius: 3px;
    padding: 3px;
}

QPushButton {
    background-color: #606060;
    color: white;
    border: none;
    padding: 6px;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #909090;
}

QPushButton:pressed {
    background-color: #707070;
}
""")


if __name__ == '__main__':
    window = AlembicImportUI()
    window.show()