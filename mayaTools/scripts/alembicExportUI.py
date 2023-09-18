#alembicExportUI.py

"""
A UI to interact with all the settings of the alembic export tool I made.

The settings include:
    - What to export
    - Where to export 
    - The name(s) of the exported file(s)
"""


import os
from subprocess import Popen

from maya import cmds
from maya import OpenMayaUI as omui


import alembicSingleExport
import alembicMultiExport
import constants


from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance



class AlembicExportUI(QWidget):
    def __init__(self) -> None:
        super(AlembicExportUI, self).__init__()
        
        mayaPointerAddress = int(omui.MQtUtil.mainWindow())
        mayaMainWindow = wrapInstance(mayaPointerAddress, QWidget)
        self.UI_SETTINGS = ('Maya', 'AlembicExportUISettings')

        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)

        # Window settings
        self.setObjectName('alembicExportUiWindow')
        self.setWindowTitle('Export Alembic Animation')

        # Create the widgets
        self.mainUI()
        self.loadSettings()
        
        windowSizeAndPosition = QRect(50, 50, 500, 200)
        windowSizeAndPosition.moveCenter(mayaMainWindow.geometry().center())
        self.setGeometry(windowSizeAndPosition)
        
        
        # offset the show() function to the user. That way we can make a classmethod that opens preexisting versions of the window.
        #self.showWindow()
        
        
    def mainUI(self):
        master_lyt = QVBoxLayout(self)
        
        master_lyt.addWidget(self.menuBar())
        
        main_wgt = QGroupBox()
        master_lyt.addWidget(main_wgt)
        
        main_lyt = QVBoxLayout(main_wgt)
        
        main_lyt.addWidget(self.fileOutputOptionsUI())
        main_lyt.addWidget(self.exportOptionsUI())
        main_lyt.addWidget(self.confirmOptionsUI())
        
    
    def saveSettings(self):
        settings = QSettings(*self.UI_SETTINGS)
        
        settings.setValue('combinedFileCheckbox', self.combined_chk.isChecked())
        settings.setValue('exportLocation', self.outputDir_txt.text())
        
        
    def loadSettings(self):
        settings = QSettings(*self.UI_SETTINGS)
        
        combinedCheckboxValue = settings.value('combinedFileCheckbox', True)
        
        if not isinstance(combinedCheckboxValue, bool): # the bool was returning as a string, so I added this bandage code :P
            if combinedCheckboxValue == 'false':
                exportMethod = False
            if combinedCheckboxValue == 'true':
                exportMethod = True
        else: exportMethod = combinedCheckboxValue
        
        self.combined_chk.setChecked(exportMethod)
        self.exportOptions_wgt.setDisabled(exportMethod) 
        self.separate_chk.setChecked(not exportMethod)
        
        self.exportDir = settings.value('exportLocation', cmds.workspace(q=1, fullName=1))
        self.outputDir_txt.setText(self.exportDir)
        
        exportFilepath = os.path.join(self.exportDir, self.outputCombinedFilename())
        self.combinedFileOutput_txt.setText(exportFilepath)
        
        
    def closeEvent(self, event):
        self.saveSettings()
        event.accept()
        
        
    def menuBar(self):
        main_mnb = QMenuBar()
        
        settings_mnu = main_mnb.addMenu('&Settings')
        
        editExportSet_act = QAction('Edit Export Set Keyword', settings_mnu)
        settings_mnu.addAction(editExportSet_act)
        editExportSet_act.triggered.connect(self.exportSetDialog)
        
        defaultExportSet_act = QAction('Reset Export Set Keyword', settings_mnu)
        settings_mnu.addAction(defaultExportSet_act)
        defaultExportSet_act.triggered.connect(lambda: self.editExportSetName()) # needs lambda or a random, uneeded bool arg is passed.
        
        return main_mnb
        
            
    def fileOutputOptionsUI(self):
        self.fileOutputOptions_wgt = QGroupBox(self)
        
        fileOutput_lyt = QGridLayout(self.fileOutputOptions_wgt)
        
        self.combined_chk = QCheckBox('One File', checked=1)
        self.combined_chk.stateChanged.connect(self.toggleFileOutput)
        fileOutput_lyt.addWidget(self.combined_chk, 0, 0)
        
        
        filename = self.outputCombinedFilename()
        self.combinedFileOutput_txt = QLineEdit(filename)
        fileOutput_lyt.addWidget(self.combinedFileOutput_txt, 0, 1) # functionality for disabling this when the above chk is off
        
        outputFileBrowse_btn = QPushButton()
        outputFileBrowse_btn.setIcon(QIcon(':/fileOpen'))
        outputFileBrowse_btn.clicked.connect(self.outputSingleLocation)
        fileOutput_lyt.addWidget(outputFileBrowse_btn, 0, 2)
        
        self.separate_chk = QCheckBox('Separate Files')
        self.separate_chk.stateChanged.connect(self.toggleFileOutput)
        fileOutput_lyt.addWidget(self.separate_chk, 1, 0)
    
        
        return self.fileOutputOptions_wgt
    
    
    def toggleFileOutput(self, state):
        if state == 2:
            if self.sender() == self.combined_chk:
                self.separate_chk.setChecked(False)
                self.combinedFileOutput_txt.setDisabled(False)
                self.exportOptions_wgt.setDisabled(True)
                self.selectionOnly_btn.setDisabled(False)
            if self.sender() == self.separate_chk:
                self.combined_chk.setChecked(False)
                self.combinedFileOutput_txt.setDisabled(True)
                self.exportOptions_wgt.setDisabled(False)
                self.selectionOnly_btn.setDisabled(True)
                
            
    def exportOptionsUI(self):
        self.exportOptions_wgt = QFrame()
        self.exportOptions_wgt.setFrameStyle(QFrame.Box|QFrame.Sunken)
        
        exportOptions_lyt = QVBoxLayout(self.exportOptions_wgt)
        
        exportSetOuputs_wgt = QGroupBox()
        exportOptions_lyt.addWidget(exportSetOuputs_wgt)
        
        options_lyt = QHBoxLayout(exportSetOuputs_wgt)

        self.findExportSets()
        
        
        if self.exportSelectionSets:
            exportSets_lbl = QLabel('Export Sets:')
            output_lbl = QLabel('    Outputs:')
            
            options_lyt.addWidget(exportSets_lbl)
            options_lyt.addWidget(output_lbl)
            
            exportGroups_lyt = QVBoxLayout()
            exportOptions_lyt.addLayout(exportGroups_lyt)
        
        
            self.exportOptionsDict = {}
            for i, exportSet in enumerate(self.exportSelectionSets): #make wgt scroll area?
                exportRow_wgt = QWidget()
                
                exportRow_lyt = QHBoxLayout(exportRow_wgt)
                exportRow_lyt.setContentsMargins(0,0,0,0)
                exportGroups_lyt.addWidget(exportRow_wgt)
                
                
                self.exportOptionsDict[i] = {}
                
                exportEnabled_chk = QCheckBox()
                exportEnabled_chk.setChecked(True)
                exportEnabled_chk.stateChanged.connect(self.toggleExport)
                self.exportOptionsDict[i][f'enable_{i}'] = exportEnabled_chk
                
                exportSet_txt = QLineEdit(exportSet)
                self.exportOptionsDict[i][f'exportSet_{i}'] = exportSet_txt
                
                filename = self.outputSeparateFilename(exportSet)
                output_txt = QLineEdit(filename)
                self.exportOptionsDict[i][f'output_{i}'] = output_txt
                
                exportRow_lyt.addWidget(exportEnabled_chk)
                exportRow_lyt.addWidget(exportSet_txt)
                exportRow_lyt.addWidget(output_txt)
        else:
            noExportSets_lbl = QLabel(f'No export sets were found with the keyword "{alembicMultiExport.EXPORT_SET_NAME}".')
            options_lyt.addWidget(noExportSets_lbl) 
            
        outputDir_wgt = QFrame()
        outputDir_wgt.setFrameStyle(QFrame.Box|QFrame.Sunken)
        exportOptions_lyt.addWidget(outputDir_wgt)
        
        outputDir_lyt = QHBoxLayout(outputDir_wgt)
        
        outputDir_lbl = QLabel('Directory:')
        outputDir_lyt.addWidget(outputDir_lbl)
        
        self.outputDir_txt = QLineEdit()
        outputDir_lyt.addWidget(self.outputDir_txt)
        
        outputBrowse_btn = QPushButton()
        outputBrowse_btn.setIcon(QIcon(':/fileOpen'))
        outputBrowse_btn.clicked.connect(self.outputMultiLocation)
        outputDir_lyt.addWidget(outputBrowse_btn)
        
            
        return self.exportOptions_wgt
    
    
    def toggleExport(self, state):
        toggledCheckbox = self.sender()
        
        exportRow_wgt = toggledCheckbox.parentWidget()
        textField_wgts = exportRow_wgt.findChildren(QLineEdit)
        
        if state == 2:
            for wgt in textField_wgts:
                wgt.setEnabled(True)
                
        else:
            for wgt in textField_wgts:
                wgt.setDisabled(True)
    
    
    def confirmOptionsUI(self):
        confirm_wgt = QGroupBox(self)
        
        confirm_lyt = QHBoxLayout(confirm_wgt)
        
        self.selectionOnly_btn = QPushButton('Selection Only')
        confirm_lyt.addWidget(self.selectionOnly_btn)
        
        ok_btn = QPushButton('OK')
        confirm_lyt.addWidget(ok_btn)
        
        ok_btn.clicked.connect(self.run)
        
        return confirm_wgt
            
            
    def showWindow(self):
        self.show()
        
        return self
        
        
        
    def editExportSetName(self, newValue = 'EXPORT_SET'):
        constants.setConstant('exportSetName', newValue) # Changes variable in constant.json for future use
        alembicMultiExport.EXPORT_SET_NAME = newValue # Updates the current session to look for this new name
        self.close() # closes window, since window will need a refresh to populate with new found sets. 
    
    def exportSetDialog(self):
        newExportSetName, confirm = QInputDialog.getText(self,
                                                         'New Export Set Keyword',
                                                         'Window must be re-opened to reflect change.\n'
                                                         'If blank, all sets are shown.\n\n'
                                                         'Export Set Name:',
                                                         QLineEdit.Normal,
                                                         alembicMultiExport.EXPORT_SET_NAME)
        if confirm:
            self.editExportSetName(newValue=newExportSetName)
    
    
    def findExportSets(self):
        self.exportSelectionSets = alembicMultiExport.MultiExport.findExportSets()
        
        return self.exportSelectionSets
    
    
    def outputSeparateFilename(self, exportSet):
        namespace = exportSet.split(':')[0]
        name = namespace+'.abc'
        return name
    
    
    def outputCombinedFilename(self):
        sceneName = cmds.file(q=1, sceneName=1, shortName=1)
        if sceneName == '':
            sceneName = 'untitled'
        name = sceneName.split('.')[0]+'.abc'
        
        return name
    
    
    def outputSingleLocation(self):
        fileFilter = 'Alembic (*.abc);; All Files(*)'
        startingDirectory = self.exportDir
        selection = cmds.fileDialog2(
            fileFilter = fileFilter,
            dialogStyle = 2,
            startingDirectory = startingDirectory,
            fileMode = 0
        )[0]
        
        if not selection.lower().endswith('.abc'):
            selection += '.abc'
        
        self.combinedFileOutput_txt.setText(selection)
        
        
    def outputMultiLocation(self):
        fileFilter = 'All Files(*)'
        lastDirectory = self.outputDir_txt.text()
        startingDirectory = lastDirectory if lastDirectory != '' else self.exportDir
        print(startingDirectory,end='\n\n\THIS IS IT')
        selection = cmds.fileDialog2(
            fileFilter = fileFilter,
            dialogStyle = 2,
            startingDirectory = startingDirectory,
            fileMode = 2
        )[0]
        
        self.outputDir_txt.setText(selection)
    
    
    def run(self):
        if self.combined_chk.isChecked():
            self.exportSingle()
        else: 
            self.exportMulti()
            
        self.successDialog()
            
    
    def exportSingle(self):
        filepath = self.combinedFileOutput_txt.text()
        
        if cmds.ls(sl=1):
            alembicSingleExport.SingleExport.exportSelection(filepath)
        else:
            alembicSingleExport.SingleExport.exportSelectionSets(filepath)
            
        self.filepaths = [filepath]
        
        return [filepath]
    
    
    def exportMulti(self):
        exportDict = {}
        for i in range(len(self.exportSelectionSets)):
            runExport_chk = self.exportOptionsDict[i][f'enable_{i}']
            if not runExport_chk.isChecked():
                continue
            
            exportSetName = self.exportOptionsDict[i][f'exportSet_{i}'].text()
            
            outputFilename = self.exportOptionsDict[i][f'output_{i}'].text()
            if not outputFilename.lower().endswith('abc'):
                outputFilename += '.abc'
            
            outputDirectory = self.outputDir_txt.text()
            outputPath = os.path.join(outputDirectory, outputFilename)
            
            exportDict[exportSetName] = outputPath
            
        alembicMultiExport.MultiExport.exportSelectionSets(exportSetsOutputDict=exportDict)
        
        filepaths = [filepath for filepath in exportDict.values()]
        self.filepaths = filepaths
        
        return filepaths
        
    
    def successDialog(self):
        confirm_msg = QMessageBox()
        confirm_msg.setWindowTitle('Export Complete')
        
        filesExportedNum = len(self.filepaths)
        filePlural = 'file' if filesExportedNum == 1 else 'files'
        exportLocation = self.filepaths[0]
        finishingMessage = f'{filesExportedNum} {filePlural} exported to:\n {exportLocation}'
        
        confirm_msg.setText(finishingMessage)
        
        confirm_msg.addButton(QMessageBox.Ok)
        confirm_msg.addButton('Open Directory', QMessageBox.YesRole)
        
        answer = confirm_msg.exec_()
        print(answer)
        
        if answer == 1024: #OK = 1024
            self.close()
        if answer == 0: #Yes = 0
            self.openFileLocation(exportLocation)
            
            
    def openFileLocation(self, directory):
        formattedDirectory = directory.replace('/','\\') 
        Popen(f'explorer /select,"{formattedDirectory}"')
            
    