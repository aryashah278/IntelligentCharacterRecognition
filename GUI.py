from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import writer
import Cleaner
import scanner
import sys
import os
import shutil
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import cropper
import PatternLocator
import predict
import keyReader
import Uploader
import time
class window1(QWidget):

    def __init__(self, parent=None):
        super(window1,self).__init__(parent)
        self.pathsField = QLineEdit(self)
        self.browseBtn = QPushButton("Browse", self)
        self.fromPhoneButton = QPushButton("From Phone",self)
        self.fromOtherFilesButton = QPushButton("From Other Files",self)
        self.dropDownLabel = QLabel(self)
        self.formIdDropDown = QComboBox(self)
        self.nextPage = QPushButton("Next> ",self)
        self.newfont = QFont("Times", 16)
        print(MainWindow.final)
        self.initUI()

    def initUI(self):
        #textField
        self.instruct = QLabel(self)
        self.instruct.setText("Select 'from other files' to enable browse button")
        self.instruct.move(200,30)
        self.instruct.resize(750,50)
        self.pathsField.move(200, 100)
        self.pathsField.resize(750, 50)
        #browseButton
        self.browseBtn.setEnabled(False)
        self.browseBtn.move(1000, 100)
        self.browseBtn.resize(100, 50)
        #from files or phone
        self.fromPhoneButton.move(300, 250)
        self.fromPhoneButton.resize(150, 50)

        self.fromOtherFilesButton.move(700, 250)
        self.fromOtherFilesButton.resize(200, 50)

        #form_id
        for row in MainWindow.info:
            self.formIdDropDown.addItem(row[0])

        self.dropDownLabel.setText("Select Form")
        self.dropDownLabel.move(400,450)
        self.dropDownLabel.resize(150,50)
        self.formIdDropDown.move(550,450)
        self.formIdDropDown.resize(250,50)

        #next page
        self.nextPage.move(500,600)
        self.nextPage.resize(150,50)

        #setting font
        self.pathsField.setFont(self.newfont)
        self.browseBtn.setFont(self.newfont)
        self.fromPhoneButton.setFont(self.newfont)
        self.fromOtherFilesButton.setFont(self.newfont)
        self.formIdDropDown.setFont(self.newfont)
        self.dropDownLabel.setFont(self.newfont)
        self.nextPage.setFont(self.newfont)
        self.instruct.setFont(self.newfont)
        #events
        self.fromOtherFilesButton.clicked.connect(self.otherFiles)
        self.fromPhoneButton.clicked.connect(self.phone)
        self.browseBtn.clicked.connect(self.browseFunc)
        self.formIdDropDown.activated[str].connect(self.onActivated)

    def otherFiles(self):
        self.browseBtn.setEnabled(True)
        self.instruct.setText("File Transfer mode")

    def phone(self):
        self.browseBtn.setEnabled(False)
        self.instruct.setText("Phone Transfer mode")
        self.folder_path = "./demoImagesForPhone/"
        self.images = os.listdir(self.folder_path)
        self.moveTo = "FromPhone"
        cnt = 0
        for i in self.images:
            if i.endswith(".jpg"):
                destFilename = os.path.join(self.moveTo, i)
                srcFileName = os.path.join(self.folder_path, i)
                shutil.move(srcFileName, destFilename)

    def browseFunc(self):
        self.folder_path = str(QFileDialog.getExistingDirectory(None, "Select Folder"))
        self.pathsField.setText(self.folder_path)
        self.images = os.listdir(self.folder_path)
        self.moveTo = "FromPhone"
        cnt = 0
        for i in self.images:
            if i.endswith(".jpg"):
                destFilename = os.path.join(self.moveTo,i)
                srcFileName = os.path.join(self.folder_path,i)
                shutil.copy(srcFileName,destFilename)

    def onActivated(self):
        temp = list(MainWindow.info[:,0])
        MainWindow.form_id = temp.index(self.formIdDropDown.currentText())

class window1_5(QWidget):
    def __init__(self, parent=None):
        super(window1_5, self).__init__(parent)
        self.newfont = QFont("Times", 22, QFont.Bold)
        self.newfont2 = QFont("Times", 16)
        self.initUI()

    def initUI(self):
        self.statusLabel = QLabel(self)
        self.statusLabel.setText("Waiting for User Action")
        self.finalLabel = QLabel(self)
        self.finalLabel.setText("After pressing 'Start Loading', it may take few minutes")
        self.finalLabel.setFont(self.newfont)
        self.statusLabel.move(10,10)
        self.statusLabel.resize(500, 50)
        self.statusLabel.setFont(self.newfont)
        self.finalLabel.move(225,300)
        self.finalLabel.resize(1000,70)
        self.startVerifying = QPushButton("Start Verification",self)
        self.startVerifying.setFont(self.newfont2)
        self.startVerifying.setEnabled(False)
        self.startVerifying.move(450,450)
        self.startVerifying.resize(200,50)
        self.startLoading = QPushButton("Start Loading",self)
        self.startLoading.move(450,200)
        self.startLoading.resize(200,50)
        self.startLoading.setFont(self.newfont2)
        self.startLoading.clicked.connect(self.startLoad)


    def startLoad(self):
        self.startLoading.setEnabled(False)
        self.statusLabel.setText("Scaning Images.")
        scanner.main(MainWindow.form_id)
        self.statusLabel.setText("Images Scanned. Cropping Images.")
        cropper.main(MainWindow.form_id)
        self.statusLabel.setText("Images Cropped. Finding Tags.")
        PatternLocator.main(MainWindow.form_id)
        self.statusLabel.setText("Tags located. Extraacting Data.")
        predict.main(MainWindow.form_id)
        self.statusLabel.setText("Done.")
        
        

        self.startVerifying.setEnabled(True)
        temp = list(np.load("results.npy"))

        for each in temp:
            MainWindow.result.append(list(each))
        
        MainWindow.x, MainWindow.y =  len(MainWindow.result), len(MainWindow.result[1])

