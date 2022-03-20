#!/usr/bin/env python



from PyQt5 import QtCore
from PyQt5.QtCore import QFile, QFileInfo, QRect, QRegExp, QSize, QStringListModel, Qt, QTextCodec, pyqtSlot
from PyQt5.QtGui import (QColor, QCursor, QFont, QFontDatabase, QFontInfo, QIcon, QKeySequence, QPainter,
        QPixmap, QSyntaxHighlighter, QTextBlockFormat, QTextCharFormat, QTextCursor,
        QTextDocumentWriter, QTextFormat, QTextListFormat)
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QColorDialog,
        QComboBox, QCompleter, QFileDialog, QFontComboBox, QGroupBox, QHBoxLayout, QListWidget, QMainWindow, QMenu, QMessageBox, QPlainTextEdit, QPushButton, QSizePolicy,
        QTextEdit, QToolBar)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import (QFont, QTextCharFormat, QTextCursor, QTextFrameFormat,
        QTextLength, QTextTableFormat)
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog, QWidget,QDockWidget,
        QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QMainWindow,
        QMessageBox, QMenu, QTableWidget, QTableWidgetItem, QTabWidget,
        QTextEdit)
from PyQt5.QtPrintSupport import QAbstractPrintDialog, QPrintDialog, QPrinter
from PyQt5.Qsci import *
import sys
import os

import shutil
import time
import json
import re
from subprocess import STDOUT, PIPE
import argparse
import shutil
import subprocess
from subprocess import check_output, CalledProcessError, STDOUT
from datetime import datetime


import zipfile


rsrcPath = os.getcwd()+"/res"

currentProjectName=""
currentProjectFolder=""

currentFileName=""
currentFileFolder=""

ANDROID_SDK="/home/djoker/Android/Sdk"
ANDROID_NDK="/home/djoker/Android/Sdk/ndk/22.1.7171670"
AAPT       =ANDROID_SDK+'/build-tools/30.0.3/aapt'
DX         =ANDROID_SDK+'/build-tools/30.0.3/dx'
DX8        =ANDROID_SDK+'/build-tools/30.0.3/d8'
ZIPALIGN   =ANDROID_SDK+'/build-tools/30.0.3/zipalign'
APKSIGNER  =ANDROID_SDK+'/build-tools/30.0.3/apksigner'
PLATFORM   =ANDROID_SDK+'/platforms/android-31/android.jar'
JAVA_SDK   ='/usr/lib/jvm/jdk1.8.0_291'
JAVA_LIB_RT='/usr/lib/jvm/jdk1.8.0_291/jre/lib/rt.jar'
JAVAFX     ="/usr/lib/jvm/jdk1.8.0_291/lib/javafx-mx.jar"

ANDROIDFXRT="/media/djoker/code/linux/python/compiler/javafx/jarlibs/jfxrt.jar"
ANDROIDJFXDVK="/media/djoker/code/linux/python/compiler/javafx/jarlibs/jfxdvk.jar"
ANDROIDFXCOMPACT="/media/djoker/code/linux/python/compiler/javafx/jarlibs/compat-1.0.0.jar"
ANDROIDMULTIDEX="/media/djoker/code/linux/python/compiler/javafx/jarlibs/android-support-multidex.jar"
ANDROIDDESUGAR="/media/djoker/code/linux/python/compiler/javafx/jarlibs/desugar_jdk_libs-1.0.10.jar"


SHOW_COMMAND=True
    

def trace(*args):
    result = ""
    for x in args:
        result += x
    print(result)    
        
