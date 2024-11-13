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


import singleExport
import multiExport
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
         
        
        
    def mainUI(self):
        """Creates the master layout and adds the widgets.
        """
        master_lyt = QVBoxLayout(self)
        
        master_lyt.addWidget(self.menuBar())
        
        main_wgt = QGroupBox()
        master_lyt.addWidget(main_wgt)
        
        self.main_lyt = QVBoxLayout(main_wgt)
        
        self.main_lyt.addWidget(self.fileOutputOptionsUI())
        self.main_lyt.addWidget(self.exportOptionsUI())
        self.main_lyt.addWidget(self.confirmOptionsUI())
        
    
    def saveSettings(self):
        """Saves the UI preferences for the next time the window is opened. 
        """
        settings = QSettings(*self.UI_SETTINGS)
        
        settings.setValue('combinedFileCheckbox', self.combined_chk.isChecked())
        settings.setValue('exportLocation', self.outputDir_txt.text())
        
        
    def loadSettings(self):
        """Loads the UI preferences.
        """
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
        """Activates when the window is closed. 
        When the window closes, the UI settings are saved.
        """
        self.saveSettings()
        event.accept()
        
        
    def menuBar(self):
        """Returns the menu bar widget.
        """
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
        """Returns the upper widget, which asks the user wether to export a single or multiple files.
        """
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
        """Toggles what is enabled depending on the selected output file checkbox.
        """
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
        """Returns the lower widget, which asks the user for the multi-file export names/dir.
        """
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
            noExportSets_lbl = QLabel(f'No export sets were found with the keyword "{multiExport.EXPORT_SET_NAME}".')
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
        """Toggles the child widgets of the multi export widget.
        """
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
        """Returns the lowest widget, 2 buttons that execute the tool.
        """
        confirm_wgt = QGroupBox(self)
        
        confirm_lyt = QHBoxLayout(confirm_wgt)
        
        self.selectionOnly_btn = QPushButton('Selection Only')
        confirm_lyt.addWidget(self.selectionOnly_btn)
        self.selectionOnly_btn.clicked.connect(lambda: self.run(True))
        
        
        ok_btn = QPushButton('OK')
        confirm_lyt.addWidget(ok_btn)
        ok_btn.clicked.connect(self.run)
        
        return confirm_wgt
            
            
    def showWindow(self):
        """Shows the window.
        """
        self.show()
        
        return self
        
        
        
    def editExportSetName(self, newValue = 'EXPORT_SET'):
        """The export set name is saved in the constants.json file.
        This function edits the json file and updates the constant variables within the respective export modules.
        """
        constants.setConstant('exportSetName', newValue) # Changes variable in constant.json for future use
        multiExport.EXPORT_SET_NAME = newValue # Updates the current session to look for this new name in the Multi exporter
        singleExport.EXPORT_SET_NAME = newValue # Updates the current session to look for this new name Single exporter
        self.exportOptions_wgt.deleteLater() # Deletes the widget made in exportOptionsUI
        self.main_lyt.insertWidget(1, self.exportOptionsUI()) # Re-adds the widget to the layout with the updates
        if self.combined_chk.isChecked():
            self.exportOptions_wgt.setDisabled(True)
        else:
            self.exportOptions_wgt.setDisabled(False)

    
    
    def exportSetDialog(self):
        """A dialog to edit the export set name.
        Returns the user given name.
        """
        newExportSetName, confirm = QInputDialog.getText(self,
                                                         'New Export Set Keyword',
                                                         'Window must be re-opened to reflect change.\n'
                                                         'If blank, all sets are shown.\n\n'
                                                         'Export Set Name:',
                                                         QLineEdit.Normal,
                                                         multiExport.EXPORT_SET_NAME)
        if confirm:
            self.editExportSetName(newValue=newExportSetName)
    
    
    def findExportSets(self):
        """Returns the unique export sets for the multi export.
        """
        self.exportSelectionSets = multiExport.MultiExport.findExportSets()
        
        return self.exportSelectionSets
    
    
    def outputSeparateFilename(self, exportSet):
        """Returns the name of the unique export set with the alembic file extension.
        """
        namespace = exportSet.split(':')[0]
        name = namespace+'.abc'
        return name
    
    
    def outputCombinedFilename(self):
        """Returns the name of the scene with the alembic file extension.
        """
        sceneName = cmds.file(q=1, sceneName=1, shortName=1)
        if sceneName == '':
            sceneName = 'untitled'
        name = sceneName.split('.')[0]+'.abc'
        
        return name
    
    
    def outputSingleLocation(self):
        """A dialog to search for the single export directory.
        """
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
        """A dialog to search for the multi export directory.
        """
        fileFilter = 'All Files(*)'
        lastDirectory = self.outputDir_txt.text()
        startingDirectory = lastDirectory if lastDirectory != '' else self.exportDir
        selection = cmds.fileDialog2(
            fileFilter = fileFilter,
            dialogStyle = 2,
            startingDirectory = startingDirectory,
            fileMode = 2
        )[0]
        
        self.outputDir_txt.setText(selection)
    
    
    def run(self, selection = False):
        """Runs tool based on which box user selected.
        if selection argument set to True and single export is active, exports selection only.
        """
        if self.combined_chk.isChecked():
            self.exportSingle(selection)
        else: 
            self.exportMulti()
            
        self.successDialog()
            
    
    def exportSingle(self, selection):
        """Runs the single export.
        Returns the output filepath.
        """
        filepath = self.combinedFileOutput_txt.text()
        
        if selection:
            singleExport.SingleExport.exportSelection(filepath)
        else:
            singleExport.SingleExport.exportSelectionSets(filepath)
            
        self.filepaths = [filepath]
        
        return [filepath]
    
    
    def exportMulti(self):
        """Runs the multi export.
        Returns the output filepaths.
        """
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
            
        multiExport.MultiExport.exportSelectionSets(exportSetsOutputDict=exportDict)
        
        filepaths = [filepath for filepath in exportDict.values()]
        self.filepaths = filepaths
        
        return filepaths
        
    
    def successDialog(self):
        """Dialog after process is finished.
        """
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
        """Opens the directory in the file explorer.
        """
        formattedDirectory = directory.replace('/','\\') 
        Popen(f'explorer /select,"{formattedDirectory}"')
            
    