class window2(QWidget):
    tfs = []
    lbls = []
    temperory = []
    def __init__(self,parent=None):
        super(window2,self).__init__(parent)
        self.newfont = QFont("Times", 16)
        self.initUI()

    def initUI(self):
        MainWindow.formLogs = MainWindow.formLogs[MainWindow.form_id]
        count = 0
        for row in MainWindow.formLogs:
            if not (row[7]==0):
                window2.tfs.append(QLineEdit(self))
                window2.lbls.append(QLabel(self))
        for i in range(len(window2.tfs)):
            window2.tfs[i].move(125,i*200+50)
            window2.tfs[i].resize(200,50)
            window2.tfs[i].setText(MainWindow.result[0][i])
            window2.lbls[i].move(50,i*200+50)
            window2.lbls[i].resize(100,50)
            window2.lbls[i].setText(MainWindow.formLogs[i][0])
                
        self.gui_images = []
        gui_files = sorted(os.listdir("ForGUI"))
        for i in gui_files:
            if i.endswith(".jpg"):
                self.gui_images.append(i)

        self.imageLabel = QLabel(self)
        pixmap = QPixmap(os.path.join("ForGUI",self.gui_images[MainWindow.imageNumber]))
        pixmap2 = pixmap.scaled(450,500)
        self.imageLabel.setPixmap(pixmap2)
        self.imageLabel.move(550,50)
        self.imageLabel.resize(450,500)
        self.nextImage = QPushButton("Next Image > ",self)
        self.nextImage.move(250,575)
        self.nextImage.resize(150,50)
        self.endImage = QPushButton("End", self)
        self.endImage.setEnabled(False)
        self.endImage.move(500, 575)
        self.endImage.resize(150, 50)
        self.nextImage.setFont(self.newfont)
        self.endImage.setFont(self.newfont)
        self.nextImage.clicked.connect(self.looks)

    def looks(self):
        for i in range(len(window2.tfs)):
            window2.temperory.append(window2.tfs[i].text())
            
        MainWindow.final.append(window2.temperory)
        window2.temperory = []
        

        if MainWindow.imageNumber != len(self.gui_images)-1:

            MainWindow.imageNumber += 1
            self.imageLabel.clear()
            pixmap = QPixmap(os.path.join("ForGUI",self.gui_images[MainWindow.imageNumber]))
            pixmap2 = pixmap.scaled(450,500)
            self.imageLabel.setPixmap(pixmap2)
            self.imageLabel.move(550, 50)
            self.imageLabel.resize(450, 500)
            
            for i in range(len(window2.tfs)):
                window2.tfs[i].setText(MainWindow.result[MainWindow.imageNumber][i])
        else:
            self.endImage.setEnabled(True)
            self.nextImage.setEnabled(False)


class window3(QWidget):
    def __init__(self, parent=None):
        super(window3, self).__init__(parent)
        np.save("results.npy", MainWindow.final)       
        self.initUI()
        
    def initUI(self):
        newfont = QFont("Times", 22, QFont.Bold)
        self.finalLabel = QLabel(self)
        self.finalLabel.setText("Your data will soon be updated to the client database. Please don't close the application.")
        self.finalLabel.setFont(newfont)
        self.finalLabel.move(200,300)
        self.finalLabel.resize(1000,70)
        Uploader.main(MainWindow.form_id, MainWindow.sk)
        Cleaner.main()
        self.finalLabel.setText("Data Uploaded! You may now exit!")
        

class MainWindow(QMainWindow):

    form_id = 0
    imageNumber = 0
    formLogs = np.load("formLogs.npy")
    info = np.load("info.npy")
    result = []
    final = []
    x,y = 0,0
    sk = keyReader.main()
    def __init__(self):
        Cleaner.main()
        super(MainWindow,self).__init__()
        self.setGeometry(50,50,1200,800)
        self.setWindowTitle("ReForm IT")
        session_id = QLabel(self)
        session_id.setText("Session_key:" + str(MainWindow.sk))
        session_id.move(800, 0)
        session_id.resize(300, 50)
        self.startWindow1()

    def startWindow1(self):
        self.win1 =  window1(self)
        self.setCentralWidget(self.win1)
        self.win1.nextPage.clicked.connect(self.startWindow1_5)
        self.show()

    def startWindow1_5(self):
        self.win1_5 = window1_5(self)
        self.setCentralWidget(self.win1_5)
        self.win1_5.startVerifying.clicked.connect(self.startWindow2)
        self.show()

    def startWindow2(self):
        self.win2 = window2(self)
        self.setCentralWidget(self.win2)
        self.win2.endImage.clicked.connect(self.startWindow3)
        self.show()

    def startWindow3(self):
        self.win3 = window3(self)
        self.setCentralWidget(self.win3)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