def runProcess(command, args=[],wait=True):
    args = [command] + args
    def cmd_args_to_str(cmd_args):
        return ' '.join([arg if not ' ' in arg else '"%s"' % arg for arg in cmd_args])

    global SHOW_COMMAND
    if SHOW_COMMAND:
        trace("Execute -> ",cmd_args_to_str(args))
    proc = subprocess.Popen(args,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    
    stdout, stderr = proc.communicate()
    if wait:
        proc.wait()
    return proc.returncode, stdout, stderr
    
def cmd_args_to_str(cmd_args):
    return ' '.join([arg if not ' ' in arg else '"%s"' % arg for arg in cmd_args])


def getParentDir(path, level=1):
  return os.path.normpath( os.path.join(path, *([".."] * level)) )

def cleanString(string):
    return "-".join(string.split())

def createPath(root,sub):
    path = os.path.join(os.path.dirname(os.path.abspath(root)), sub)
    trace("Create path ",path)
    if not os.path.exists(path):
            os.mkdir(path)

def createFolderTree(maindir):
    if not os.path.exists(maindir):
        try:
                    os.makedirs(maindir)
        except OSError as e:
                 trace('Something else happened'+str(e))

def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


def CompileJavaDesktop(mainWindow,mainRoot,appName,srcFolder,javaLibs,javaSrcFiles):
    
    #args=[]

    #args.append("-cp")
    #addToClass=outFolder
    #for p in pathsList:
    #    addToClass+=":"+p

    #args.append(outFolder+":"+outFolder+OSP+"camsview")
    #args.append(addToClass)
    #args.append(appName)

    #mainWindow.trace(" Execute  java code ...")
    
    #code, out, err=runProcess("java",args)
    #if code!=0:
    #    mainWindow.trace("Error  Nuning :"+err.decode("utf-8") )
    #    return False
    #mainWindow.trace(out.decode("utf-8"))

  
    return True

class JavaProject():
    def __init__(self,mainWindow, folderRoot,projectName):
        self.FolderRoot=folderRoot
        self.projectName=projectName
        self.MainClass=""
        self.MainPackage=""
        self.MainLabel=""
        self.AndroidLibPath=""
        self.DesktopLibPath=""
        self.AndroidLibs=[]
        self.DesktopLibs=[]
        self.DesktopLibs.append("/media/djoker/code/linux/python/projects/JavaFX/libs/json.jar")
        self.DesktopLibs.append("/media/djoker/code/linux/python/projects/JavaFX/libs/re2j.jar")

        self.pathsList=[]
        self.ARM7=True
        self.ARM64=False
        self.srcFiles=[]
        self.mainWindow=mainWindow
    def addSrc(self,src):
        if not src in self.srcFiles:
            self.srcFiles.append(src)

    def clear(self):
        pass
    def addLib(self,src,plat):
        if plat==0:
            self.AndroidLibs.append(src)
            self.DesktopLibs.append(src)
        if plat==1:
            self.DesktopLibs.append(src)
        if plat==2:
            self.AndroidLibs.append(src)
        


    def compile(self):
        self.mainWindow.trace("Start JOB.")
        #def CompileJavaDesktop(mainRoot,appName,srcFolder,javaLibs,javaSrcFiles):
        OSP=os.path.sep
        outFolder=self.FolderRoot+OSP+"out"+OSP
        
        
        if not os.path.exists(outFolder):
            self.mainWindow.trace("Create :"+outFolder)
            os.mkdir(outFolder)
        
        


        

        self.pathsList=[]
        for src in self.srcFiles:
            
            path = os.path.dirname(os.path.abspath(src))
            if path not in self.pathsList:
                self.pathsList.append(path)
                self.mainWindow.trace("Add Path:",path) 


            args=[]
            #args.append("-Xlint:deprecation")
            #args.append("-deprecation")
            #args.append("-Xmaxerrs")
            args.append("-nowarn")
            args.append("-Xlint:none")
            args.append("-J-Xmx2048m")
            args.append("-Xlint:unchecked")
                
            args.append("-source")
            args.append("1.8")
            args.append("-target")  
            args.append("1.8")
            args.append("-d")
            args.append(outFolder)
            #args.append("-bootclasspath")
            #args.append(JAVA_LIB_RT+":"+JAVAFX+":"+JAVA_LIB_RT)
            args.append("-classpath")
            if len(self.DesktopLibs)>=1:
                lista =JAVAFX
                for lib in self.DesktopLibs:
                    lista+=":"+lib
                print(lista)
                args.append(lista)
            else:
                args.append(JAVAFX)
                
            
            args.append("-sourcepath")
            args.append(self.FolderRoot+":"+outFolder)
            args.append(src)

            src_modified_time = os.path.getmtime(src)
            
            src_convert_time = time.ctime(src_modified_time)
            print(src_convert_time)




            filename, file_extension = os.path.splitext(src)
            basename = os.path.basename(src)
            basename_without_ext = os.path.splitext(os.path.basename(src))[0]
            maindir = os.path.dirname(os.path.abspath(src))
            maindir = maindir.replace(self.FolderRoot,maindir+OSP+"out")
            self.mainWindow.trace("save to  "+ maindir)
            

            objName=maindir+OSP+basename_without_ext+".class"
            

            if os.path.exists(objName):
                obj_modified_time = os.path.getmtime(objName)
                obj_convert_time = time.ctime(obj_modified_time)
                
                print(obj_convert_time)
                if (src_convert_time<=obj_convert_time):
                    self.mainWindow.trace("Skip "+ src)
                    continue
            
            self.mainWindow.trace("Compile ", src,">" ,objName)
            code, out, err=runProcess("javac",args)
            if code!=0:
                self.mainWindow.trace("Error  compiling :"+err.decode("utf-8") )
                return False
            self.mainWindow.trace(out.decode("utf-8"))  
        

        self.mainWindow.trace('Job  is done ...')


    def run(self):
        OSP=os.path.sep
        outFolder=self.FolderRoot+OSP+"out"+OSP

        args=[]

        args.append("-cp")
        addToClass=outFolder
        for p in self.pathsList:
            if not p in self.pathsList:
                addToClass+=":"+p
        if len(self.DesktopLibs)>=1:
            for lib in self.DesktopLibs:
                addToClass+=":"+lib

        #args.append(outFolder)
        args.append(addToClass)
        args.append(self.MainPackage+"."+self.MainClass)

        self.mainWindow.trace(" Execute  java code ...",self.MainClass)
        
        code, out, err=runProcess("java",args)
        if code!=0:
            self.mainWindow.trace("Error  Nuning :"+err.decode("utf-8") )
            return False
        self.mainWindow.trace(out.decode("utf-8"))
        
    def save(self):
        self.mainWindow.trace("save project")
        try:
            with open(self.projectName, 'w') as f:
                f.write("{ \n")
                f.write('"Project":"'+self.projectName+'",\n')
                f.write('"Folder":"'+self.FolderRoot+'",\n')
                f.write('"MainClass":"'+self.MainClass+'",\n')
                f.write('"MainPackage":"'+self.MainPackage+'",\n')
                f.write('"MainLabel":"'+self.MainLabel+'",\n')
                f.write('"Src":[')
                count = len(self.srcFiles)
                index=1
                for src in self.srcFiles:
                    print(index,"",count)
                    if index<count:
                        f.write('"'+src+'",\n')
                    if index==count:
                        f.write('"'+src+'"\n')

                    
                    index+=1
                
                f.write(']\n')



                f.write("} \n")
        except Exception as e:
            print("Error SAVE project file ",e)
            return 
    
    def load(self):
        project = None
        try:
            with open(self.projectName, "r") as jsonfile:
                project = json.load(jsonfile)
                print(project)
                self.FolderRoot  =project['Folder']
                self.MainClass   =project['MainClass']
                self.MainPackage =project['MainPackage']
                self.MainLabel   =project['MainLabel']
                self.srcFiles    =project['Src']
        except Exception as e:
            print("Error load project file ",e)
            return 

        
      
 

class CodeListView(QListWidget):
    
    def __init__(self,  parent=None):
        super(CodeListView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(72, 72))
        self.items = []
        self.mainfolder = None
        
        
        self.clicked.connect(self.onClick)
        self.doubleClicked.connect(self.onDoubleClicked)
    

        
    def onClick(self):
        #print("clink")    
        pass

    def onDoubleClicked(self,item):
        print("doublw clink",str(item.row()))   


    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        clrAct = contextMenu.addAction("Clear")
        removeAct = contextMenu.addAction("Remove")
        listAct = contextMenu.addAction("List")

        if self.count()<=0:
            return 
        
        
        
        #print("count ",self.count())
        #print("row ",self.currentRow())
        index = self.currentRow()
        

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == clrAct:
            self.items=[]
            self.clear()
            self.mainfolder==None
        if action == removeAct:
            print("Remove   ",str(self.items[index])," index: ", index)
            self.items.pop(index)
            self.takeItem(index)
        if action==listAct:
            for i in range(self.count()):
                print(self.items[i])

            
    def clearAll(self):
        self.items=[]
        self.clear()
    def MoveUp(self):
        currentRow = self.currentRow()
        currentItem = self.takeItem(currentRow)
        self.insertItem(currentRow - 1, currentItem)

    def MoveDown(self):
        currentRow = self.currentRow()
        currentItem = self.takeItem(currentRow)
        self.insertItem(currentRow + 1, currentItem)        

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    
    def addSrcFile(self,src):
        print(src)
    
    

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                isDirectory = os.path.isdir(str(url.toLocalFile()))
                if isDirectory:
                    path = str(url.toLocalFile())
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            ext = os.path.splitext(file)[1]
                            print(os.path.join(root, file))
                            self.addSrcFile(os.path.join(root, file))
                else:
                    self.addSrcFile(str(url.toLocalFile()))
                    

        else:
            event.ignore()
            
            
class TabEditor(QWidget):
    def __init__(self):
        super(TabEditor, self).__init__()




class CodeEditor(QsciScintilla):
#class CodeEditor(QTextEdit):
    def __init__(self, parent=None):
        QsciScintilla.__init__(self, parent)
        self.setup()


    
    def setup(self):
        # Set the autocompletion to be case IN-sensitive
        self.setAutoCompletionCaseSensitivity(False)
        # Set the threshold at which the autocompletion window appears
        self.setAutoCompletionThreshold(1)
        # Set the source from which the autocompletions will be pulled from
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        # Sets whether the characters to the right of the autocompletion
        # will be overwritten when an autocompletion is selected.
        self.setAutoCompletionReplaceWord(True)
        # Select the behaviour of autocompletions when there is only a single
        # entry in the autocompletion list. The selection below sets that
        # when the autocompletion window will always be displayed.
        self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)
        



        
        
        







