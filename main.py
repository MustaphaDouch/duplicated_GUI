from sre_compile import isstring
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from PyQt5 import uic


class MainWindow(QMainWindow): 
    def __init__(self) :
        super().__init__()
        uic.loadUi('mainApp.ui', self)
        self.setWindowIcon(QIcon('duplicate.png'))
        self.setWindowTitle('Duplicated Files')
        
    
        #Label info
        self.label = self.findChild(QLabel, 'info')
        self.label.setText('No action was lunched!')
        
        #Label loading 
        self.loading = self.findChild(QLabel, 'loading')
        load_gif = QMovie("assets/loading.gif")
        
        self.loading.setMovie(load_gif)
        load_gif.start()
        
        # self.duplicate = self.retreiveFiles()
        
        #Scan button
        self.scanBtn = self.findChild(QPushButton, 'scanbtn')
        self.scanBtn.clicked.connect(self.scan_btn)
        
        #browse Button
        self.browseBtn = self.findChild(QPushButton, 'filebrowse')
        self.browseBtn.clicked.connect(self.browse_files)
        
        #Edit Input -> Browser Path
        self.filePath = self.findChild(QLineEdit, 'path_browser')
        self.filePath.setText("/run/media/mdg/GHOST 3.14/.Master/PFE")
        #TableView
        self.tableWidget = self.findChild(QTableWidget, 'dup_table')
 
        
        # print(self.duplicate)
        
        #ComboBox sort
        self.sortCombo = self.findChild(QComboBox, 'sort_combo')
        # self.clicked = 'No'
        # if self.clicked == 'Yes':
        # self.sortCombo.currentIndexChanged.connect(self.scan_btn if self.clicked == 'Yes' else self.sortBy)
        self.sortCombo.currentIndexChanged.connect(self.scan_btn  )
        
      
        
    ##################### START FUNCTIONS ###################
    # def sort(self, clicked):
    #     if clicked == 'Yes':
    #         return self.scan_btn
        #     print(1)
        # print(0)
        
    def choices(self, choice):
        # print(choice)
        if choice == 'Name (default)':
            duplicated = dict(sorted(self.duplicate.items(), key=lambda x : x[0], reverse=False))
        elif choice == 'Size':
            duplicated = dict(sorted(self.duplicate.items(), key=lambda x : x[1][0][1], reverse=True))
        # else:
        #     self.error('12')
            
            
        row = 0 
        for el in duplicated.keys():   
            if len(duplicated[el]) > 1 :
                for a in duplicated[el]:
                    self.tableWidget.insertRow(row)
                    self.tableWidget.setItem(row, 1, QTableWidgetItem(el))
                    self.tableWidget.setItem(row, 2, QTableWidgetItem(a[0]))
                    self.tableWidget.setItem(row, 3, QTableWidgetItem(self.megaCalc(a[1])))
                    row += 1
        self.label.setText('Done !')
            

    #SortBy ComboBox
    def sortBy(self):
        self.sortChoice = self.sortCombo.currentText()
        if self.sortChoice == 'Sort by':
            self.sortChoice = 'Name (default)'
        return self.sortChoice
        # print(self.sortChoice)
    
    #browse Files    
    def browse_files(self):
        # file_name, _ = QFileDialog.getOpenFileName(self, 'Open Directory', QDir.rootPath(), 'All Files (*.*)')
        file_name = QFileDialog.getExistingDirectory(self, 
                                                    'Open Directory', 
                                                    QDir.rootPath() , 
                                                    QFileDialog.ShowDirsOnly
                                                    | QFileDialog.DontResolveSymlinks)
        # print(file_name)
        
        self.filePath.setText(file_name)
        self.path = file_name+'/'
        
    #Retreive All Files
    def retreiveFiles(self, path):
        import os
        duplicated = {}
        for dirpath, dirs, files in os.walk(path):
            # p = dirpath
            # dirpath = dirpath.replace(r'C:\Users\D.Mustapha\OneDrive\Desktop\new_edge',r'Path')
            
            for filename in files: 
                if filename in duplicated.keys():
                    duplicated[filename].append([os.path.join(dirpath, filename), 
                                                os.path.getsize(os.path.join(dirpath, filename))])
                else:
                    duplicated[filename] = [[os.path.join(dirpath, filename), 
                                            os.path.getsize(os.path.join(dirpath, filename))]]
        return duplicated
    
          
    #Size Calculator        
    def megaCalc(self, size):
        import math
        if size <= 1024:
            return f'{size} bytes'
        elif size > 1024:
            size = size/1024
            if size >= 1024:
                size = (size/1024)
                if size >= 1024:
                    mega = size
                    size = size/1024
                    return f'{mega} Mb ({math.floor(size)} Gb)'
                return f'{math.floor(size)} Mb'            
            return f'{math.floor(size)} kb'
        
    #Scan button
    def scan_btn(self):
        self.label.setText('Loading information ...')
        self.path = self.filePath.text()
        if not self.path :
            self.error('File Path Is Empty')
            self.label.setText('Error !')
            
        else:
            try:                
                self.duplicate = self.retreiveFiles(self.path+'/')
                self.choices(self.sortBy())
                
            except Exception as e:
                self.error(e)
                
        self.clicked = 'Yes'          
    #Error, Alerts...
    def error(self, exception):
        self.alert = QMessageBox.critical(
        self,
        "Error!",
        f'{exception}',
        buttons=QMessageBox.Discard | QMessageBox.Ignore,
        defaultButton=QMessageBox.Discard,
    )

        
   
try:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_() 
except Exception as error:
    print(error)