#alembicImportUI.py

from assetImports import alembicImport

import unreal as ue
import sys
import os

try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
except:
    raise Exception('The needed UI module was not found.')

class AlembicImportUI(QWidget):
    def __init__(self) -> None:
        super(AlembicImportUI, self).__init__()
        
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle('Batch Shot Importer')
        self.setFixedSize(350, 800)
        self.setAcceptDrops(True) 
    
        self.uiWindow()
    
    
    def uiWindow(self):
        self.createMainWidget()
        
        
    def createMainWidget(self):
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
        
        # asset location (TBD if location is editable)
        assetLocationBox = QGroupBox('Asset Location Template:')
        assetLocationBox.setStyleSheet('QLabel {color: grey;}')
        mainLayout.addWidget(assetLocationBox)
        assetLocationLayout = QVBoxLayout(assetLocationBox)
        assetLocationLayout.setContentsMargins(15,15,15,15)
        
        assetLocationLabel = QLabel('/Game/Sequencer/S01/S01.abc')
        assetLocationLayout.addWidget(assetLocationLabel)
        
        # import abcs
        importButton = QPushButton('Import')
        importButton.clicked.connect(self.runImports)
        mainLayout.addWidget(importButton)
        
        
        
    
    def createFileListWidget(self):
        dragNdropBox = QGroupBox('Browse or drag Alembic and FBX files into the list:')
        dragNdropLayout = QVBoxLayout(dragNdropBox)
        dragNdropLayout.setContentsMargins(20,20,20,20)
        self.fileListWidget = QListWidget()
        self.fileListWidget.setFixedSize(250,500)
        self.fileListWidget.setStyleSheet('background-color: #202020;')
        dragNdropLayout.addWidget(self.fileListWidget)
        
        return dragNdropBox
        
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            
            
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            self.dragNdropListUpdate(urls)
    
    
    def dragNdropListUpdate(self, urls):
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
                #ue.log(item.data(itemDataRole))
            else:
                ue.log('Skipping duplicate files.')
                
                
    def fileChecker(self, filepath):
        ext = os.path.splitext(filepath)[-1]
        print(ext)
        if ext != '.fbx' and ext != '.abc':
            ue.log(f'Given file: {filepath} incorrect file type. (.fbx or .abc only)')    
            return False
        return True           

                
    def browseListUpdate(self):
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
        title = 'Select Animation Files for Import'
        fileFilter = 'Animation Files (*.fbx, *.abc)'
        startingDirectory = ue.Paths.get_project_file_path()
        selection = QFileDialog.getOpenFileNames(self,
                                                title,
                                                startingDirectory,
                                                fileFilter)[0]
        return selection

    def runImports(self):

        files = self.getFiles()
        
        self.setAlembicImportTask()
        self.setFbxImportTask()
        for file in files:
            if '.abc' in file:
                self.alembicImport(file)
            if '.fbx' in file:
                print('FBX import not supported yet')
                
        self.alembicTask.runTasks()
        #self.fbxTask.runTasks()

        
        
    def importLocation(self, file):
        fixedLocation = '/Game/Sequencer'
        shot = os.path.split(file)[-1].split('_')[0]
        if 'S' not in shot:
            raise Exception(f'{file} does NOT have the correct naming convention. IE: S03_V001_Mark.abc')
        importFolder = fixedLocation+'/'+shot

        return importFolder 
        
        
    def getFiles(self):
        listItems = [self.fileListWidget.item(x).data(Qt.UserRole+1) for x in range(self.fileListWidget.count())]
        return listItems
            
            
    def setAlembicImportTask(self):
        self.alembicTask = alembicImport.AlembicImportTask()


    def alembicImport(self,file):
        importFolder = self.importLocation(file)
        self.alembicTask.setTaskQueue(file, importFolder)


    def setFbxImportTask(self):
        pass
        
        
        
    
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