class SetupDialog(QDialog):
    def __init__(self,proj, parent=None):
        QDialog.__init__(self, parent)
        self.resize(660, 398)
        self.projectSetup=proj
        self.MainApp=parent
        self.isConfig=False
        self.androidArm7=False
        self.androidArm764=False
        self.MainClass="Main"
        self.AndroidLabel="MyApplication"
        self.aplicationPackage="com.djokersoft.myaplication"

        self.groupBox = QGroupBox(self)
        self.groupBox.setGeometry(QRect(10, 10, 631, 141))
        self.lineEditAndroidActivity = QLineEdit(self.groupBox)
        self.lineEditAndroidActivity.setGeometry(QRect(10, 50, 181, 24))
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setGeometry(QRect(60, 30, 101, 16))

        self.lineEditAndroidPackage = QLineEdit(self.groupBox)
        self.lineEditAndroidPackage.setGeometry(QRect(210, 50, 181, 24))
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setGeometry(QRect(250, 30, 151, 16))


        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setGeometry(QRect(10, 160, 631, 151))
        self.groupBox_3 = QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QRect(10, 30, 153, 65))
        self.horizontalLayout = QHBoxLayout(self.groupBox_3)
        self.checkBoxAndroidArm0 = QCheckBox(self.groupBox_3)
        self.checkBoxAndroidArm0.setChecked(True)

        
        self.horizontalLayout.addWidget(self.checkBoxAndroidArm0)
        self.checkBoxAndroidArm1 = QCheckBox(self.groupBox_3)
        self.horizontalLayout.addWidget(self.checkBoxAndroidArm1)
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setGeometry(QRect(220, 30, 101, 16))
        self.label_2.setTextFormat(Qt.PlainText)
        self.lineEditAndroidLabel = QLineEdit(self.groupBox_2)
        self.lineEditAndroidLabel.setGeometry(QRect(180, 60, 141, 24))
        self.pushButtonOK = QPushButton(self)
        
        self.pushButtonOK.setGeometry(QRect(560, 360, 80, 24))
        self.pushButtonCancel = QPushButton(self)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setGeometry(QRect(470, 360, 80, 24))
        self.pushButtonCancel.clicked.connect(self.close)
        self.pushButtonOK.clicked.connect(self.setpProject)

        self.retranslateUi()

    def setpProject(self):
        self.androidArm7=self.checkBoxAndroidArm0.isChecked()
        self.androidArm764=self.checkBoxAndroidArm1.isChecked()
        self.MainClass=self.lineEditAndroidActivity.text()
        self.AndroidLabel=self.lineEditAndroidLabel.text()
        self.aplicationPackage=self.lineEditAndroidPackage.text()
        if self.projectSetup!=None:
            self.projectSetup.MainClass  =self.MainClass
            self.projectSetup.MainPackage=self.aplicationPackage
            self.projectSetup.MainLabel  =self.AndroidLabel
            self.projectSetup.ARM7 =self.androidArm7
            self.projectSetup.ARM64=self.androidArm764
            self.projectSetup.save()
        

            #dirsPack = self.aplicationPackage.split(".")
            
            

            createFolderTree(self.projectSetup.FolderRoot+os.path.sep+self.aplicationPackage.replace(".",os.path.sep))

            packFolder =self.projectSetup.FolderRoot+os.path.sep+self.aplicationPackage.replace(".",os.path.sep)
            

            mainJava=packFolder+os.path.sep+self.projectSetup.MainClass+".java"

            with open(mainJava, 'w') as f:
                f.write("package  "+self.aplicationPackage+" ;\n")
                f.write("public class "+self.projectSetup.MainClass+"  \n")
                f.write("{  \n")
                f.write("public static void main(String[] args)   \n")
                f.write(" {  \n")
                f.write('    System.out.println("Hello World");\n')
                f.write(" }  \n")
                f.write("}  \n")
            self.projectSetup.addSrc(mainJava)
            self.MainApp.listSrc.addSrcFile(mainJava)
            self.MainApp.load(mainJava)
            
            
        self.isConfig=True
        self.close()
       
            
    # setupUi

    def retranslateUi(self):
        self.setWindowTitle("Project Setup")
        self.groupBox.setTitle("Main")
        self.lineEditAndroidActivity.setText("MainAplication")
        self.lineEditAndroidLabel.setText("MyAplication")
        self.label_3.setText("Main Class")
        self.groupBox_2.setTitle("Android setup")
        self.groupBox_3.setTitle("ARM")
        self.checkBoxAndroidArm0.setText("Arm7")
        self.checkBoxAndroidArm1.setText("Arm64")
        self.label_2.setText("Text Label")
        self.pushButtonOK.setText("Ok")
        self.pushButtonCancel.setText("Cancel")
        self.label_4.setText("Aplication Package")
        self.lineEditAndroidPackage.setText("com.djokersoft.myaplication")

    # retranslateUi



class ConsoleText(QPlainTextEdit):
    def __init__(self,  parent=None):
        super(ConsoleText, self).__init__(parent)
    '''
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        clrAct = contextMenu.addAction("Clear")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == clrAct:
            self.clear()
    '''    

class CodeListView(QListWidget):
    
    def __init__(self, mainWindow, parent=None):
        super(CodeListView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(72, 72))
        self.items = []
        self.mainfolder = None
        self.mainWindow=mainWindow
        
        
        self.clicked.connect(self.onClick)
        self.doubleClicked.connect(self.onDoubleClicked)
    

        
    def onClick(self):
        #print("clink")    
        pass

    def onDoubleClicked(self,item):
        print("doublw clink",str(item.row()))   
        print(self.items[item.row()])
        self.mainWindow.load(self.items[item.row()])



    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        clrAct = contextMenu.addAction("Clear")
        removeAct = contextMenu.addAction("Remove")
        listAct = contextMenu.addAction("List")

        if self.count()<=0:
            return 
        
        
        
        #print("count ",self.count())
        #print("row ",self.currentRow())
        index = self.currentRow()
        

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == clrAct:
            self.items=[]
            self.clear()
            self.mainfolder==None
        if action == removeAct:
            print("Remove   ",str(self.items[index])," index: ", index)
            self.items.pop(index)
            self.takeItem(index)
        if action==listAct:
            for i in range(self.count()):
                print(self.items[i])

            
    def clearAll(self):
        self.items=[]
        self.clear()
        self.mainWindow.reload()
    def MoveUp(self):
        currentRow = self.currentRow()
        currentItem = self.takeItem(currentRow)
        self.insertItem(currentRow - 1, currentItem)

    def MoveDown(self):
        currentRow = self.currentRow()
        currentItem = self.takeItem(currentRow)
        self.insertItem(currentRow + 1, currentItem)        

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    
    def addSrcFile(self,src):
        print(src)
        if not src in self.items:
            filename, file_extension = os.path.splitext(src)
            self.items.append(src)
            self.addItem(os.path.basename(filename))



    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                isDirectory = os.path.isdir(str(url.toLocalFile()))
                if isDirectory:
                    path = str(url.toLocalFile())
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            ext = os.path.splitext(file)[1]
                            print(os.path.join(root, file))
                            self.addSrcFile(os.path.join(root, file))
                else:
                    self.addSrcFile(str(url.toLocalFile()))
            
            self.mainWindow.reload()
        else:
            event.ignore()
    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        self.setupFileActions()
        self.setupProjectActions()
        self.setupCompilerActions()
        self.setupEditActions()

        self.mainProject=None

        self.LAST_DIR=""#os.getcwd()+"/res"
        self.LAST_PROJECT=""

        
        
        self.dock = QDockWidget()
        self.dock.setWindowTitle('Src')
        self.listSrc = CodeListView(self)
        self.dock.setWidget(self.listSrc)
        self.listSrc.show()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        self.Consoledock = QDockWidget()
        self.Consoledock.setWindowTitle('Console')
        self.console = ConsoleText()
        self.Consoledock.setWidget(self.console)
        self.listSrc.show()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.Consoledock)
        
        
        
        
        self.setWindowTitle(self.tr("%s[*] - %s" % ("editor", "Java FX IDE by @ DjokerSoft")))
        self.setWindowModified(False)
        
        helpMenu = QMenu("Help", self)
        self.menuBar().addMenu(helpMenu)
        helpMenu.addAction("About", self.about)
        helpMenu.addAction("About &Qt", QApplication.instance().aboutQt)


        '''tb = QToolBar(self)
        tb.setWindowTitle("Compiler Actions")
        self.addToolBar(tb)
        self.groupBox = QGroupBox(tb)
        self.groupBox.setGeometry(QRect(160, 130, 360, 67))
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("Dektop")
        self.comboBox.addItem("Android")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setEditable(False)'''

 
        
        QApplication.clipboard().dataChanged.connect(self.clipboardDataChanged)


        self.codeTab = QTabWidget()
        
        wordlist = os.getcwd()+os.path.sep+"res"+os.path.sep+"wordlist.txt"
        self.cpplexer = QsciLexerCPP()
        self.api = QsciAPIs(self.cpplexer)
        self.AutoCompletionsFromFile(wordlist)
        
        
        
        '''self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.textEdit.copyAvailable.connect(self.actionCut.setEnabled)
        self.textEdit.copyAvailable.connect(self.actionCopy.setEnabled)'''
        
        #self.textEdit.currentCharFormatChanged.connect(self.currentCharFormatChanged)
        #self.textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
        
        #self.textEdit.document().modificationChanged.connect(                self.actionSave.setEnabled)
        #self.textEdit.document().modificationChanged.connect(                self.setWindowModified)
        #self.textEdit.document().undoAvailable.connect(                self.actionUndo.setEnabled)
        #self.textEdit.document().redoAvailable.connect(                self.actionRedo.setEnabled)
        #self.setWindowModified(self.textEdit.document().isModified())
        
        #self.actionSave.setEnabled(self.textEdit.document().isModified())
        #self.actionUndo.setEnabled(self.textEdit.document().isUndoAvailable())
        #self.actionRedo.setEnabled(self.textEdit.document().isRedoAvailable())


        
        

        #newAction.triggered.connect(self.openDialog)
        #quitAction.triggered.connect(self.close)

        self.Consoledock = QDockWidget()
        self.Consoledock.setWindowTitle('Console')
        self.console = ConsoleText()
        self.Consoledock.setWidget(self.console)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.Consoledock)
         
        self.setCentralWidget(self.codeTab)
        self.loadConfig()
        self.createTab()

    def createTab(self):
        textEdit = CodeEditor()
        textEdit.setLexer(self.cpplexer)
        textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
        textEdit.setFocus()
        
       
        textEdit.setFocus()
        #self.setCurrentFileName()
        #self.fontChanged(self.textEdit.font())
        
        
        
        self.actionUndo.triggered.connect(textEdit.undo)
        self.actionRedo.triggered.connect(textEdit.redo)
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)
        self.actionCut.triggered.connect(textEdit.cut)
        self.actionCopy.triggered.connect(textEdit.copy)
        self.actionPaste.triggered.connect(textEdit.paste)
        textEdit.copyAvailable.connect(self.actionCut.setEnabled)
        textEdit.copyAvailable.connect(self.actionCopy.setEnabled)
        
     
                

        tabIndex = self.codeTab.addTab(textEdit, "main")
        self.codeTab.setCurrentIndex(tabIndex)
    def  AutoCompletionsFromFile(self, fileName):
        f = QFile(fileName)
        if not f.open(QFile.ReadOnly):
            print("erro")
            return 

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        words = []
        while not f.atEnd():
            line = f.readLine().trimmed()
            if line.length() != 0:
                try:
                    line = str(line, encoding='ascii')
                except TypeError:
                    line = str(line)
                #print(line)
                self.api.add(line)
                words.append(line)
        
                
        
        self.api.prepare()
        QApplication.restoreOverrideCursor()
        
    def trace(self,*args):
        result = ""
        for x in args:
            result += x
        self.console.appendPlainText(result)

    def console_clear(self):
        self.console.clear()

    def closeEvent(self,event):
        self.saveConfig()

    def saveConfig(self):
        if self.mainProject!=None:
            self.mainProject.save()
        with open('config.json', 'w') as f:
            f.write("{ \n")
            f.write('"LAST_PATH":"'+self.LAST_DIR+'", \n')
            f.write('"LAST_PROJECT":"'+self.LAST_PROJECT+'"\n')
            f.write("} \n")
        
    def loadConfig(self):
        
        try:
            with open("config.json", "r") as jsonfile:
                config = json.load(jsonfile)
            
        
        
            self.LAST_DIR=config['LAST_PATH']
            self.LAST_PROJECT    =config['LAST_PROJECT']

            print(self.LAST_PROJECT)
            print(self.LAST_DIR)
            

            

            
                


        except:
            print("Error parsing config file ")

        if  os.path.exists(self.LAST_PROJECT):
            print("Load project",self.LAST_PROJECT)
            self.mainProject=JavaProject(self,self.LAST_DIR,self.LAST_PROJECT)
            self.mainProject.load()
            for src in self.mainProject.srcFiles:
                self.listSrc.addSrcFile(src)
            if len(self.mainProject.srcFiles)>0:
                self.load(self.mainProject.srcFiles[0])
            self.setWindowTitle(self.tr("%s[*] - %s" % ("editor", "Java FX IDE by @ DjokerSoft")))
    

    def modelFromFile(self, fileName):
        f = QFile(fileName)
        if not f.open(QFile.ReadOnly):
            print("erro")
            return QStringListModel(self.completer)

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        words = []
        while not f.atEnd():
            line = f.readLine().trimmed()
            if line.length() != 0:
                try:
                    line = str(line, encoding='ascii')
                except TypeError:
                    line = str(line)
                #print(line)
                words.append(line)

        QApplication.restoreOverrideCursor()

        return QStringListModel(words, self.completer)         
 

    def setupCompilerActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle("Compiler Actions")
        self.addToolBar(tb)

        menu = QMenu("&Compiler", self)
        self.menuBar().addMenu(menu)

        
        

        self.comboBox = QComboBox(tb)
        self.comboBox.setGeometry(QRect(260, 130, 360, 67))
        self.comboBox.addItem("Dektop")
        self.comboBox.addItem("Android")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setEditable(False)
        


        self.actionCompile = QAction(QIcon(rsrcPath + '/build.xpm'),
                "&Compile", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.New, triggered=self.compile)
        tb.addAction(self.actionCompile)
        menu.addAction(self.actionCompile)

        tb.insertWidget(self.actionCompile,self.comboBox)

        self.actionRun = QAction(          QIcon(rsrcPath + '/Go.png'),
                "&Run", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.New, triggered=self.compilerun)
        tb.addAction(self.actionRun)
        menu.addAction(self.actionRun)

        self.actionCompileRun = QAction(   QIcon(rsrcPath + '/buildrun.xpm'),
                "&Compile&Run", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.New, triggered=self.compile_and_run)
        tb.addAction(self.actionCompileRun)
        menu.addAction(self.actionCompileRun)

        self.actionClean= QAction(QIcon(rsrcPath + '/edit-clear.png'),
                "&Clean", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.New, triggered=self.compileclean)
        tb.addAction(self.actionClean)
        menu.addAction(self.actionClean)

        menu = menu.addMenu("Libs")

        self.AddAndroidLib= QAction("Add Android", self, triggered=self.compileclean)
        
        menu.addAction(self.AddAndroidLib)

        self.AddDesktopLib= QAction("Add Desktop", self,  triggered=self.compileclean)
        
        menu.addSeparator()
        
        menu.addAction(self.AddDesktopLib)


        


    def compile(self):
        if self.mainProject==None:
             return 
        
        self.console_clear()
        self.trace(str(self.comboBox.currentIndex())     )
        self.trace("compile"+str(self.mainProject.srcFiles))
        self.mainProject.compile()
        
        
        pass
    def compile_and_run(self):
        if self.mainProject==None:
             return 
        self.console_clear()
        self.compile()
        self.compilerun()
        
        pass
    
    def compilerun(self):
        if self.mainProject==None:
             return 
        self.console_clear()
        self.trace(" run")
        self.mainProject.run()
        pass
    
    def compileclean(self):
        if self.mainProject==None:
             return 
        self.console_clear()
        self.trace(" clean")
        pass
    
    
    
    def setupFileActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle("File Actions")
        self.addToolBar(tb)

        menu = QMenu("&File", self)
        self.menuBar().addMenu(menu)

        self.actionNew = QAction(
                QIcon.fromTheme('document-new',
                        QIcon(rsrcPath + '/filenew.png')),
                "&New", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.New, triggered=self.fileNew)
        tb.addAction(self.actionNew)
        menu.addAction(self.actionNew)

        self.actionOpen = QAction(
                QIcon.fromTheme('document-open',
                        QIcon(rsrcPath + '/fileopen.png')),
                "&Open...", self, shortcut=QKeySequence.Open,
                triggered=self.fileOpen)
        tb.addAction(self.actionOpen)
        menu.addAction(self.actionOpen)
        menu.addSeparator()

        self.actionSave = QAction(
                QIcon.fromTheme('document-save',
                        QIcon(rsrcPath + '/filesave.png')),
                "&Save", self, shortcut=QKeySequence.Save,
                triggered=self.fileSave, enabled=False)
        tb.addAction(self.actionSave)
        menu.addAction(self.actionSave)

        self.actionSaveAs = QAction("Save &As...", self,
                priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.SHIFT + Qt.Key_S,
                triggered=self.fileSaveAs)
        menu.addAction(self.actionSaveAs)
        menu.addSeparator()
 


        menu.addSeparator()

        self.actionQuit = QAction("&Quit", self, shortcut=QKeySequence.Quit,triggered=self.close)
        menu.addAction(self.actionQuit)

    def newProject(self):
        fn, fp = QFileDialog.getSaveFileName(self, "Save project as...", self.LAST_DIR,
                "Project Files pfx (*.pfx);;All Files (*)")

        if not fn:
            return False

        if not fn.endswith(".pfx"):
            fn +=".pfx"

        self.listSrc.clearAll()
        self.LAST_PROJECT=fn
        self.LAST_DIR = os.path.dirname(fn)
        print("Project Path ",self.LAST_DIR)
        print("Project filename :",self.LAST_PROJECT)
        self.mainProject=JavaProject(self,self.LAST_DIR,self.LAST_PROJECT)
        

        form = SetupDialog(self.mainProject,self)
        form.show()

            
        

    
        print(form.androidArm7)
        print(form.androidArm764)
        print(form.MainClass)
        print(form.AndroidLabel)
        print(form.aplicationPackage)
        form = None
        



        
        
    def openProject(self):
        pass

    def saveProject(self):
        pass
    def projectSaveAs(self):
        pass

    
    def setupProjectActions(self):
        menu = QMenu("&Project", self)
        self.menuBar().addMenu(menu)

        self.actionNewProject = QAction(
                QIcon.fromTheme('document-new',
                        QIcon(rsrcPath + '/filenew.png')),
                "&New", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.New, triggered=self.newProject)
        
        menu.addAction(self.actionNewProject)

        self.actionOpenProject = QAction(
                QIcon.fromTheme('document-open',
                        QIcon(rsrcPath + '/fileopen.png')),
                "&Open", self, shortcut=QKeySequence.Open,
                triggered=self.openProject)
        
        menu.addAction(self.actionOpenProject)
        menu.addSeparator()

        self.actionSaveProject = QAction(
                QIcon.fromTheme('document-save',
                        QIcon(rsrcPath + '/filesave.png')),
                "&Save", self, shortcut=QKeySequence.Save,
                triggered=self.saveProject, enabled=False)
        
        menu.addAction(self.actionSaveProject)

        self.actionSaveProjectAs = QAction("Save &As...", self,
                priority=QAction.LowPriority,
                shortcut=Qt.CTRL + Qt.SHIFT + Qt.Key_S,
                triggered=self.projectSaveAs)
        menu.addAction(self.actionSaveProjectAs)
        menu.addSeparator()
 


        menu.addSeparator()





    def setupEditActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle("Edit Actions")
        self.addToolBar(tb)

        menu = QMenu("&Edit", self)
        self.menuBar().addMenu(menu)

        self.actionUndo = QAction(
                QIcon.fromTheme('edit-undo',
                        QIcon(rsrcPath + '/editundo.png')),
                "&Undo", self, shortcut=QKeySequence.Undo)
        tb.addAction(self.actionUndo)
        menu.addAction(self.actionUndo)

        self.actionRedo = QAction(
                QIcon.fromTheme('edit-redo',
                        QIcon(rsrcPath + '/editredo.png')),
                "&Redo", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Redo)
        tb.addAction(self.actionRedo)
        menu.addAction(self.actionRedo)
        menu.addSeparator()

        self.actionCut = QAction(
                QIcon.fromTheme('edit-cut', QIcon(rsrcPath + '/editcut.png')),
                "Cu&t", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Cut)
        tb.addAction(self.actionCut)
        menu.addAction(self.actionCut)

        self.actionCopy = QAction(
                QIcon.fromTheme('edit-copy',
                        QIcon(rsrcPath + '/editcopy.png')),
                "&Copy", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Copy)
        tb.addAction(self.actionCopy)
        menu.addAction(self.actionCopy)

        self.actionPaste = QAction(
                QIcon.fromTheme('edit-paste',
                        QIcon(rsrcPath + '/editpaste.png')),
                "&Paste", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.Paste,
                enabled=(len(QApplication.clipboard().text()) != 0))
        tb.addAction(self.actionPaste)
        menu.addAction(self.actionPaste)        

  
    def load(self, f):
        print("load ",f)

        if not QFile.exists(f):
            print(f,"dont exits")
            return False

        
        try:
            with open(f, "r") as textfile:
                
                self.textEdit.setPlainText(textfile.read())
               
               
        except Exception as e:
            print("Error load",f," file :",e)
            return 

        self.setCurrentFileName(f)
        return True

    def maybeSave(self):
        
        if not self.textEdit.document().isModified():
            return True

        if self.fileName.startswith(':/'):
            return True

        ret = QMessageBox.warning(self, "Application",
                "The document has been modified.\n"
                "Do you want to save your changes?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

        if ret == QMessageBox.Save:
            return self.fileSave()

        if ret == QMessageBox.Cancel:
            return False

        return True

    def setCurrentFileName(self, fileName=''):
        self.fileName = fileName
        
        if self.textEdit!=None:
            self.textEdit.document().setModified(False)

        self.setWindowTitle(self.tr("%s[*] - %s" % ("editor", "Java FX IDE by @ DjokerSoft")))
      
        self.setWindowModified(False)

    def fileNew(self):
        print("new")

        
    def fileOpen(self):
        fn, _ = QFileDialog.getOpenFileName(self, "Open File...", None,
                "Code files (*.java);;All Files (*)")

        if fn:
            self.load(fn)


    def reload(self):
        if self.mainProject:
            self.mainProject.srcFiles=[]
            for src in self.listSrc.items:
                self.mainProject.srcFiles.append(src)
            self.mainProject.save()
            

    def fileSave(self):
        print("Save file as ",self.fileName)
        #if not self.fileName:
        #    return self.fileSaveAs()
  


        try:
            with open( self.fileName, 'w') as f:
                f.write(self.textEdit.toPlainText())
              
        except Exception as e:
            print("Error Save File ", self.fileName,":",e)
            return 

        self.textEdit.document().setModified(False)
        self.reload()

    def fileSaveAs(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Save as...", None,
                "Code Files (*.java);;All Files (*)")

        if not fn:
            return False

        
        
        
        self.setCurrentFileName(fn)
        return self.fileSave()




    def textBold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(self.actionTextBold.isChecked() and QFont.Bold or QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)

    def textUnderline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.actionTextUnderline.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textItalic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.actionTextItalic.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)

    def textFamily(self, family):
        fmt = QTextCharFormat()
        fmt.setFontFamily(family)
        self.mergeFormatOnWordOrSelection(fmt)

    def textSize(self, pointSize):
        pointSize = float(pointSize)
        if pointSize > 0:
            fmt = QTextCharFormat()
            fmt.setFontPointSize(pointSize)
            self.mergeFormatOnWordOrSelection(fmt)

 

    def textColor(self):
        col = QColorDialog.getColor(self.textEdit.textColor(), self)
        if not col.isValid():
            return

        fmt = QTextCharFormat()
        fmt.setForeground(col)
        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)

    def textAlign(self, action):
        
        if action == self.actionAlignLeft:
            self.textEdit.setAlignment(Qt.AlignLeft | Qt.AlignAbsolute)
        elif action == self.actionAlignCenter:
            self.textEdit.setAlignment(Qt.AlignHCenter)
        elif action == self.actionAlignRight:
            self.textEdit.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)
        elif action == self.actionAlignJustify:
            self.textEdit.setAlignment(Qt.AlignJustify)

    def currentCharFormatChanged(self, format):
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())


    def cursorPositionChanged(self):
        pass

    def clipboardDataChanged(self):
        self.actionPaste.setEnabled(len(QApplication.clipboard().text()) != 0)

    def about(self):
        QMessageBox.about(self, "About", 
                "This example demonstrates Qt's rich text editing facilities "
                "in action, providing an example document for you to "
                "experiment with.")

    def mergeFormatOnWordOrSelection(self, format):
        
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(format)
        self.textEdit.mergeCurrentCharFormat(format)

    def fontChanged(self, font):
        
        #self.comboFont.setCurrentIndex(self.comboFont.findText(QFontInfo(font).family()))
        #self.comboSize.setCurrentIndex(self.comboSize.findText("%s" % font.pointSize()))
        
        self.actionTextBold.setChecked(font.bold())
        self.actionTextItalic.setChecked(font.italic())
        self.actionTextUnderline.setChecked(font.underline())

    def colorChanged(self, color):
        pix = QPixmap(16, 16)
        pix.fill(color)
        self.actionTextColor.setIcon(QIcon(pix))

 
 
      
        



    def openDialog(self):
        pass

    def printFile(self):
        
        print(self.textEdit.Text())






#def verify(self):
# if self.nameEdit.text() and self.addressEdit.toPlainText():
#self.accept()
 #   return

#answer = QMessageBox.warning(self, "Incomplete Form",
#        "The form does not contain all the necessary information.\n"
#       "Do you want to discard it?",
#                QMessageBox.Yes, QMessageBox.No)

#if answer == QMessageBox.Yes:
#    self.reject()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1400, 880)
    window.show()
    sys.exit(app.exec_())
