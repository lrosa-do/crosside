#!/usr/bin/env python



from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, QFile, QMetaObject,QFileInfo, QRect, QRegExp, QSize, QStringListModel, Qt, QTextCodec, pyqtSlot,QThread,QRunnable, Qt, QThreadPool,pyqtSignal,QObject

from PyQt5.QtGui import (QColor, QCursor, QFont, QFontDatabase, QFontInfo, QIcon, QKeySequence, QPainter,
        QPixmap, QSyntaxHighlighter, QTextBlockFormat, QTextCharFormat, QTextCursor,QFontMetrics,
        QTextDocumentWriter, QTextFormat, QTextListFormat)
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QColorDialog, QProgressBar,QStatusBar,QDesktopWidget,
        QComboBox, QCompleter, QFileDialog, QFontComboBox, QGroupBox, QHBoxLayout, QListWidget, QMainWindow, QMenu, QMessageBox, QPlainTextEdit, QPushButton, QSizePolicy,
        QTextEdit, QToolBar,QSpacerItem,QVBoxLayout)
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
import json

from subprocess import STDOUT, PIPE
import subprocess
import shlex
import argparse
import shutil
import time
import json
import re
import subprocess
from subprocess import check_output, CalledProcessError, STDOUT
from datetime import datetime
import logging
import random
import sys
import time
import http.server
import socketserver


import zipfile

if sys.platform.startswith('darwin'):
    rsrcPath = ":/images/mac"
else:
    rsrcPath = ":/images/win"


nativeManifeste="""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="@apppkg@"     android:versionCode="1" android:versionName="1.0">
            <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
            <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
            <uses-sdk  android:compileSdkVersion="30"     android:minSdkVersion="23"  android:targetSdkVersion="30" />
           <uses-feature android:glEsVersion="0x00020000" android:required="true" />
            <application android:allowBackup="false" android:label="@applbl@" android:icon="@mipmap/ic_icon" >

           <activity android:name="@appactv@"
             android:theme="@android:style/Theme.NoTitleBar.Fullscreen"
             android:configChanges="orientation|keyboardHidden|screenSize"
             android:screenOrientation="landscape" android:launchMode="singleTask"
             android:clearTaskOnLaunch="true">
            <meta-data android:name="android.app.lib_name" android:value="main" />
                               
             <intent-filter>
                  <action android:name="android.intent.action.MAIN" />
                   <category android:name="android.intent.category.LAUNCHER" />
         </intent-filter>
           </activity>
           </application>
</manifest>"""


javaNative="""package @apppkg@; 

public class @appactv@ extends android.app.NativeActivity {
  static {
  System.loadLibrary("main");
 }
}"""
OSP=os.path.sep
ANDROID_SDK="/home/djoker/Android/Sdk"
ANDROID_NDK="/home/djoker/Android/Sdk/ndk/23.0.7599858"
#22.1.7171670"
AAPT       =ANDROID_SDK+'/build-tools/31.0.0/aapt'
DX         =ANDROID_SDK+'/build-tools/31.0.0/dx'
DX8        =ANDROID_SDK+'/build-tools/31.0.0/d8'
ZIPALIGN   =ANDROID_SDK+'/build-tools/31.0.0/zipalign'
APKSIGNER  =ANDROID_SDK+'/build-tools/31.0.0/apksigner'
PLATFORM   =ANDROID_SDK+'/platforms/android-31/android.jar'
JAVA_SDK   ='/usr/lib/jvm/jdk1.8.0_291'
JAVA_LIB_RT='/usr/lib/jvm/jdk1.8.0_291/jre/lib/rt.jar'
JAVAFX     ="/usr/lib/jvm/jdk1.8.0_291/lib/javafx-mx.jar"



PORT = 8080
DIRECTORY = "/media/djoker/code/linux/python/projects/CppEditor/projects/Web/main"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def do_GET(self):
        print("get",self.requestline)
        
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()


SHOW_COMMAND=True
    
        
def runProcess(command, args=[],wait=True):
    args = [command] + args
    def cmd_args_to_str(cmd_args):
        return ' '.join([arg if not ' ' in arg else '"%s"' % arg for arg in cmd_args])
    global SHOW_COMMAND
    if SHOW_COMMAND:
        print("Execute -> ",cmd_args_to_str(args))
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

def call_cmd(command, args=[]):
    args = [command] + args
    result = subprocess.Popen([command], shell=True,close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result.wait()
    chkdata = result.stdout.readlines()
    for line in chkdata:
        lstr=line.decode('utf-8')
        print(lstr)
        

        


def getParentDir(path, level=1):
  return os.path.normpath( os.path.join(path, *([".."] * level)) )

def cleanString(string):
    return "-".join(string.split())

def createPath(root,sub):
    path = os.path.join(os.path.dirname(os.path.abspath(root)), sub)
    print("Create path ",path)
    if not os.path.exists(path):
            os.mkdir(path)

def createFolderTree(maindir):
    if not os.path.exists(maindir):
        try:
                    os.makedirs(maindir)
        except OSError as e:
                 print('Something else happened'+str(e))

rsrcPath = os.getcwd()+os.path.sep+"res"
modulesPath = os.getcwd()+os.path.sep+"modules"
projectsPath = os.getcwd()+os.path.sep+"projects"

#debugs

showSRCLoad=False

isLinux=True
    
    
def LinuxCompile(parent,folderRoot ,name, srcs ,CARGS,CPPARGS, fullBuild=False):
    useCPP=False
    outFolder=folderRoot+os.path.sep+"obj"+os.path.sep+"Linux"+os.path.sep+name
    parent.trace("Build ",outFolder)
    createFolderTree(outFolder)
    objsList=[]
    index=0
    numSrc= len(srcs)
    for src in srcs:
        if not os.path.isfile(src):
            parent.trace("File not exists")
            continue
    
        if parent.IsDone:
            return None

        args=[]
        srcFolder = os.path.dirname(os.path.abspath(src))
        objFolder =outFolder +  srcFolder.replace(folderRoot,"")
        
        createFolderTree(objFolder)
        filename, file_extension = os.path.splitext(src)
        basename = os.path.basename(src)
        basename_without_ext = os.path.splitext(os.path.basename(src))[0]
        objName = objFolder+os.path.sep+basename_without_ext+".o"
        objsList.append(objName)
        src_modified_time = os.path.getmtime(src)
        src_convert_time = time.ctime(src_modified_time)

        index +=1
        parent.setProgress(int((index/numSrc)*100),os.path.basename(src))

        cType = "gcc"
        if len(file_extension)>=3:
                cType="g++"
                useCPP=True
                
        
        if not fullBuild:       
            if os.path.exists(objName):
                obj_modified_time = os.path.getmtime(objName)
                obj_convert_time   = time.ctime(obj_modified_time)
                if (src_convert_time<obj_convert_time):
                    parent.trace("Skip  file"+ src)
                    continue
            
                
    
        
        parent.trace (cType," ",os.path.basename(src),">",os.path.basename(objName))

            
                
        args.append("-c")
        args.append(src)
        args.append("-o")
        args.append(objName)
        

        if useCPP:
            for arg in CPPARGS: 
                value =arg.strip()
                if len(value)>=2:
                    args.append(arg)
                    
        else:
            for arg in CARGS: 
                value =arg.strip()
                if len(value)>=2:
                    args.append(arg)
                    
        #if not isStatic:
        args.append("-fPIC")

                        
            
        code, out, err=runProcess(cType,args)
        #print("err: '{}'".format(str(err)))
        #print("exit: {}".format(code))
        if code!=0:
            parent.trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error: '
            #match = re.compile(rexp, re.DOTALL | re.IGNORECASE).findall(err.decode("utf-8"))
            erro =re.search(rexp,err.decode("utf-8"))
            try:    
                lineY=0
                lineX=0
                if erro:
                    linhas = erro.group().split(":")
                    lineX=int(linhas[2])
                    lineY=int(linhas[1])
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            return None
            
        parent.trace(out.decode("utf-8") )
        
        if parent.IsDone:
            return None
    parent.trace("Compiling completed")
    return objsList
    

def WebCompile(parent,folderRoot ,name, srcs ,CARGS,CPPARGS, fullBuild=False):
    useCPP=False
    outFolder=folderRoot+os.path.sep+"obj"+os.path.sep+"Web"#+os.path.sep
    createFolderTree(outFolder)
    objsList=[]
    

    index=0
    numSrc=len(srcs)
    for src in srcs:
        if not os.path.isfile(src):
            parent.trace("File not exists")
            continue
    
        if parent.IsDone:
            return None
        args=[]
        srcFolder = os.path.dirname(os.path.abspath(src))
        objFolder =outFolder +  srcFolder.replace(folderRoot,"")
        
        createFolderTree(objFolder)
        filename, file_extension = os.path.splitext(src)
        basename = os.path.basename(src)
        basename_without_ext = os.path.splitext(os.path.basename(src))[0]
        objName = objFolder+os.path.sep+basename_without_ext+".o"
        objsList.append(objName)
        src_modified_time = os.path.getmtime(src)
        src_convert_time = time.ctime(src_modified_time)
        
        index +=1
        parent.setProgress(int((index/numSrc)*100),os.path.basename(src))

        cType = "emcc"
        if len(file_extension)>=3:
                cType="em++"
                useCPP=True
                
        
        if not fullBuild:       
            if os.path.exists(objName):
                obj_modified_time = os.path.getmtime(objName)
                obj_convert_time   = time.ctime(obj_modified_time)
                if (src_convert_time<obj_convert_time):
                    parent.trace("Skip  file"+ src)
                    continue
            
                
    
        
        parent.trace (cType," ",os.path.basename(src),">",os.path.basename(objName))

            
                
        args.append("-c")
        args.append(src)
        args.append("-o")
        args.append(objName)
        


        if useCPP:
            for arg in CPPARGS: 
                value =arg.strip()
                if len(value)>=2:
                    args.append(arg)
                    
        else:
            for arg in CARGS: 
                value =arg.strip()
                if len(value)>=2:
                    args.append(arg)
                    


                        
            
        code, out, err=runProcess(cType,args)
        #print("err: '{}'".format(str(err)))
        #print("exit: {}".format(code))
        if code!=0:
            parent.trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error: '
            #match = re.compile(rexp, re.DOTALL | re.IGNORECASE).findall(err.decode("utf-8"))
            erro =re.search(rexp,err.decode("utf-8"))
            try:    
                lineY=0
                lineX=0
                if erro:
                    linhas = erro.group().split(":")
                    lineX=int(linhas[2])
                    lineY=int(linhas[1])
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            return None
        parent.trace(out.decode("utf-8") )
        if parent.IsDone:
            return None
    parent.trace("Compiling completed")
    return objsList
    
       
def AndroidARM7Compile(parent,folderRoot ,name, srcs ,CARGS,CPPARGS, fullBuild=False):
    index=0
    numSrc=len(srcs)
    useCPP=False
    OSP=os.path.sep    
    buildPlataform='23'
    buildOutputArm='armeabi-v7a'
    buildArch='armv7a'
    buildHost='linux-x86_64'
    CC  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/clang'
    CPP =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/clang++'
    #AR  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/arm-linux-androideabi-ar'
    AR  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/llvm-ar'
    
    #STRIP=ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/arm-linux-androideabi-strip'
    STRIP=ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/llvm-strip'


    outFolder=folderRoot+OSP+"obj"+OSP+"Android"+OSP+OSP+buildOutputArm
    binFolder=folderRoot+OSP+"Android"+OSP+OSP+buildOutputArm
    createFolderTree(outFolder)
    createFolderTree(binFolder)
    objsList=[]

    for src in srcs:
        if not os.path.isfile(src):
            parent.trace("File not exists")
            continue
        
        if parent.IsDone:
            return None
    
        args=[]
        srcFolder = os.path.dirname(os.path.abspath(src))
        objFolder =outFolder +  srcFolder.replace(folderRoot,"")
        
        createFolderTree(objFolder)
        filename, file_extension = os.path.splitext(src)
        basename = os.path.basename(src)
        basename_without_ext = os.path.splitext(os.path.basename(src))[0]
        objName = objFolder+os.path.sep+basename_without_ext+".o"
        objsList.append(objName)
        src_modified_time = os.path.getmtime(src)
        src_convert_time = time.ctime(src_modified_time)
        
        
        index +=1
        parent.setProgress(int((index/numSrc)*100),os.path.basename(src))

        cType = CC
        if len(file_extension)>=3:
                cType=CPP
                useCPP=True
                
        
        if not fullBuild:       
            if os.path.exists(objName):
                obj_modified_time = os.path.getmtime(objName)
                obj_convert_time   = time.ctime(obj_modified_time)
                if (src_convert_time<obj_convert_time):
                    parent.trace("Skip  file"+ src)
                    continue
            
                
    
        
        parent.trace (cType," ",os.path.basename(src),">",os.path.basename(objName))

            
        args.append("-target")
        args.append("armv7-none-linux-androideabi"+buildPlataform)
        args.append("-fdata-sections")
        args.append("-ffunction-sections")
        args.append("-fstack-protector-strong")
        args.append("-funwind-tables")
        args.append("-no-canonical-prefixes")
        args.append("-g")
        args.append("-Wno-invalid-command-line-argument")
        args.append("-Wno-unused-command-line-argument")
        args.append("-fno-stack-protector")
        args.append("-fno-exceptions")
        args.append("-fno-rtti")
        args.append("-D_FORTIFY_SOURCE=2")
        args.append("-fpic")
        args.append("-march=armv7-a")
        args.append("-mthumb")
        args.append("-nostdinc++")
        args.append("-Wformat")
        args.append("-Werror=format-security")
        args.append("-Oz")
        

        args.append("-DDNDEBUG")
        args.append("-DANDROID")
        args.append("-DPLATFORM_ANDROID")
        

        args.append("-I"+ANDROID_NDK+"/sources/cxx-stl/llvm-libc++/include")
        args.append("-I"+ANDROID_NDK+"/sources/cxx-stl/llvm-libc++abi/include")
        args.append("-I"+ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include")
        args.append("-I"+ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include/arm-linux-androideabi")

        

        args.append("-I"+folderRoot)    
        args.append("-I"+srcFolder)
        rootFolder=os.getcwd()+OSP+"include"
        args.append("-I"+rootFolder)
        #args.append("-I"+rootFolder+OSP+"SDL2")




        args.append("--sysroot")
        args.append(ANDROID_NDK+"toolchains/llvm/prebuilt/linux-x86_64/sysroot")                
        args.append("-c")
        args.append(src)
        args.append("-o")
        args.append(objName)
        

        if useCPP:
            for arg in CPPARGS: 
                value =arg.strip()
                if len(value)>=2:
                    args.append(arg)
                    print(arg)   
        else:
            for arg in CARGS: 
                value =arg.strip()
                if len(value)>=2:
                    args.append(arg)
                    


                        
            
        code, out, err=runProcess(cType,args)
        #print("err: '{}'".format(str(err)))
        #print("exit: {}".format(code))
        if code!=0:
            parent.trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error: '
            #match = re.compile(rexp, re.DOTALL | re.IGNORECASE).findall(err.decode("utf-8"))
            erro =re.search(rexp,err.decode("utf-8"))
            try:    
                lineY=0
                lineX=0
                if erro:
                    linhas = erro.group().split(":")
                    lineX=int(linhas[2])
                    lineY=int(linhas[1])
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

            return None
        parent.trace(out.decode("utf-8") )
        if parent.IsDone:
            return None
    parent.trace("Compiling completed")
    return objsList
  

def AndroidARM8Compile(parent,folderRoot ,name, srcs ,CARGS,CPPARGS,fullBuild=False):

        index=0
        numSrc=len(srcs)
        useCPP=False
        OSP=os.path.sep    

        buildPlataform ='23'
        buildOutputArm ='arm64-v8a'
        buildArch ='aarch64'
        buildHost ='linux-x86_64'
        CC  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/clang'
        CPP =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/clang++'
        #AR  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/'+buildArch+'-linux-android-ar'
        #STRIP=ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/'+buildArch+'-linux-android-strip'
        #AR  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/arm-linux-androideabi-ar'
        AR  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/llvm-ar'
        
        #STRIP=ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/arm-linux-androideabi-strip'
        STRIP=ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/llvm-strip'
        

        outFolder=folderRoot+OSP+"obj"+OSP+"Android"+OSP+OSP+buildOutputArm
        binFolder=folderRoot+OSP+"Android"+OSP+OSP+buildOutputArm
        createFolderTree(outFolder)
        createFolderTree(binFolder)
        objsList=[]

        
        


        for src in srcs:
            if not os.path.isfile(src):
                parent.trace("File not exists")
                continue
            
            if parent.IsDone:
                return None
        
            args=[]
            srcFolder = os.path.dirname(os.path.abspath(src))
            objFolder =outFolder +  srcFolder.replace(folderRoot,"")
            
            createFolderTree(objFolder)
            filename, file_extension = os.path.splitext(src)
            basename = os.path.basename(src)
            basename_without_ext = os.path.splitext(os.path.basename(src))[0]
            objName = objFolder+os.path.sep+basename_without_ext+".o"
            objsList.append(objName)
            src_modified_time = os.path.getmtime(src)
            src_convert_time = time.ctime(src_modified_time)

            index +=1
            parent.setProgress(int((index/numSrc)*100),os.path.basename(src))

            cType = CC
            if len(file_extension)>=3:
                    cType=CPP
                    useCPP=True
                    
            
            if not fullBuild:       
                if os.path.exists(objName):
                    obj_modified_time = os.path.getmtime(objName)
                    obj_convert_time   = time.ctime(obj_modified_time)
                    if (src_convert_time<obj_convert_time):
                        parent.trace("Skip  file"+ src)
                        continue
                
                    
        
            
            parent.trace (cType," ",os.path.basename(src),">",os.path.basename(objName))

                
            args.append("-target")
            #args.append("aarch64")

                
            args.append(buildArch+"-none-linux-androideabi"+buildPlataform)
            args.append("-fdata-sections")
            args.append("-ffunction-sections")
            args.append("-fstack-protector-strong")
            args.append("-funwind-tables")
            args.append("-fno-exceptions")
            args.append("-fno-rtti")
            args.append("-Wno-invalid-command-line-argument")
            args.append("-Wno-unused-command-line-argument")
            args.append("-D_FORTIFY_SOURCE=2")
            args.append("-fpic")
            args.append("-Oz")
            args.append("-fPIC")
            args.append("-no-canonical-prefixes")
            args.append("-DDNDEBUG")
            args.append("-DANDROID")
            args.append("-DPLATFORM_ANDROID")
            

            args.append("-I"+ANDROID_NDK+OSP+"sources/cxx-stl/llvm-libc++/include")
            args.append("-I"+ANDROID_NDK+OSP+"sources/cxx-stl/llvm-libc++abi/include")
            args.append("-I"+folderRoot)    
            args.append("-I"+srcFolder)
            rootFolder=os.getcwd()+OSP+"include"
            args.append("-I"+rootFolder)
            args.append("-I"+rootFolder+OSP+"SDL2")



            args.append("--sysroot")
            args.append(ANDROID_NDK+"toolchains/llvm/prebuilt/linux-x86_64/sysroot")  
            args.append("-I"+ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include")
            args.append("-I"+ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include/aarch64-linux-android")
                
            args.append("-c")
            args.append(src)
            args.append("-o")
            args.append(objName)
            

            if useCPP:
                for arg in CPPARGS: 
                    value =arg.strip()
                    if len(value)>=2:
                        args.append(arg)
                        print(arg)   
            else:
                for arg in CARGS: 
                    value =arg.strip()
                    if len(value)>=2:
                        args.append(arg)
                        


                            
            
            code, out, err=runProcess(cType,args)
            #print("err: '{}'".format(str(err)))
            #print("exit: {}".format(code))
            if code!=0:
                parent.trace(err.decode("utf-8") )
                rexp=':(.*?):(.*?): error: '
                #match = re.compile(rexp, re.DOTALL | re.IGNORECASE).findall(err.decode("utf-8"))
                erro =re.search(rexp,err.decode("utf-8"))
                try:    
                    lineY=0
                    lineX=0
                    if erro:
                        linhas = erro.group().split(":")
                        lineX=int(linhas[2])
                        lineY=int(linhas[1])
                except Exception as e:
                    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                return None
                    
            parent.trace(out.decode("utf-8") )
            if parent.IsDone:
                return None
        parent.trace("Compiling completed")
        return objsList
          
    
def LinuxBuild(parent,folderRoot ,appName, ListOBJS ,useCPP,LDARGS , BuildType=0):
    args=[]
    cType = "gcc"
    if useCPP:
            cType="g++"
            
    if BuildType==0:
        parent.trace("Build Linux aplication")
        args.append("-o")
        export =folderRoot+os.path.sep+appName
        args.append(export)
        objs=""
        for obj in ListOBJS:
            objs+=obj+' '
            args.append(obj)
        for arg in LDARGS:
            value =arg.strip()
            if len(value)>1:
                args.append(value)
      

        parent.trace("Build to "+cType+" "+appName)
        code, out, err=runProcess(cType,args)
        if code!=0:
            self.trace(err.decode("utf-8") )
            self.trace("Operation Fail  .. ")
            return False         
    if BuildType==1:
        args.append("-shared")
        args.append("-fPIC")
        args.append("-o")
        export =folderRoot+os.path.sep+appName+".so"
        args.append(export)
        objs=""
        for obj in ListOBJS:
            objs+=obj+' '
            args.append(obj)
        #args.append('-s')

        for arg in LDARGS:
            value =arg.strip()
            if len(value)>1:
                args.append(value)
        
        rootFolder=os.getcwd()+os.path.sep+"libs"+os.path.sep+"linux"
        args.append("-L"+rootFolder)
        parent.trace("Build to "+cType+" "+appName)
        code, out, err=runProcess(cType,args)
        if code!=0:
            self.trace(err.decode("utf-8") )
            self.trace("Operation Fail  .. ")
            return False
        
        
    if BuildType==2:
        parent.trace("compile to static lib")
        createFolderTree(folderRoot+os.path.sep+"Linux"+os.path.sep)
        export =folderRoot+os.path.sep+"Linux"+os.path.sep+appName+".a"
        code, out, err=runProcess("rm",["-f",export])
        if code!=0:
            parent.trace(err.decode("utf-8") )
            parent.trace("Operation Fail  .. ")
            return False
        parent.trace(out.decode("utf-8") )

        args.append("-r")
        args.append("-s")
        args.append(export)
        for obj in ListOBJS:
            args.append(obj)

        code, out, err=runProcess("ar",args)
        if code!=0:
            parent.trace(err.decode("utf-8") )
            parent.trace("Operation Fail  .. ")
            return False
        print(out.decode("utf-8") )
        
    parent.trace("Done :) ")
    return True

def WebBuild(parent, folderRoot ,appName, ListOBJS ,useCPP,LDARGS , isStatic=True):
    args=[]

    outFolder=folderRoot+os.path.sep+"Web"+os.path.sep
    createFolderTree(outFolder)
            
    cType = "emcc"
    if useCPP:
            cType="em++"
            
    if isStatic==False:
        parent.trace("Build EMSDK aplication")
        args.append("-o")
        export = outFolder+os.path.sep+appName+".html"
        args.append(export)
        objs=""
        for obj in ListOBJS:
            objs+=obj+' '
            args.append(obj)
        #args.append('-s')


        for arg in LDARGS:
            value =arg.strip()
            if len(value)>1:
                args.append(value)
        rootFolder=os.getcwd()+os.path.sep+"libs"+os.path.sep+"web"
        args.append("-L"+rootFolder)
        parent.trace("Add folder lib:",rootFolder)
    
            
        parent.trace("Build to "+cType+" "+appName)
        code, out, err=runProcess(cType,args)
        if code!=0:
            parent.trace(err.decode("utf-8") )
            parent.trace("Operation Fail  .. ")
            return False
        
        
    
        
        
    if isStatic==True:
        parent.trace("Build EMSDK static lib")
        #export =folderRoot+os.path.sep+appName+".a"
        export =folderRoot+os.path.sep+"Web"+os.path.sep+appName+".a"
        args.append("rcs")
        args.append(export)
        parent.trace("Save to ",export)
        for obj in ListOBJS:
            args.append(obj)
        code, out, err=runProcess("emar",args)
        if code!=0:
            parent.trace(err.decode("utf-8") )
            parent.trace("Operation Fail  .. ")
            return False
    parent.trace("Done :) ")
    return True


def AndroidARM7Build(parent, folderRoot ,name, objsList ,LDARGS,useCPP=False,isStatic=True):
    print("Build Android ARM 7")
    
    OSP=os.path.sep    
    buildPlataform='23'
    buildOutputArm='armeabi-v7a'
    buildArch='armv7a'
    buildHost='linux-x86_64'
    CC  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/clang'
    CPP =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/clang++'
    #AR  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/arm-linux-androideabi-ar'
    AR  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/llvm-ar'
    
    #STRIP=ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/arm-linux-androideabi-strip'
    STRIP=ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/llvm-strip'

    outFolder=folderRoot+OSP+"obj"+OSP+"Android"+OSP+buildOutputArm
    binFolder=folderRoot+OSP+"Android"+OSP+buildOutputArm
    createFolderTree(outFolder)
    createFolderTree(binFolder)
    cType=CC

    if isStatic==False:
        args=[]
        export = binFolder+OSP+"lib"+name+".so"
        parent.trace("Build app ",buildArch," ",export )
        args.append("-Wl,-soname,"+"lib"+name+".so")
        args.append("-shared")
        objs=""
        for obj in objsList:
            objs+=obj+' '
            args.append(obj)
        
        #if linkCPP:        
        args.append(ANDROID_NDK+"/sources/cxx-stl/llvm-libc++/libs/armeabi-v7a/libc++_static.a")
        args.append(ANDROID_NDK+"/sources/cxx-stl/llvm-libc++abi/../llvm-libc++/libs/armeabi-v7a/libc++abi.a")
        #args.append(ANDROID_NDK+"/sources/cxx-stl/llvm-libc++/libs/armeabi-v7a/libunwind.a")

        for arg in LDARGS:
            value =arg.strip()
            if len(value)>1:
                args.append(value)

        args.append("-Wl,--no-whole-archive")
        #args.append("-lgcc")
        args.append("-Wl,--exclude-libs,libgcc.a")
        args.append("-Wl,--exclude-libs,libgcc_real.a")
        args.append("-latomic")
        args.append("-Wl,--exclude-libs,libatomic.a")
        args.append("-target")
        args.append(buildArch+"-none-linux-androideabi"+buildPlataform)
        args.append("-no-canonical-prefixes")
        args.append("-Wl,--build-id")
        args.append("-Wl,--exclude-libs,libunwind.a")
        args.append("-nostdlib++")
        args.append("-Wl,--no-undefined")
        args.append("-Wl,--fatal-warnings")
        
        
        args.append("-L"+ANDROID_NDK+"platforms/android-"+buildPlataform+"/arch-arm/usr/lib")
        args.append("-L"+ANDROID_NDK+"/sources/cxx-stl/llvm-libc++/libs/armeabi-v7a")
        rootFolder=os.getcwd()+"/libs/android/"+buildOutputArm
        args.append("-L"+rootFolder)
        args.append("-L"+ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/lib")  
        if useCPP:
            args.append("-lc++_static")
            args.append("-lc++abi")
            cType=CPP
        args.append("-o")
        args.append(export)
        

        
            
        

        code, out, err=runProcess(cType,args)
        if code!=0:
            parent.trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error:'
            return False
        parent.trace(out.decode("utf-8"))


        parent.trace("Strip library ")
        code, out, err=runProcess(STRIP,["--strip-unneeded",export])
        if code!=0:
            parent.trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error:'
            return False
        parent.trace(out.decode("utf-8"))
        parent.trace("Native ARM7 Done :) ")
        return True
            
    
    

    if isStatic==True:
        parent.trace("Build Android ARM7 static lib")
        args=[]
        export = binFolder+OSP+"lib"+name+".a"
        args.append("rcs")
        args.append(export)
        objs=""
        for obj in objsList:
            objs+=obj+' '
            args.append(obj)
        code, out, err=runProcess(AR,args)
        if code!=0:
            parent.trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error:'
            return False
        parent.trace(out.decode("utf-8"))
        parent.trace("Static ARM7 build completed :) ")
        return True    
    return False

def AndroidARM8Build(parent,folderRoot ,name,objsList, LDARGS,useCPP=True,isStatic=True):
    print("Build Android ARM 8")
    
    OSP=os.path.sep    
    buildPlataform ='23'
    buildOutputArm ='arm64-v8a'
    buildArch ='aarch64'
    buildHost ='linux-x86_64'
    CC  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/clang'
    CPP =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/clang++'
    #AR  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/'+buildArch+'-linux-android-ar'
    #STRIP=ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/'+buildArch+'-linux-android-strip'
    #AR  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/arm-linux-androideabi-ar'
    AR  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/llvm-ar'
    
    #STRIP=ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/arm-linux-androideabi-strip'
    STRIP=ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/llvm-strip'
    

    outFolder=folderRoot+OSP+"obj"+OSP+"Android"+OSP+buildOutputArm
    binFolder=folderRoot+OSP+"Android"+OSP+buildOutputArm
    createFolderTree(outFolder)
    createFolderTree(binFolder)

    if isStatic==False:
        print("Build Shared Android ARM 8")
        args=[]
        export = binFolder+OSP+"lib"+name+".so"
        parent.trace("Build app ",buildArch," ",export )
        args.append("-Wl,-soname,"+"lib"+name+".so")
        args.append("-Wl,--exclude-libs,libatomic.a ")
        args.append("-Wl,--build-id")
        args.append("-Wl,--no-undefined")
        args.append("-Wl,-z,noexecstack")
        args.append("-Wl,-z,relro")
        args.append("-Wl,-z,now")
        args.append("-Wl,--warn-shared-textrel")
        args.append("-Wl,--fatal-warnings")
        args.append("-target")
        args.append(buildArch+"-none-linux-androideabi"+buildPlataform)
        args.append("-shared")

        objs=""
        for obj in objsList:
            objs+=obj+' '
            args.append(obj)
        
        #if useCPP:
        args.append(ANDROID_NDK+"/sources/cxx-stl/llvm-libc++/libs/"+buildOutputArm+"/libc++_static.a")
        args.append(ANDROID_NDK+"/sources/cxx-stl/llvm-libc++abi/../llvm-libc++/libs/"+buildOutputArm+"/libc++abi.a")
        

        for arg in LDARGS:
            value =arg.strip()
            if len(value)>1:
                args.append(value)

        
        
        args.append("-L"+ANDROID_NDK+"/sources/cxx-stl/llvm-libc++/libs/"+buildOutputArm)
        rootFolder=os.getcwd()+OSP+"libs"+OSP+"android"+OSP+buildOutputArm
        args.append("-L"+rootFolder)
        args.append("-L"+ANDROID_NDK+"toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/lib")  
        if useCPP:
            args.append("-lc++_static")
            args.append("-lc++abi")
            cType=CPP
        args.append("-o")



        args.append(export)

        
            
        

        code, out, err=runProcess(cType,args)
        if code!=0:
            parent.trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error:'
            return False
        parent.trace(out.decode("utf-8"))


        parent.trace("Strip library ")
        code, out, err=runProcess(STRIP,["--strip-unneeded",export])
        if code!=0:
            parent.trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error:'
            return False
        parent.trace(out.decode("utf-8"))
        parent.trace("Native ARM8 Done :) ")
        return True
    
            
    
    

    if isStatic==True:
        parent.trace("Build Android ARM8 static lib")
        args=[]
        export = binFolder+OSP+"lib"+name+".a"
        args.append("rcs")
        args.append(export)
        objs=""
        for obj in objsList:
            objs+=obj+' '
            args.append(obj)
        code, out, err=runProcess(AR,args)
        if code!=0:
            parent.trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error:'
            return False
        parent.trace(out.decode("utf-8"))
        args=[]
        export = binFolder+OSP+"lib"+name+".a"
        args.append("-t")
        args.append(export)
        objs=""
        for obj in objsList:
            objs+=obj+' '
            args.append(obj)
        code, out, err=runProcess(AR,args)
        if code!=0:
            parent.trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error:'
            return False
        parent.trace(out.decode("utf-8"))
        parent.trace("Static Android ARM8 build completed :) ")
        return True
    return False           
    
class ConsoleText(QPlainTextEdit):
    def __init__(self,  parent=None):
        super(ConsoleText, self).__init__(parent)
        self.setReadOnly(True)

    
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        clrAct = contextMenu.addAction("Clear")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == clrAct:
            self.clear()
         





class Args:
    def __init__(self):
        self.ARGCPP=[]
        self.ARGCC=[]
        self.ARGLD=[]
    def addCPP(self, value):
        if not value in self.ARGCPP:
            self.ARGCPP.append(value)
    def addCC(self, value):
        if not value in self.ARGCC:
            self.ARGCC.append(value)
    def addLD(self, value):
        if not value in self.ARGLD:
            self.ARGLD.append(value)
    def clear(self):
        self.ARGCPP.clear()
        self.ARGCC.clear()
        self.ARGLD.clear()
        

class ArgsAndroid(Args):
    def __init__(self):
        super(ArgsAndroid, self).__init__()
        self.PACKAGE=""        
        self.ACTIVITY=""

class ArgsWeb(Args):
    def __init__(self):
        super(ArgsWeb, self).__init__()
        self.SHELL=""        
        
class ArgsDesktop(Args):
    def __init__(self):
        super(ArgsDesktop, self).__init__()
        self.SHELL=""        
        

class SrcCode:
    def __init__(self,plataform):
        self.Plataform=plataform
        self.Src=[]
        self.Objs=[]
        self.Include=[]
        self.ARGS=Args()
        self.ARGSDESKTOP=ArgsDesktop()
        self.ARGSANDROID=ArgsAndroid()
        self.ARGSWEB=ArgsWeb()
    


class AppProgress(QDialog):
    def __init__(self,parent):
        super(AppProgress, self).__init__(parent)
        self.resize(449, 155)
        self.parent=parent
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle(u"Progress")
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        self.progressBar = QProgressBar(self)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 3)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)
        self.lineEdit.setReadOnly(True)
        font = QFont()
        font.setPointSize(13)
        self.lineEdit.setFont(font)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setInputMask(u"")
        self.lineEdit.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 3)

        self.horizontalSpacer = QSpacerItem(167, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.pushButton = QPushButton(self)
        self.pushButton.setText("Abort")
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)
        self.horizontalSpacer_2 = QSpacerItem(166, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 2, 1, 1)

        self.pushButton.pressed.connect(self.abort)
        self.OnAbort=None
        self.show()
        
        
        QMetaObject.connectSlotsByName(self)    
    def setup(self,min,max,onClose):
        self.progressBar.setRange(min,max)
        self.progressBar.setValue(min)
        self.OnAbort=onClose
        
    def trace(self,*args):
        result = ""
        for x in args:
            result += str(x)
        self.lineEdit.setText(result)
        
        
        
    def setProgress(self,value,code):
        self.progressBar.setValue(value)
        self.lineEdit.setText(code)
        #print("Compile ",code," ",value)


    def abort(self):
        self.close()
        
    def closeEvent(self, event):
        event.accept()


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    isDone=False
    def run(self):
        try:
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                print("Serving at port", PORT)
                #httpd.RequestHandlerClass.directory=DIRECTORY
                httpd.serve_forever()
            while (not self.isDone):
                pass
            httpd.server_close()
        
        except  Exception as error:
            print(" Error  Startin Server :",error)  
        

class AppServer(QDialog):
    def __init__(self,parent):
        super(AppServer, self).__init__(parent)
        self.resize(438, 307)
        self.setWindowTitle(u"HTTP Server")
        self.mainWindo=parent
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        self.plainTextEdit = QPlainTextEdit(self)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setPlainText(u"")
        self.gridLayout.addWidget(self.plainTextEdit, 0, 0, 1, 1)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.buttonBox.accepted.connect(self.cancel)
        self.buttonBox.rejected.connect(self.cancel)
        self.thread = QThread()
        self.worker = Worker()
        self.thread.setTerminationEnabled(True)
        QMetaObject.connectSlotsByName(self)


    
    
    def start(self,path):
        self.path=path
        self.plainTextEdit.appendPlainText("Start web host on Port 8080")
        try:
        
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.reportProgress)
        
            self.thread.start()
        except  Exception as error:
            print(" Error  Startin Server :",error)  

    
        self.show()

    def reportProgress(self,index):
        print("index",index)

    def cancel(self):
        self.worker.isDone=True
        try:
            self.thread.terminate()
            self.thread.wait(100)
            
        except  Exception as error:
            print(" Error  Stoping Server :",error)  
        
        self.close()
        pass

class BuildWorker(QtCore.QThread):
    def __init__(self, MainWindow,plataform,folderRoot ,appName, ListOBJS ,useCPP,LDARGS , isStatic):
        super(self.__class__, self).__init__(MainWindow)
        self.MainWindow=MainWindow
        self.Plataform  =plataform
        self.FolderRoot =folderRoot
        self.AppName   =appName
        self.ListOBJS =ListOBJS
        self.UseCPP   =useCPP
        self.LDARGS  =LDARGS
        self.IsStatic=isStatic

    def run(self):
        pass

    def stop(self):
        self.wait()
    
    def trace(self,*args):
        #self.MainWindow.trace(*args)
        pass

   

class RunWorker(QThread):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.isDone=False
        self.parent=parent
        self.progress = AppProgress(self.parent)
        self.progress.setup(0,10,self.OnAbort)
        
    def OnAbort(self):
         print("abort")
         self.isDone=True
         self.stop()


    def run(self):
        for i in range(10):
            if self.isDone:
                logging.info(f"Abort")
                break
            
            self.progress.setProgress(i + 1,f"Working in thread  step {i + 1}/5")
            time.sleep(random.randint(700, 2500) / 1000)
            self.parent.MainConsole.appendPlainText(f"Working in thread  step {i + 1}/5")
            
        


    def stop(self):
        self.wait()
        
class ExecuteWorker(QThread):
    def __init__(self, parent,App):
        super(self.__class__, self).__init__(parent)
        self.isDone=False
        self.parent=parent
        self.app=App
        
    def execute(self,cmd,args):
        args = [cmd] + args
        re = subprocess.Popen(args, shell=False,close_fds=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #re.wait()
        chkdata = re.stdout.readlines()
        for line in chkdata:
            lstr=line.decode('utf-8')
            #self.parent.trace(lstr)
            #self.parent.MainConsole.appendPlainText(lstr)
            print(lstr)
            
    def OnAbort(self):
         print("abort")
         self.isDone=True
         self.stop()

    def stop(self):
        self.wait()
        
    def run(self):
        try:
            self.execute(self.app,[])
            
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

        print("Done")
        
class TestWorker(QThread):
    def __init__(self, parent):
        super(self.__class__, self).__init__(parent)
        self.isDone=False
        self.parent=parent
        self.progress = AppProgress(self.parent)
        self.progress.setup(0,10,self.OnAbort)
        
    def OnAbort(self):
         print("abort")
         self.isDone=True
         self.stop()

    def stop(self):
        self.wait()
        
    def run(self):
        for i in range(10):
            if self.isDone:
                print("Abort")
                break
            print(f"Working in thread  step {i + 1}/5")
            self.progress.setProgress(i + 1,f"Working in thread  step {i + 1}/5")
            time.sleep( 2500 / 1000)
            
        print("Done")
        
class CompileWorker(QThread):
    def __init__(self, parent,plataform,folderRoot ,appName, ListSrc ,useCPP,CPPARGS,CCARGS):
        super(self.__class__, self).__init__(parent)
        self.parent = parent
        self.Plataform  =plataform
        self.FolderRoot =folderRoot
        self.AppName   =appName
        self.SrcList = ListSrc
        self.UseCPP   =useCPP
        self.CPPARGS  =CPPARGS
        self.CCARGS  =CCARGS
        self.IsDone=False
        self.AppProgress = AppProgress(self.parent)
        self.AppProgress.setup(0,len(self.SrcList),self.OnAbort)
        
        
        
    def OnAbort(self):
        print("Abort ...")
        self.IsDone=True
        self.stop()
        self.AppProgress.close()


    def run(self):
           
        if self.Plataform==0:
            self.LinuxCompile(self.FolderRoot ,self.AppName, self.SrcList ,self.CCARGS,self.CPPARGS)
        if self.Plataform==2:
            self.WebCompile(self.FolderRoot ,self.AppName, self.SrcList ,self.CCARGS,self.CPPARGS)
        self.AppProgress.close()
        print("Done")
    

    def stop(self):
        self.wait()
        
        
    
    def trace(self,*args):
        #self.parent.trace(*args)
        self.AppProgress.trace(args)
        pass

                                




class CppModule:
    def __init__(self,parent):
        self.Dir=""
        self.Name=""
        self.About=""
        self.Version=""
        self.System=[]
        self.Depends=[]
        self.MainSrc=SrcCode("Main")
        self.DesktopSrc=SrcCode("Desktop")
        self.AndroidSrc=SrcCode("Android")
        self.WebSrc=SrcCode("Web")
        self.MainWindow=parent
        self.IsDone=False


    def trace(self,*args):
        self.MainWindow.trace(*args)
        
    def setProgress(self,value,code):
        print("Compile ",code," ",value,"%")
    
    def load(self,fileName):
        pass

    def compileAndroid(self,arm7=True,arm8=True):
        self.MainWindow.ClearConsole()
        self.MainWindow.trace("Compile Android")
        self.MainWindow.trace("Compile:",self.Name)
        self.MainWindow.trace("Path:",self.Dir)
        self.MainWindow.trace("About:",self.About)
        self.MainWindow.trace("Version:",self.Version)


        ARGCC =[]
        ARGCPP =[]
        ARGLD =[]

        ARGCC.append("-I"+self.Dir+os.path.sep+"src")
        ARGCPP.append("-I"+self.Dir+os.path.sep+"src")
        ARGCPP.append("-I"+self.Dir+os.path.sep+"include")
        ARGCC.append("-I"+self.Dir+os.path.sep+"include")
        
        for arg in self.MainSrc.ARGS.ARGCPP:
            ARGCPP.append(arg)

        for arg in self.MainSrc.ARGS.ARGCC:
            ARGCC.append(arg)

        for arg in self.MainSrc.ARGS.ARGLD:                        
            ARGLD.append(arg)

        for arg in self.AndroidSrc.ARGS.ARGCPP:
            ARGCPP.append(arg)

        for arg in self.AndroidSrc.ARGS.ARGCC:
            ARGCC.append(arg)
            
        for arg in self.AndroidSrc.ARGS.ARGLD:                        
            ARGLD.append(arg)




        code = []
        for src in self.MainSrc.Src:
            code.append(self.Dir+os.path.sep+src)
           
        for src in self.AndroidSrc.Src:
            code.append(self.Dir+os.path.sep+src)
        

        if arm7:
            objs=AndroidARM7Compile(self,self.Dir,self.Name,code,ARGCC,ARGCPP)
            if objs:
                AndroidARM7Build(self,self.Dir,self.Name,objs,ARGLD)
                
        if arm8:
            objs=AndroidARM8Compile(self,self.Dir,self.Name,code,ARGCC,ARGCPP)
            
            if objs:
                print(objs)
                AndroidARM8Build(self,self.Dir,self.Name,objs,ARGLD,True)
                
                
                    
    
    def compileWeb(self):
        self.MainWindow.ClearConsole()
        self.MainWindow.trace("Compile Emscripten")
        self.MainWindow.trace("Compile:",self.Name)
        self.MainWindow.trace("Path:",self.Dir)
        self.MainWindow.trace("About:",self.About)
        self.MainWindow.trace("Version:",self.Version)


        ARGCC =[]
        ARGCPP =[]
        ARGLD =[]

        ARGCC.append("-I"+self.Dir+os.path.sep+"src")
        ARGCPP.append("-I"+self.Dir+os.path.sep+"src")
        ARGCPP.append("-I"+self.Dir+os.path.sep+"include")
        ARGCC.append("-I"+self.Dir+os.path.sep+"include")
        
        for arg in self.MainSrc.ARGS.ARGCPP:
            ARGCPP.append(arg)

        for arg in self.MainSrc.ARGS.ARGCC:
            ARGCC.append(arg)

        for arg in self.MainSrc.ARGS.ARGLD:                        
            ARGLD.append(arg)

        for arg in self.WebSrc.ARGS.ARGCPP:
            ARGCPP.append(arg)

        for arg in self.WebSrc.ARGS.ARGCC:
            ARGCC.append(arg)
            
        for arg in self.WebSrc.ARGS.ARGLD:                        
            ARGLD.append(arg)




        code = []
        for src in self.MainSrc.Src:
            code.append(self.Dir+os.path.sep+src)
           
        for src in self.WebSrc.Src:
            code.append(self.Dir+os.path.sep+src)
        
        #self.worker = CompileWorker(self.MainWindow,2,self.Dir,self.Name,code,True,ARGCPP,ARGCC)
        #self.worker.start()
        objs = WebCompile(self, self.Dir,self.Name,code,ARGCC,ARGCPP)
        if objs:
            WebBuild(self,self.Dir,self.Name,objs,True,ARGLD,True)
        
        



    def clean(self):
        try:
            self.MainWindow.ClearConsole()
            self.MainWindow.trace("Clean:",self.Name)
            #code.append(self.Dir+os.path.sep+src)
            for root, dirs, files in os.walk(self.Dir+os.path.sep+"obj"):
                for file in files:
                    fullName=os.path.join(root, file)
                    isFile = os.path.isfile(fullName)
                    if isFile:
                        os.remove(fullName)
                   
            if  os.path.exists(self.Dir+os.path.sep+"obj"):
                shutil.rmtree(self.Dir+os.path.sep+"obj")
        except Exception as e:
            self.MainWindow.trace('Error on line :',sys.exc_info()[-1].tb_lineno,str(e))
          
 


    def compileDesktop(self):
        self.MainWindow.ClearConsole()
        self.MainWindow.trace("Compile Desktop")
        self.MainWindow.trace("Compile:",self.Name)
        self.MainWindow.trace("Path:",self.Dir)
        self.MainWindow.trace("About:",self.About)
        self.MainWindow.trace("Version:",self.Version)

        self.MainSrc.ARGS.ARGCC.append("-I"+self.Dir+os.path.sep+"src")
        self.MainSrc.ARGS.ARGCC.append("-I"+self.Dir+os.path.sep+"src")
        self.MainSrc.ARGS.ARGCC.append("-I"+self.Dir+os.path.sep+"include")
        self.MainSrc.ARGS.ARGCC.append("-I"+self.Dir+os.path.sep+"include")


        ARGCC =[]
        ARGCPP =[]
        ARGLD =[]

        ARGCC.append("-I"+self.Dir+os.path.sep+"src")
        ARGCPP.append("-I"+self.Dir+os.path.sep+"src")
        ARGCPP.append("-I"+self.Dir+os.path.sep+"include")
        ARGCC.append("-I"+self.Dir+os.path.sep+"include")
        

        for arg in self.MainSrc.ARGS.ARGCPP:
            ARGCPP.append(arg)

        for arg in self.MainSrc.ARGS.ARGCC:
            ARGCC.append(arg)

        for arg in self.MainSrc.ARGS.ARGLD:                        
            ARGLD.append(arg)

        for arg in self.DesktopSrc.ARGS.ARGCPP:
            ARGCPP.append(arg)

        for arg in self.DesktopSrc.ARGS.ARGCC:
            ARGCC.append(arg)
            
        for arg in self.DesktopSrc.ARGS.ARGLD:                        
            ARGLD.append(arg)


        code = []
        for src in self.MainSrc.Src:
            code.append(self.Dir+os.path.sep+src)
           
        for src in self.DesktopSrc.Src:
            code.append(self.Dir+os.path.sep+src)
        
        #self.worker=TestWorker(self.MainWindow)
        #self.worker = CompileWorker(self.MainWindow,0,self.Dir,self.Name,code,True,ARGCPP,ARGCC)
        #self.worker.start()
        #wr = TestWorker(self.MainWindow)
        #wr.start()
        #for obj in self.DesktopSrc.Objs:
        #    self.MainWindow.trace ("Build ",obj)
        
        #print(self.MainSrc.ARGS.ARGCC)
        #print(self.MainSrc.ARGS.ARGCPP)
        #print(self.MainSrc.ARGS.ARGLD)
        

        objs = LinuxCompile(self, self.Dir,self.Name,code,ARGCC,ARGCPP)
        if objs:
            LinuxBuild(self,self.Dir,self.Name,objs,True,ARGLD,2)
           
           
        

class Project:
    def __init__(self,parent):
        self.Dir=projectsPath
        self.Root=""
        self.FileName="untitled.c"
        self.Name=""
        self.Modules=[]
        self.Src=SrcCode("Main")
        self.MainWindow=parent
        self.IsDone=False
            
    def trace(self,*args):
        self.MainWindow.trace(*args)
        
    def setProgress(self,value,code):
        print("Compile ",code," ",value,"%")

    def addSrc(self,code):
        if not code in self.Src.Src:
            print("add ",code)
            self.Src.Src.append(code)
            
    def removeSrc(self,code):
        if  code in self.Src.Src:
            self.Src.Src.remove(code)

    def addModule(self,code):
        if not code in self.Modules:
            print("add module",code)
            self.Modules.append(code)
            
    def removeModule(self,code):
        if  code in self.Modules:
            self.Modules.remove(code)

    def cleanAndroid(self):
        pass
    def cleanDesktop(self):
        export =self.Dir+os.path.sep+self.Name
        if os.path.isfile(export):
            os.remove(export)
        shutil.rmtree(self.Dir+os.path.sep+"obj"+os.path.sep+"Linux")


    def cleanWeb(self):
        pass
    
    def clean(self,plataform):
        print("clean ",plataform," ",self.Name," ",self.Dir)
        try:
            if plataform==0:
                self.cleanDesktop()
            
            if plataform==1:
                self.cleanAndroid()

            if plataform==2:
                self.cleanWeb()


        except  Exception as error:
            print(" Error  cleaning project :",error) 


    def runAndroid(self):
        pass


    def runDesktop(self):
        export =self.Dir+os.path.sep+self.Name
        if os.path.isfile(export):
            self.trace("Running  "+export)
            code, out, err=runProcess(export,[],False)
            if code!=0:
                self.trace(err.decode("utf-8") )
                return
            self.trace(out.decode("utf-8"))
    
    def runWeb(self):
        outFolder=self.Dir+os.path.sep+"Web"+os.path.sep+self.Name
        

    def run(self,plataform):
        print("run ",plataform," ",self.Name," ",self.Dir)
        try:
            if plataform==0:
                self.runDesktop()
            
            if plataform==1:
                self.runAndroid()

            if plataform==2:
                self.runWeb()
        except  Exception as error:
            print(" Error  run  File:",error)

    def compile(self,plataform):
        print("compile ",plataform," ",self.Name," ",self.Dir)
        try:
            if plataform==0:
                self.compileDesktop()
            
            if plataform==1:
                self.compileAndroid()

            if plataform==2:
                self.compileWeb()

        except  Exception as error:
            print(" Error  Compilimg project :",error)

    def compileDesktop(self):
        Objs=None
        Objs=self.LinuxCompile(self.Dir,self.Name)
        if Objs:
            self.LinuxBuild(self.Dir,self.Name,Objs,True)


    def compileAndroid(self):
        print("compile android")
        arm7=True
        arm8=True
        
        buildWithCpp=False
        
        srcs=[]
        for src in self.Src.Src:
            srcs.append(src)
            filename, file_extension = os.path.splitext(src)
            print(file_extension,len(file_extension))
            #if len(file_extension)>=3:
            #
            buildWithCpp=True
            
            
        ARGCPP=[]
        for arg in self.Src.ARGSANDROID.ARGCPP: 
            value =arg.strip()
            if len(value)>=2:
                ARGCPP.append(arg)
        ARGCC=[]
        for arg in self.Src.ARGSANDROID.ARGCC: 
            value =arg.strip()
            if len(value)>=2:
                ARGCC.append(arg)
                        
        ARGLD=[]
        for arg in self.Src.ARGSANDROID.ARGLD: 
            value =arg.strip()
            if len(value)>=2:
                ARGLD.append(arg)
                        

        if arm7:
            objs=AndroidARM7Compile(self,self.Dir,self.Name,srcs,ARGCC,ARGCPP)
            if objs:
                AndroidARM7Build(self,self.Dir,self.Name,objs,ARGLD,buildWithCpp,False)
                
        if arm8:
            objs=AndroidARM8Compile(self,self.Dir,self.Name,srcs,ARGCC,ARGCPP)
            if objs:
                AndroidARM8Build(self,self.Dir,self.Name,objs,ARGLD,buildWithCpp,False)
      
        
        
    def compileWeb(self):
        Objs=self.WebCompile(self.Dir,self.Name)
        if Objs:
            self.WebBuild(self.Dir,self.Name,Objs,True)
            
    



    
    def saveArg(self,f,plat):
        cppargs=""
        ccargs=""
        ldargs=""

        if plat==0:
            for arg in self.Src.ARGSDESKTOP.ARGCPP:
                cppargs+" "+arg
            for arg in self.Src.ARGSDESKTOP.ARGCC:
                ccargs+" "+arg
            for arg in self.Src.ARGSDESKTOP.ARGLD:
                ldargs+" "+arg                

            f.write('"Desktop" :{\n')
            f.write('"CPP":"'+cppargs+'",\n')
            f.write('"CC":"'+ccargs+'",\n')
            f.write('"LD":"'+ldargs+'"\n')
            f.write('},\n')
        if plat==1:
            for arg in self.Src.ARGSANDROID.ARGCPP:
                cppargs+" "+arg
            for arg in self.Src.ARGSANDROID.ARGCC:
                ccargs+" "+arg
            for arg in self.Src.ARGSANDROID.ARGLD:
                ldargs+" "+arg                

            f.write('"Android" :{\n')
            f.write('"PACKAGE":"'+self.Src.ARGSANDROID.PACKAGE+'",\n')
            f.write('"ACTIVITY":"'+self.Src.ARGSANDROID.ACTIVITY+'",\n')
            f.write('"CPP":"'+cppargs+'",\n')
            f.write('"CC":"'+ccargs+'",\n')
            f.write('"LD":"'+ldargs+'"\n')
            f.write('},\n')
        if plat==2:
            for arg in self.Src.ARGSWEB.ARGCPP:
                cppargs+" "+arg
            for arg in self.Src.ARGSWEB.ARGCC:
                ccargs+" "+arg
            for arg in self.Src.ARGSWEB.ARGLD:
                ldargs+" "+arg                

            f.write('"Web" :{\n')
            f.write('"SHELL":"'+self.Src.ARGSWEB.SHELL+'",\n')
            f.write('"CPP":"'+cppargs+'",\n')
            f.write('"CC":"'+ccargs+'",\n')
            f.write('"LD":"'+ldargs+'"\n')
            f.write('},\n')

    def load(self,fileName):
        try:
            self.FileName=fileName
            
            self.Name=os.path.splitext(os.path.basename(self.FileName))[0]
            self.Dir=os.path.dirname(os.path.abspath(self.FileName))
            
            self.Root=self.Dir+OSP+os.path.basename(self.FileName)
            
            self.trace("Load  (",self.Name,") Project")
            self.trace("Path  ",self.Dir)
            self.trace("Root  ",self.Root)
            with open(self.FileName, 'r') as data:
                jdata = json.load(data)
                #print(jdata)        
                #self.Dir=jdata["path"] ?????
                modules=jdata["module"]
                for module in modules:
                    self.addModule(module)
                srcs=jdata["src"]
                for src in srcs:
                    self.addSrc(src)
                
                mainOpts=jdata["Main"]
                desktopOpts=jdata["Desktop"]
                androidOpts=jdata["Android"]
                webOpts    =jdata["Web"]
                




        except  Exception as error:
            print(" Error  Loading  File:",error)   
        

  
    def save(self,fileName):
        if fileName==None:
            fileName=self.FileName
        else:
            self.FileName=fileName

        try:
            self.Name=os.path.splitext(os.path.basename(self.FileName))[0]
            self.Dir=os.path.dirname(os.path.abspath(self.FileName))
            with open(self.FileName, 'w') as f:
                f.write('{ \n')
                
                f.write('"path" :"'+self.Dir+'",\n')
                
                

                numModules  =len(self.Modules)
                numSrcFiles =len(self.Src.Src)

                f.write('"modules" :'+str(numModules)+',\n')
                f.write('"srcs" :'+str(numSrcFiles)+',\n')




                print('Modules',numModules)
                print("Src Files",numSrcFiles)

                if numModules==0:
                    f.write('"module" :[""],\n')
                
                if numModules==1:
                    f.write('"module":[')
                    f.write('"'+self.Modules[0]+'"')
                    f.write('],\n')

                if numModules>1:
                    f.write('"module":[')
                    for i in range(numModules-1):
                        f.write('"'+self.Modules[i]+'",')
                    f.write('"'+self.Modules[numModules-1]+'"')
                    f.write('],\n')

     
                
                if numSrcFiles==0:
                    f.write('"src":[""],\n')
                
                if numSrcFiles==1:
                    f.write('"src":[')
                    f.write('"'+self.Src.Src[0]+'"')
                    f.write('],\n')

                if numSrcFiles>1:
                    f.write('"src" :[')
                    for i in range(numSrcFiles-1):
                        print(i)
                        f.write('"'+self.Src.Src[i]+'",')
                    f.write('"'+self.Src.Src[numSrcFiles-1]+'"')
                    f.write('],\n')
                


                self.saveArg(f,0)
                self.saveArg(f,1)
                self.saveArg(f,2)

                cppargs=""
                ccargs=""
                ldargs=""

                for arg in self.Src.ARGS.ARGCPP:
                    cppargs+" "+arg
                for arg in self.Src.ARGS.ARGCC:
                    ccargs+" "+arg
                for arg in self.Src.ARGS.ARGLD:
                    ldargs+" "+arg                

                f.write('"Main" :{\n')
                f.write('"CPP":"'+cppargs+'",\n')
                f.write('"CC":"'+ccargs+'",\n')
                f.write('"LD":"'+ldargs+'"\n')
                f.write('},\n')          
                    
                

                f.write('}\n')
        except  Exception as error:
            print(" Error  Saving  File:",error)             


    def LinuxBuild(self, folderRoot ,appName, ListOBJS ,useCPP):
            if not ListOBJS or not folderRoot or not appName:
                return False
            if len(ListOBJS)<=0:
                return False
            

            args=[]
            cType = "gcc"
            if useCPP:
                    cType="g++"
            self.MainWindow.trace("Build Linux aplication")
            args.append("-o")
            export =folderRoot+os.path.sep+appName
            args.append(export)
            objs=""
            for obj in ListOBJS:
                objs+=obj+' '
                args.append(obj)
            #args.append('-s')

            for arg in self.Src.ARGSDESKTOP.ARGLD:
                value =arg.strip()
                if len(value)>1:
                    args.append(value)
            rootFolder=os.getcwd()+os.path.sep+"libs"+os.path.sep+"linux"
            args.append("-L"+rootFolder)
            
            self.trace("Build  "+appName)
            code, out, err=runProcess(cType,args)
            if code!=0:
                self.MainWindow.trace(err.decode("utf-8") )
                self.MainWindow.trace("Operation Fail  .. ")
                return False
            self.MainWindow.trace("Done :) ")
            return True
                                

    def LinuxCompile(self,folderRoot ,name):
        useCPP=False
        lineY=0
        lineX=0
        if not folderRoot or not name:
            return False
        #print("Linux compile to ",folderRoot," app ",name)
        outFolder=folderRoot+os.path.sep+"obj"+os.path.sep+"Linux"+os.path.sep+name
        createFolderTree(outFolder)


        objsList=[]
        
        srcs=[]

        for src in self.Src.Src:
            srcs.append(src)

        for src in srcs:
            if not os.path.isfile(src):
                self.trace("File ",src," not exists ..")
                continue
        
            args=[]
            srcFolder = os.path.dirname(os.path.abspath(src))
            objFolder =outFolder +  srcFolder.replace(folderRoot,"")
            
            createFolderTree(objFolder)
            filename, file_extension = os.path.splitext(src)
            basename = os.path.basename(src)
            basename_without_ext = os.path.splitext(os.path.basename(src))[0]
            objName = objFolder+os.path.sep+basename_without_ext+".o"
            objsList.append(objName)
            src_modified_time = os.path.getmtime(src)
            src_convert_time = time.ctime(src_modified_time)

            cType = "gcc"
            if len(file_extension)>=3:
                    cType="g++"
                    useCPP=True
                    
            
 
            if os.path.exists(objName):
                obj_modified_time = os.path.getmtime(objName)
                obj_convert_time   = time.ctime(obj_modified_time)
                if (src_convert_time<obj_convert_time):
                    self.trace("Skip  file"+ src)
                    continue
                
                    
        
            
            self.MainWindow.trace ("Compile : ",cType," ",os.path.basename(src)," > ",os.path.basename(objName))

                
                    
            args.append("-c")
            args.append(src)
            args.append("-o")
            args.append(objName)
            

            if useCPP:
                for arg in self.Src.ARGSDESKTOP.ARGCPP: 
                    value =arg.strip()
                    if len(value)>=2:
                        args.append(arg)
                        
            else:
                for arg in self.Src.ARGSDESKTOP.ARGCC: 
                    value =arg.strip()
                    if len(value)>=2:
                        args.append(arg)
                        
            
            args.append("-fPIC")

                            
                
            code, out, err=runProcess(cType,args)
            #print("err: '{}'".format(str(err)))
            print(code)
            if code!=0:
                self.trace(err.decode("utf-8") )
                rexp=':(.*?):(.*?): error: '
                #match = re.compile(rexp, re.DOTALL | re.IGNORECASE).findall(err.decode("utf-8"))
                erro =re.search(rexp,err.decode("utf-8"))
                
                try:    
                    if erro:
                        linhas = erro.group().split(":")
                        lineX=int(linhas[2])
                        lineY=int(linhas[1])
                        self.MainWindow.setCursor(lineY-1,lineX-1)        
                        #self.trace("Compile Error line",str(lineY)," position:",str(lineX))

                except  Exception as error:
                    self.trace("Error ",error)
                
                return None
            self.trace(out.decode("utf-8") )
        self.trace("Compiling complete ")
        return objsList
        
    
             
    def WebBuild(self,folderRoot ,appName, ListOBJS ,useCPP ):
        if not ListOBJS or not folderRoot or not appName:
           return False
        if len(ListOBJS)<=0:
                return False
            
        args=[]
        outFolder=folderRoot+os.path.sep+"Web"+os.path.sep+appName
        createFolderTree(outFolder)
                
        cType = "emcc"
        if useCPP:
                cType="em++"
                
        self.trace("Build EMSDK aplication")
        args.append("-o")
        
        export = outFolder+os.path.sep+appName+".html"
        args.append(export)
        objs=""
        for obj in ListOBJS:
            objs+=obj+' '
            args.append(obj)
        #args.append('-s')


        for arg in self.Src.ARGSWEB.ARGLD:
            value =arg.strip()
            if len(value)>1:
                args.append(value)
        rootFolder=os.getcwd()+os.path.sep+"libs"+os.path.sep+"web"
        args.append("-L"+rootFolder)
           
            
        self.trace("Build to "+cType+" "+appName)
        code, out, err=runProcess(cType,args)
        if code!=0:
            self.trace(err.decode("utf-8") )
            self.trace("Operation Fail  .. ")
            return False
        return True
                
                
  
            
            
    def WebCompile(self,folderRoot ,name):
        useCPP=False
        if not folderRoot or not name:
            return False

        outFolder=folderRoot+os.path.sep+"obj"+os.path.sep+"Web"+os.path.sep+name
        createFolderTree(outFolder)
        objsList=[]
        
        srcs=[]
        for src in self.Src.Src:
            srcs.append(src)


        for src in srcs:
            if not os.path.isfile(src):
                self.trace("File ",src,"not exists")
                continue
        
            args=[]
            srcFolder = os.path.dirname(os.path.abspath(src))
            objFolder =outFolder +  srcFolder.replace(folderRoot,"")
            
            createFolderTree(objFolder)
            filename, file_extension = os.path.splitext(src)
            basename = os.path.basename(src)
            basename_without_ext = os.path.splitext(os.path.basename(src))[0]
            objName = objFolder+os.path.sep+basename_without_ext+".o"
            objsList.append(objName)
            src_modified_time = os.path.getmtime(src)
            src_convert_time = time.ctime(src_modified_time)

            cType = "emcc"
            if len(file_extension)>=3:
                    cType="em++"
                    useCPP=True
                    
            
       
            if os.path.exists(objName):
                obj_modified_time = os.path.getmtime(objName)
                obj_convert_time   = time.ctime(obj_modified_time)
                if (src_convert_time<obj_convert_time):
                    self.trace("Skip  file"+ src)
                    continue
            
                    
        
            
            self.trace ("Compile :",cType," ",os.path.basename(src)," > ",os.path.basename(objName))

                
                    
            args.append("-c")
            args.append(src)
            args.append("-o")
            args.append(objName)
            

            if useCPP:
                for arg in self.Src.ARGSWEB.ARGCPP: 
                    value =arg.strip()
                    if len(value)>=2:
                        args.append(arg)
 
            else:
                for arg in self.Src.ARGSWEB.ARGCC: 
                    value =arg.strip()
                    if len(value)>=2:
                        args.append(arg)
                        


                            
            print(args)    
            code, out, err=runProcess(cType,args)
            #print("err: '{}'".format(str(err)))
            #print("exit: {}".format(code))
            if code!=0:
                self.trace(err.decode("utf-8") )
                rexp=':(.*?):(.*?): error: '
                #match = re.compile(rexp, re.DOTALL | re.IGNORECASE).findall(err.decode("utf-8"))
                erro =re.search(rexp,err.decode("utf-8"))
                #print(erro)
                try:    
                    lineY=0
                    lineX=0
                    if erro:
                        linhas = erro.group().split(":")
                        lineX=int(linhas[2])
                        lineY=int(linhas[1])
                        self.MainWindow.setCursor(lineY-1,lineX-1)       
                        return None
                except  Exception as error:
                    self.trace("Error ",error)
                
            self.trace(out.decode("utf-8") )
        self.trace("Compiling completed")
        return objsList
        


class TabEditor(QWidget):
    def __init__(self):
        super(TabEditor, self).__init__()
            
        



class AppModulesWindow(QDialog):
    def __init__(self,parent,plataform):
        super(AppModulesWindow, self).__init__(parent)
        self.mainWindow=parent
        self.Plataform=plataform
        self.resize(965, 314)
        self.listBoxModule=[]
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle(u"Add Modules to Aplication")
        self.gridLayout_3 = QGridLayout(self)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"ModulesgroupBox")
        
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        
        self.groupBox.setSizePolicy(sizePolicy1)
        self.groupBox.setTitle(u"Modules")
        #self.gridLayout = QGridLayout(self.groupBox)
        #self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 3)

        self.moduleGridLayout = QGridLayout(self.groupBox)
        self.moduleGridLayout.setObjectName(u"moduleGridLayout")



        self.verticalSpacer = QSpacerItem(20, 2, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 1, 1, 1, 1)

        self.groupBoxBuildOptions = QGroupBox(self)
        self.groupBoxBuildOptions.setObjectName(u"groupBoxBuildOptions")
        sizePolicy1.setHeightForWidth(self.groupBoxBuildOptions.sizePolicy().hasHeightForWidth())
        self.groupBoxBuildOptions.setSizePolicy(sizePolicy1)
        self.groupBoxBuildOptions.setTitle(u"Compile & Build ARGS Options")
        self.gridLayout_2 = QGridLayout(self.groupBoxBuildOptions)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        
        self.label = QLabel(self.groupBoxBuildOptions)
        self.label.setObjectName(u"label")
        self.label.setText(u"CPP")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.lineEditLDArg = QLineEdit(self.groupBoxBuildOptions)
        self.lineEditLDArg.setObjectName(u"lineEditLDArg")
        self.lineEditLDArg.setText(u"")
        
        argument=""
        for arg in self.mainWindow.GLOBALARGS.ARGLD:
            argument+=arg
        self.lineEditLDArg.setText(argument)
        
        
        
        #        self.ARGCPP=[]
        #self.ARGCC=[]
        #self.ARGLD=[]

        self.gridLayout_2.addWidget(self.lineEditLDArg, 2, 1, 1, 1)

        self.label_2 = QLabel(self.groupBoxBuildOptions)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setText(u"CC")
        
        

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEditCCArg = QLineEdit(self.groupBoxBuildOptions)
        self.lineEditCCArg.setObjectName(u"lineEditCCArg")
        self.lineEditCCArg.setText(u"")
        argument=""
        for arg in self.mainWindow.GLOBALARGS.ARGCC:
            argument+=arg
        self.lineEditCCArg.setText(argument)
        

        self.gridLayout_2.addWidget(self.lineEditCCArg, 1, 1, 1, 1)

        self.label_3 = QLabel(self.groupBoxBuildOptions)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setText(u"LINK")

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.lineEditCPPArg = QLineEdit(self.groupBoxBuildOptions)
        self.lineEditCPPArg.setObjectName(u"lineEditCPPArg")
        self.lineEditCPPArg.setText(u"")
        argument=""
        for arg in self.mainWindow.GLOBALARGS.ARGCPP:
            argument+=arg
        self.lineEditCPPArg.setText(argument)
        

        self.gridLayout_2.addWidget(self.lineEditCPPArg, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.groupBoxBuildOptions, 2, 0, 1, 3)

        self.verticalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 3, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(722, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 4, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setTitle(u"")
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonCancel = QPushButton(self.groupBox_2)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setText(u"Cancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)

        self.pushButtonOk = QPushButton(self.groupBox_2)
        self.pushButtonOk.setObjectName(u"pushButtonOk")
        self.pushButtonOk.setText(u"OK")

        self.horizontalLayout.addWidget(self.pushButtonOk)


        self.gridLayout_3.addWidget(self.groupBox_2, 4, 2, 1, 1)

        self.pushButtonOk.pressed.connect(self.onSelect)
        self.pushButtonCancel.pressed.connect(self.onCancel)


        

        QMetaObject.connectSlotsByName(self)
    def load(self):
        self.mainWindow.loadModules()   
        row = 0
        col = 0
        widgetsPerRow = 8
        index=0
        for module in self.mainWindow.modulesData:
            print("load  ",module.Name)
            checkBoxModule = QCheckBox()
            checkBoxModule.toggled.connect(self.onCheckBoxModule)  
            checkBoxModule.setObjectName(module.Name)
            if module in self.mainWindow.GLOBALMODULES:
                checkBoxModule.setChecked(True)
            else:
                checkBoxModule.setChecked(False)
                
            checkBoxModule.module=module
            checkBoxModule.setText(module.Name)
            self.listBoxModule.append(checkBoxModule)
            self.moduleGridLayout.addWidget(checkBoxModule,row,col,1,1)
            index+=1
            col += 1
            if col % widgetsPerRow == 0:
                    row += 1
                    col = 0
        #for gmodule in self.mainWindow.GLOBALMODULES:
        #    for inmodule in self.listBoxModule:
        #        if gmodule==inmodule.module:
        #            inmodule.setChecked(True)
                        
        self.show()
    def onCheckBoxModule(self):
        cbutton = self.sender()
        print("module " + (cbutton.module.Name) + " is " + str(cbutton.isChecked()))
        if cbutton.isChecked():
            if not cbutton.module in self.mainWindow.GLOBALMODULES:
                self.mainWindow.GLOBALMODULES.append(cbutton.module)
        else:
            if cbutton.module in self.mainWindow.GLOBALMODULES:
                self.mainWindow.GLOBALMODULES.remove(cbutton.module)
        
        
        
    def onSelect(self):
        cppArgs = self.lineEditCPPArg.text().strip().split("-")
        ccArgs = self.lineEditCCArg.text().strip().split("-")
        ldArgs = self.lineEditLDArg.text().strip().split("-")
        self.mainWindow.GLOBALARGS.clear()
        
        for arg in cppArgs:
            value ="-"+arg.strip()
            if len(value)>=2:
                self.mainWindow.GLOBALARGS.addCPP(value)
            
        for arg in ccArgs:
            value ="-"+arg.strip()
            if len(value)>=2:
                self.mainWindow.GLOBALARGS.addCC(value)

        for arg in ldArgs:
            value ="-"+arg.strip()
            if len(value)>=2:
                self.mainWindow.GLOBALARGS.addLD(value)
        
        print(cppArgs)
        print(ccArgs)
        print(ldArgs)
        
        for module in self.mainWindow.GLOBALMODULES:
            print(module.Name)
        
        self.close()
        pass
    def onCancel(self):
        self.close()
        pass

class ModulesWindow(QDialog):
    def __init__(self,parent):
        super(ModulesWindow, self).__init__(parent)
        self.resize(887, 345)
        self.mainWindow=parent
        
        self.listBoxModule=[]
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(self)
        self.groupBox.setObjectName(u"groupBox")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.groupBox.setSizePolicy(sizePolicy)

        self.moduleGridLayout = QGridLayout(self.groupBox)
        self.moduleGridLayout.setObjectName(u"moduleGridLayout")

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 358, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self)
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.groupBox_3 = QGroupBox(self.groupBox_2)
        self.verticalLayout = QVBoxLayout(self.groupBox_3)
        self.checkBoxDesktop = QCheckBox(self.groupBox_3)
        self.checkBoxDesktop.setChecked(True)
        self.verticalLayout.addWidget(self.checkBoxDesktop)
        self.checkBoxAndroid = QCheckBox(self.groupBox_3)
        self.verticalLayout.addWidget(self.checkBoxAndroid)
        self.checkBoxEmsdk = QCheckBox(self.groupBox_3)
        self.verticalLayout.addWidget(self.checkBoxEmsdk)
        self.horizontalLayout.addWidget(self.groupBox_3)
        
        self.groupBoxAndroidArm = QGroupBox(self.groupBox_2)
        self.groupBoxAndroidArm.setObjectName(u"groupBoxAndroidArm")
        
        self.groupBoxAndroidArm.setTitle(u"Android Arm")
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxAndroidArm)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkBoxArm7 = QCheckBox(self.groupBoxAndroidArm)
        self.checkBoxArm7.setObjectName(u"checkBoxArm7")
        self.checkBoxArm7.setText(u"ARM7")
        self.checkBoxArm7.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBoxArm7)

        self.checkBoxArm64 = QCheckBox(self.groupBoxAndroidArm)
        self.checkBoxArm64.setObjectName(u"checkBoxArm64")
        self.checkBoxArm64.setText(u"ARM64")

        self.verticalLayout_2.addWidget(self.checkBoxArm64)


        self.horizontalLayout.addWidget(self.groupBoxAndroidArm)

        
        
        
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        


        self.pushButtonCompileBuild = QPushButton(self.groupBox_2)
        self.pushButtonCompileBuild.setIcon( QIcon(rsrcPath + '/pkg_compile_200.png'))
        self.pushButtonCompileBuild.setText("NormalBuild")
        self.horizontalLayout.addWidget(self.pushButtonCompileBuild)


        self.pushButtonCompile = QPushButton(self.groupBox_2)
        self.pushButtonCompile.setIcon( QIcon(rsrcPath + '/pkg_compile_200.png'))
        self.pushButtonCompile.setText("Compile")
        self.horizontalLayout.addWidget(self.pushButtonCompile)

        self.pushButtonBuild = QPushButton(self.groupBox_2)
        self.pushButtonBuild.setIcon( QIcon(rsrcPath + '/pkg_compile_200.png'))
        self.pushButtonBuild.setText("Build")
        self.horizontalLayout.addWidget(self.pushButtonBuild)


        self.pushButtonClean = QPushButton(self.groupBox_2)
        self.pushButtonClean.setObjectName(u"pushButtonClean")
        self.pushButtonClean.setIcon( QIcon(rsrcPath + '/edit-clear.png'))
        self.horizontalLayout.addWidget(self.pushButtonClean)

        
        self.pushButtonRealod = QPushButton(self.groupBox_2)
        self.pushButtonRealod.setObjectName(u"pushButtonRealod")
        self.pushButtonRealod.setIcon( QIcon(rsrcPath + '/pkg_package_circle_200.png'))
        self.horizontalLayout.addWidget(self.pushButtonRealod)

        self.pushButtonClose = QPushButton(self.groupBox_2)
        self.pushButtonClose.setObjectName(u"pushButtonClose")
        self.pushButtonClose.pressed.connect(self.close)


        self.pushButtonCompile.pressed.connect(self.compile)
        self.pushButtonBuild.pressed.connect(self.build)


        self.pushButtonCompileBuild.pressed.connect(self.compile_and_build)
        self.pushButtonClean.pressed.connect(self.clean)
        self.pushButtonRealod.pressed.connect(self.selectRealod)
        
        
        

        self.horizontalLayout.addWidget(self.pushButtonClose)


        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 1)


        

        QMetaObject.connectSlotsByName(self)
        self.retranslateUi()

    def selectRealod(self):
        print("reload modules")
        for w in self.listBoxModule:
            self.moduleGridLayout.removeWidget(w)
            w.close()
            w=None

        self.listBoxModule.clear()
        self.mainWindow.loadModules(True)
        row = 0
        col = 0
        widgetsPerRow = 8
        index=0
        for module in self.mainWindow.modulesData:
            print("load ",module.Name)
            checkBoxModule = QCheckBox()
            checkBoxModule.toggled.connect(self.onCheckBoxModule)  
            checkBoxModule.setObjectName(module.Name)
            checkBoxModule.setChecked(False)
            checkBoxModule.module=module
            checkBoxModule.setText(module.Name)
            self.listBoxModule.append(checkBoxModule)
            self.moduleGridLayout.addWidget(checkBoxModule,row,col,1,1)
            index+=1
            col += 1
            if col % widgetsPerRow == 0:
                    row += 1
                    col = 0

    def clean(self):
        compileDesktop =self.checkBoxDesktop.isChecked()
        compileAndroid =self.checkBoxAndroid.isChecked()
        compileWeb     =self.checkBoxEmsdk.isChecked()
       
        for cbutton in self.listBoxModule:
            if (cbutton.isChecked()):
                module = cbutton.module
                module.clean()
    def compile(self):
        compileDesktop =self.checkBoxDesktop.isChecked()
        compileAndroid =self.checkBoxAndroid.isChecked()
        compileWeb     =self.checkBoxEmsdk.isChecked()
        for cbutton in self.listBoxModule:
            if (cbutton.isChecked()):
                module = cbutton.module
                if compileDesktop:
                    module.compileDesktop()
                if compileAndroid:
                    if self.checkBoxArm7.isChecked()==False and self.checkBoxArm64.isChecked()==False:
                        self.checkBoxArm7.setChecked(True)
                        
                    module.compileAndroid(self.checkBoxArm7.isChecked(),self.checkBoxArm64.isChecked())
                if compileWeb:
                    module.compileWeb()
    def build(self):
        compileDesktop =self.checkBoxDesktop.isChecked()
        compileAndroid =self.checkBoxAndroid.isChecked()
        compileWeb     =self.checkBoxEmsdk.isChecked()

    def compile_and_build(self):
        compileDesktop =self.checkBoxDesktop.isChecked()
        compileAndroid =self.checkBoxAndroid.isChecked()
        compileWeb     =self.checkBoxEmsdk.isChecked()
        for cbutton in self.listBoxModule:
            if (cbutton.isChecked()):
                module = cbutton.module
                if compileDesktop:
                    module.compileDesktop()
                if compileAndroid:
                    if self.checkBoxArm7.isChecked()==False and self.checkBoxArm64.isChecked()==False:
                        self.checkBoxArm7.setChecked(True)
                    module.compileAndroid(self.checkBoxArm7.isChecked(),self.checkBoxArm64.isChecked())
                if compileWeb:
                    module.compileWeb()


    def onCheckBoxModule(self):
        cbutton = self.sender()
        #print("module " + (cbutton.module.name) + " is " + str(cbutton.isChecked()))
        pass

   

           
    def load(self):
        self.mainWindow.loadModules()
        row = 0
        col = 0
        widgetsPerRow = 8
        index=0
        for module in self.mainWindow.modulesData:
            print("load ",module.Name)
            checkBoxModule = QCheckBox()
            checkBoxModule.toggled.connect(self.onCheckBoxModule)  
            checkBoxModule.setObjectName(module.Name)
            checkBoxModule.setChecked(False)
            checkBoxModule.module=module
            checkBoxModule.setText(module.Name)
            self.listBoxModule.append(checkBoxModule)
            self.moduleGridLayout.addWidget(checkBoxModule,row,col,1,1)
            index+=1
            col += 1
            if col % widgetsPerRow == 0:
                    row += 1
                    col = 0
            
        self.show()
        pass

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Modules", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Actions", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Plataform", None))
        self.checkBoxDesktop.setText(QCoreApplication.translate("Dialog", u"Desktop", None))
        self.checkBoxAndroid.setText(QCoreApplication.translate("Dialog", u"Android", None))
        self.checkBoxEmsdk.setText(QCoreApplication.translate("Dialog", u"Emscripten", None))
        
        self.pushButtonClean.setText(QCoreApplication.translate("Dialog", u"Clean", None))
        
        self.pushButtonRealod.setText(QCoreApplication.translate("Dialog", u"Reload", None))
        self.pushButtonClose.setText(QCoreApplication.translate("Dialog", u"Close", None))    # retranslateUi



class Theme():

    class LexerCPP(QsciLexerCPP):

        def __init__(self, parent=None):
            super().__init__(parent)

        def defaultColor(self, style):
            DEFAULT = QColor(247, 247, 241)
            KEYWORD = QColor(249, 38, 114)
            DATATYPE = QColor(102, 216, 238)
            NUMBER = QColor(174, 129, 255)
            OPERATOR = QColor(249, 38, 114)
            STRING = QColor(255, 219, 116)
            FUNCTION = QColor(166, 226, 46)
            COMMENT = QColor(117, 113, 94)
            HASHCOMMENT = QColor(174, 129, 255)

            dct = {
                self.Comment: COMMENT,
                self.CommentLine: COMMENT,
                self.CommentDoc: COMMENT,
                self.CommentLineDoc: COMMENT,
                self.PreProcessorCommentLineDoc: COMMENT,
                self.Number: NUMBER,
                self.Keyword: FUNCTION,
                # self.Keyword: KEYWORD,
                self.KeywordSet2: QColor(102, 216, 238),
                self.DoubleQuotedString: STRING,
                self.SingleQuotedString: STRING,
                self.RawString: STRING,
                self.PreProcessor: QColor(0x7f, 0x7f, 0x00),
                self.Operator: DEFAULT,
                self.UnclosedString: STRING,
                self.VerbatimString: STRING,
                self.TripleQuotedVerbatimString: STRING,
                self.HashQuotedString: STRING,
                self.Regex: QColor(0x3f, 0x7f, 0x3f),
                self.CommentDocKeyword: QColor(0x30, 0x60, 0xa0),
                self.CommentDocKeywordError: QColor(0x80, 0x40, 0x20),
                self.PreProcessorComment: QColor(0x65, 0x99, 0x00),
                self.InactiveDefault: QColor(0xc0, 0xc0, 0xc0),
                self.InactiveUUID: QColor(0xc0, 0xc0, 0xc0),
                self.InactiveCommentLineDoc: QColor(0xc0, 0xc0, 0xc0),
                self.InactiveKeywordSet2: QColor(0xc0, 0xc0, 0xc0),
                self.InactiveCommentDocKeyword: QColor(0xc0, 0xc0, 0xc0),
                self.InactiveCommentDocKeywordError: QColor(0xc0, 0xc0, 0xc0),
                self.InactivePreProcessorCommentLineDoc: QColor(0xc0, 0xc0, 0xc0),
                self.InactiveComment: QColor(0x90, 0xb0, 0x90),
                self.InactiveCommentLine: QColor(0x90, 0xb0, 0x90),
                self.InactiveNumber: QColor(174, 129, 255),
                self.InactiveVerbatimString: STRING,
                self.InactiveTripleQuotedVerbatimString: STRING,
                self.InactiveHashQuotedString: QColor(0x90, 0xb0, 0x90),
                self.InactiveCommentDoc: QColor(0xd0, 0xd0, 0xd0),
                self.InactiveKeyword: QColor(0x90, 0x90, 0xb0),
                self.InactiveDoubleQuotedString: STRING,
                self.InactiveSingleQuotedString: STRING,
                self.InactiveRawString: STRING,
                self.InactivePreProcessor: QColor(0xb0, 0xb0, 0x90),
                self.InactiveOperator: QColor(0xb0, 0xb0, 0xb0),
                self.InactiveIdentifier: QColor(0xb0, 0xb0, 0xb0),
                self.InactiveGlobalClass: QColor(0xb0, 0xb0, 0xb0),
                self.InactiveUnclosedString: STRING,
                self.InactiveRegex: QColor(0x7f, 0xaf, 0x7f),
                self.InactivePreProcessorComment: QColor(0xa0, 0xc0, 0x90),
                self.UserLiteral: QColor(0xc0, 0x60, 0x00),
                self.InactiveUserLiteral: QColor(0xd7, 0xa0, 0x90),
                self.TaskMarker: QColor(0xbe, 0x07, 0xff),
                self.InactiveTaskMarker: QColor(0xc3, 0xa1, 0xcf)
            }

            return dct.get(style, DEFAULT)

        def defaultPaper(self, style):
            # return self.parent().paper()
            return QColor(39, 40, 34)

        def defaultFont(self, style):
            font = QFont()
            font.setFamily('Consolas')
            font.setFixedPitch(True)
            font.setPointSize(12)
            font.setBold(False)
            return font

    def __init__(self, sci):
        self.sci = sci

        sci.setFolding(QsciScintilla.CircledFoldStyle)
        sci.setMarginType(1, QsciScintilla.NumberMargin)
        sci.setMarginSensitivity(1, True)
        sci.markerDefine(QsciScintilla.RightArrow, 8)
        sci.setMarkerBackgroundColor(QColor("#ee1111"), 8)

        lexer = self.LexerCPP()
        lexer.setFoldAtElse(True)
        lexer.setFoldComments(True)
        lexer.setFoldCompact(False)
        lexer.setFoldPreprocessor(True)
        sci.setLexer(lexer)


class Monokai():

    def __init__(self, sci):
        self.sci = sci

        # Set default font
        sci.font = QFont()
        sci.font.setFamily('Consolas')
        sci.font.setFixedPitch(True)
        sci.font.setPointSize(8)
        sci.font.setBold(True)
        sci.setFont(sci.font)
        sci.setMarginsFont(sci.font)
        sci.setUtf8(True)

        # Set paper
        sci.setPaper(QColor(39, 40, 34))

        # Set margin defaults
        fontmetrics = QFontMetrics(sci.font)
        sci.setMarginsFont(sci.font)
        sci.setMarginWidth(0, fontmetrics.width("000") + 6)
        sci.setMarginLineNumbers(0, True)
        sci.setMarginsForegroundColor(QColor(128, 128, 128))
        sci.setMarginsBackgroundColor(QColor(39, 40, 34))
        sci.setMarginType(1, sci.SymbolMargin)
        sci.setMarginWidth(1, 12)
        # sci.setMarginMarkerMask(1,
        #                   1 << MarkerType::ERROR |
        #                   1 << MarkerType::WARNING
        #                   );

        # Set indentation defaults
        sci.setIndentationsUseTabs(False)
        sci.setIndentationWidth(4)
        sci.setBackspaceUnindents(True)
        sci.setIndentationGuides(True)
        # sci.setIndentationGuidesBackgroundColor(QColor("#2a2b24"))
        # sci.setIndentationGuidesForegroundColor(QColor("#2a2b24"))
        sci.setFoldMarginColors(QColor(39, 40, 34), QColor(39, 40, 34))
        # sci.setEolMode(QsciScintilla.EolUnix)

        # Set caret defaults
        sci.setCaretForegroundColor(QColor(247, 247, 241))
        sci.setCaretWidth(2)

        # Set edge defaults
        sci.setEdgeColumn(80)
        sci.setEdgeColor(QColor('#dddddd'))
        sci.setEdgeMode(sci.EdgeLine)

        # Set folding defaults (http://www.scintilla.org/ScintillaDoc.html#Folding)
        sci.setFolding(QsciScintilla.BoxedFoldStyle)
        #PlainFoldStyle
        #CircledFoldStyle
        #BoxedFoldStyle
        #CircledTreeFoldStyle
        #BoxedTreeFoldStyle
        

        # Set brace defaults
        # sci.setBraceMatching(sci.SloppyBraceMatch)
        # sci.setMatchedBraceBackgroundColor(QColor(62, 61, 50))
        # sci.setUnmatchedBraceBackgroundColor(QColor(249, 38, 114))

        sci.setWrapMode(sci.WrapNone)

        # Set selection color defaults
        sci.setSelectionBackgroundColor(QColor(61, 61, 52))
        sci.resetSelectionForegroundColor()

        # Set scrollwidth defaults
        sci.SendScintilla(QsciScintilla.SCI_SETSCROLLWIDTHTRACKING, 1)

        # Current line visible with special background color
        # sci.setCaretLineVisible(True)
        # sci.setCaretLineBackgroundColor(QColor('#ffffe0'))

        # Set multiselection defaults
        sci.SendScintilla(QsciScintilla.SCI_SETMULTIPLESELECTION, True)
        sci.SendScintilla(QsciScintilla.SCI_SETMULTIPASTE, 1)
        sci.SendScintilla(QsciScintilla.SCI_SETADDITIONALSELECTIONTYPING, True)
  

class CodeEditor(QsciScintilla):
    comment_string = "// "
    line_ending = "\n"
    def __init__(self, parent=None):
        QsciScintilla.__init__(self, parent)

        self.setup()
        self.mainWindow=parent
        self.project=None
        self.currentLine=0
        self.currentCursor=0
        
        features = [
        Theme(self),
        Monokai(self)    ]
        self.setup()
        self.cursorPositionChanged.connect(self.OncursorPositionChanged)

        
        
        
    def OncursorPositionChanged(self,line,index):
        #print(line," ",index)
        self.currentLine=line
        self.currentCursor=index
        self.mainWindow.setStatusBarLineCount(line)
    def saveProject(self):
        print("save project")
    def loadProject(self):
        print("save project")
    def compileProject(self):
        print("compile project")
    def buildProject(self):
        print("build project")
    def runProject(self):
        print("run project")

    def keyPressEvent(self, event):
        # Execute the superclasses event
        super().keyPressEvent(event)
        # Check pressed key information
        key = event.key()
        key_modifiers = QApplication.keyboardModifiers()
        if (key == QtCore.Qt.Key_K and 
            key_modifiers == QtCore.Qt.ControlModifier):
                self.toggle_commenting()
    
    def toggle_commenting(self):
        # Check if the selections are valid
        selections = self.get_selections()
        if selections == None:
            return
        # Merge overlapping selections
        while self.merge_test(selections) == True:
            selections = self.merge_selections(selections)
        # Start the undo action that can undo all commenting at once
        self.beginUndoAction()
        # Loop over selections and comment them
        for i, sel in enumerate(selections):
            if self.text(sel[0]).lstrip().startswith(self.comment_string):
                self.set_commenting(sel[0], sel[1], self._uncomment)
            else:
                self.set_commenting(sel[0], sel[1], self._comment)
        # Select back the previously selected regions
        self.SendScintilla(self.SCI_CLEARSELECTIONS)
        for i, sel in enumerate(selections):
            start_index = self.positionFromLineIndex(sel[0], 0)
            # Check if ending line is the last line in the editor
            last_line = sel[1]
            if last_line == self.lines() - 1:
                end_index = self.positionFromLineIndex(sel[1], len(self.text(last_line)))
            else:
                end_index = self.positionFromLineIndex(sel[1], len(self.text(last_line))-1)
            if i == 0:
                self.SendScintilla(self.SCI_SETSELECTION, start_index, end_index)
            else:
                self.SendScintilla(self.SCI_ADDSELECTION, start_index, end_index)
        # Set the end of the undo action
        self.endUndoAction()
    
    def get_selections(self):
        # Get the selection and store them in a list
        selections = []
        for i in range(self.SendScintilla(self.SCI_GETSELECTIONS)):
            selection = (
                self.SendScintilla(self.SCI_GETSELECTIONNSTART, i),
                self.SendScintilla(self.SCI_GETSELECTIONNEND, i)
            )
            # Add selection to list
            from_line, from_index = self.lineIndexFromPosition(selection[0])
            to_line, to_index = self.lineIndexFromPosition(selection[1])
            selections.append((from_line, to_line))
        selections.sort()
        # Return selection list
        return selections
    
    def merge_test(self, selections):
        """
        Test if merging of selections is needed
        """
        for i in range(1, len(selections)):
            # Get the line numbers
            previous_start_line = selections[i-1][0]
            previous_end_line = selections[i-1][1]
            current_start_line = selections[i][0]
            current_end_line = selections[i][1]
            if previous_end_line == current_start_line:
                return True
        # Merging is not needed
        return False
    
    def merge_selections(self, selections):
        """
        This function merges selections with overlapping lines
        """
        # Test if merging is required
        if len(selections) < 2:
            return selections
        merged_selections = []
        skip_flag = False
        for i in range(1, len(selections)):
            # Get the line numbers
            previous_start_line = selections[i-1][0]
            previous_end_line = selections[i-1][1]
            current_start_line = selections[i][0]
            current_end_line = selections[i][1]
            # Test for merge
            if previous_end_line == current_start_line and skip_flag == False:
                merged_selections.append(
                    (previous_start_line, current_end_line)
                )
                skip_flag = True
            else:
                if skip_flag == False:
                    merged_selections.append(
                        (previous_start_line, previous_end_line)
                    )
                skip_flag = False
                # Add the last selection only if it was not merged
                if i == (len(selections) - 1):
                    merged_selections.append(
                        (current_start_line, current_end_line)
                    )
        # Return the merged selections
        return merged_selections
    
    def set_commenting(self, arg_from_line, arg_to_line, func):
        # Get the cursor information
        from_line = arg_from_line
        to_line = arg_to_line
        # Check if ending line is the last line in the editor
        last_line = to_line
        if last_line == self.lines() - 1:
            to_index = len(self.text(to_line))
        else:
            to_index = len(self.text(to_line))-1
        # Set the selection from the beginning of the cursor line
        # to the end of the last selection line
        self.setSelection(
            from_line, 0, to_line, to_index
        )
        # Get the selected text and split it into lines
        selected_text = self.selectedText()
        selected_list = selected_text.split("\n")
        # Find the smallest indent level
        indent_levels = []
        for line in selected_list:
            indent_levels.append(len(line) - len(line.lstrip()))
        min_indent_level = min(indent_levels)
        # Add the commenting character to every line
        for i, line in enumerate(selected_list):
            selected_list[i] = func(line, min_indent_level)
        # Replace the whole selected text with the merged lines
        # containing the commenting characters
        replace_text = self.line_ending.join(selected_list)
        self.replaceSelectedText(replace_text)
    
    def _comment(self, line, indent_level):
        if line.strip() != "":
            return line[:indent_level] + self.comment_string + line[indent_level:]
        else:
            return line
    
    def _uncomment(self, line, indent_level):
        if line.strip().startswith(self.comment_string):
            return line.replace(self.comment_string, "", 1)
        else:
            return line
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
        
        self.setMarginType(1, QsciScintilla.NumberMargin)
        self.SendScintilla(QsciScintilla.SCI_SETMULTIPLESELECTION, 1)
        self.SendScintilla(QsciScintilla.SCI_SETADDITIONALSELECTIONTYPING, True)
        

        self.setCallTipsStyle(QsciScintilla.CallTipsNoContext)
        self.setCallTipsVisible(0)
        self.setCallTipsPosition(QsciScintilla.CallTipsAboveText)
        self.setCallTipsBackgroundColor(QColor(0xff, 0xff, 0xff, 0xff))
        self.setCallTipsForegroundColor(QColor(0x50, 0x50, 0x50, 0xff))
        self.setCallTipsHighlightColor(QColor(0xff, 0x00, 0x00, 0xff))
        self.setCaretForegroundColor(QColor(0xff, 0x00, 0x00, 0x00))
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor('lightblue'))
        

class CodeListView(QListWidget):
    
    def __init__(self,  parent=None):
        super(CodeListView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(72, 72))
        self.items = []
        self.mainfolder = None
        self.mainWindow = parent
        self.project=None
        
        
        self.clicked.connect(self.onClick)
        self.doubleClicked.connect(self.onDoubleClicked)
    

    def loadProject(self,project):
        self.clearAll()
        self.project=project
        for src in project.Src.Src:
            self.addSrcFile(src)
        

    def onClick(self):
        #print("clink")    
        pass

    def onDoubleClicked(self,item):
        #print("doublw clink",str(item.row())) 
        #print("doublw clink",str(item.row()))   
        #print(self.items[item.row()])
        #self.mainWindow.load(self.items[item.row()])  
        self.mainWindow.load(self.items[item.row()])   
        pass


    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        clrAct = contextMenu.addAction("Clear")
        removeAct = contextMenu.addAction("Remove")
        listAct = contextMenu.addAction("List")
        addAct = contextMenu.addAction("Add")

        if self.count()<=0:
            return 
        
        
        
        #print("count ",self.count())
        #print("row ",self.currentRow())
        index = self.currentRow()
        

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == clrAct:
            self.items.clear()
            self.clear()
            self.mainfolder==None
        if action == removeAct:
            print("Remove   ",str(self.items[index])," index: ", index)
            self.items.pop(index)
            self.takeItem(index)
        if action==listAct:
            for i in range(self.count()):
                print(self.items[i])
        if action==addAct:
            fn, _ = QFileDialog.getOpenFileName(self, "Open File...", None,
                "Code files (*.cpp *.c);;All Files (*)")
            if fn:
                self.addSrcFile(fn)

            
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
                    

        else:
            event.ignore
    




    def stop(self):
        self.wait()    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        
        
        self.setupFileActions()
        self.setupProjectActions()

        self.setupCompilerActions()
        self.setupModulesActions()

        self.setupEditActions()        
        
        self.modulesList=[]
        self.modulesData=[]
        self.currentPlataform=0
        
        self.IsDone=False
        self.GLOBALARGS=Args()
        #self.GLOBALARGS.ARGCC.append("-std=c99")
        #self.GLOBALARGS.ARGCPP.append("-std=c++11")
        self.GLOBALMODULES=[]
        
        self.LAST_DIR=os.getcwd()+"/projects"
        self.LAST_PROJECT=""
        self.projects=[]
        self.files=[]

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.lineCountLabel = QLabel("Current Line: 1")
        self.statusbar.addPermanentWidget(self.lineCountLabel)

        self.dock = QDockWidget()
        self.dock.setWindowTitle('Project Src List')
        self.listSrc = CodeListView(self)
        self.dock.setWidget(self.listSrc)
        self.listSrc.show()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        
        self.Consoledock = QDockWidget()
        self.Consoledock.setWindowTitle('Console')
        self.MainConsole = ConsoleText()
        self.MainConsole.appendPlainText("By DjokerSoft @2021")
        self.Consoledock.setWidget(self.MainConsole)
        
        self.addDockWidget(Qt.BottomDockWidgetArea, self.Consoledock)
        
        
        
        self.setWindowTitle(self.tr("%s[*] - %s" % ("editor", "Cross Compile IDE")))
        self.setWindowModified(False)
        
        helpMenu = QMenu("Help", self)
        self.menuBar().addMenu(helpMenu)
        helpMenu.addAction("About", self.about)
        helpMenu.addAction("About &Qt", QApplication.instance().aboutQt)
 
        
        QApplication.clipboard().dataChanged.connect(self.clipboardDataChanged)

        self.cpplexer = QsciLexerCPP()
        self.api = QsciAPIs(self.cpplexer)

        for root, directories, files in os.walk(os.getcwd()+os.path.sep+"api", topdown=False):
            for name in files:
                ext = os.path.splitext(name)[1]
                if (ext==".api"):
                    print(os.path.join(root, name)," ",ext," ",directories)
                    with open(os.path.join(root, name)) as data:
                        for rline in data.readlines():
                            line=rline.strip()
                            if (len(line))>=1:
                                self.api.add(line)
                            
                            

                    #self.api.add(line)
        
        self.api.prepare()
                    
    
        
        #wordlist = os.getcwd()+os.path.sep+"res"+os.path.sep+"wordlist.txt"

        #self.AutoCompletionsFromFile(wordlist)


        self.X=0
        self.Y=0
        self.codeTab = QTabWidget()
        self.codeTab.setTabBarAutoHide(False)
        self.codeTab.setMovable(True)
        self.codeTab.setTabsClosable(True)
        self.codeTab.tabCloseRequested.connect(self.onCloseTab)
        self.codeTab.currentChanged.connect(self.onChangeTab)
        
        #self.pushButtonCancel.pressed.connect(self.onCancel)
        #connect(tabBar, &QTabBar::tabCloseRequested, this, &TabWidget::closeTab);
        

        #newAction.triggered.connect(self.openDialog)
        #quitAction.triggered.connect(self.close)

        self.setCentralWidget(self.codeTab)
        
        #self.loadProject("projects/main.mk")
        
        with open("config.json", 'r') as data:
            jdata = json.load(data)
            values = jdata["Global"]
            files=values["Files"]
            for f in files:
                self.load(str(f))
            projects=values["Projects"]
            for proj in projects:
                self.loadProject(str(proj))
            ArgsCPP=values["ArgCPP"]
            ArgsCC =values["ArgCC"]
            ArgsLD =values["ArgLD"]
            
            for arg in ArgsCPP:
                self.GLOBALARGS.addCPP(str(arg))
            
            for arg in ArgsCC:
                self.GLOBALARGS.addCC(str(arg))

            for arg in ArgsLD:
                self.GLOBALARGS.addLD(str(arg))
                
                
            
            #print(values)
            #print(jdata)        


        #self.setWindowTitle("Order Form")
    def setStatusBarLineCount(self,count):
        self.lineCountLabel.setText("Current Line: "+str(count))

    def onChangeTab(self,index):
        print("switch tab:",index)
        self.listSrc.clearAll()
        textEdit = self.codeTab.currentWidget()
        project = textEdit.project
        if project:
            self.listSrc.loadProject(project)
        self.setCurrentFileName()
        

    def onCloseTab(self,index):

        print("close tab:",index)
        self.fileSave()
        textEdit = self.codeTab.currentWidget()
        textEdit.close()
        if textEdit.project in self.projects:
            self.projects.remove(textEdit.project)
        if textEdit.fileName in self.files:
            self.files.remove(textEdit.fileName)
            
        self.codeTab.removeTab(index)
        if self.codeTab.count()==0:
           self.actionSaveAs.setEnabled(False)
           self.actionSave.setEnabled(False)
           self.actionSaveProject.setEnabled(False)
           self.LAST_PROJECT=None

    def log(self,msg):
        self.MainConsole.appendPlainText(msg)        

    def trace(self,*args):
        result = ""
        for x in args:
            result += str(x)
        
        self.MainConsole.appendPlainText(result)

    def ClearConsole(self):
        self.MainConsole.clear()
        
                    
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
    
    def selectWorkPlataform(self):
        pass
    def addModule(self):
        AppModules = AppModulesWindow(self,0)
        AppModules.load()
    
    def switchPlataform(self,index):
        self.currentPlataform=index

    def setupCompilerActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle("Compiler Actions")
        self.addToolBar(tb)

        menu = QMenu("&Compiler", self)
        self.menuBar().addMenu(menu)

        
        

        self.comboBox = QComboBox(tb)
        self.comboBox.setGeometry(QRect(260, 130, 390, 67))
        self.comboBox.addItem("Dektop")
        self.comboBox.addItem("Android")
        self.comboBox.addItem("Emscripten")
        self.comboBox.currentIndexChanged.connect(self.switchPlataform)
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setEditable(False)
        


        actionCompile = QAction(QIcon(rsrcPath + '/build.xpm'),           "&Compile", self,  shortcut=Qt.Key_F5, priority=QAction.LowPriority, triggered=self.compile)
        tb.addAction(actionCompile)
        menu.addAction(actionCompile)

        tb.insertWidget(actionCompile,self.comboBox)

        actionRun = QAction(          QIcon(rsrcPath + '/Go.png'),                "&Run", self, shortcut=Qt.Key_F6,priority=QAction.LowPriority, triggered=self.compileRun)
        tb.addAction(actionRun)
        menu.addAction(actionRun)

        actionCompileRun = QAction(   QIcon(rsrcPath + '/buildrun.xpm'),                "&Compile&Run", self, shortcut=Qt.Key_F9,priority=QAction.LowPriority, triggered=self.compileAndRun)
        tb.addAction(actionCompileRun)
        menu.addAction(actionCompileRun)

        actionClean= QAction(QIcon(rsrcPath + '/edit-clear.png'),                "&Clean", self, priority=QAction.LowPriority,triggered=self.compileClean)
        tb.addAction(actionClean)
        menu.addAction(actionClean)

        actionSelectModule= QAction(QIcon(rsrcPath + '/pkg_inherited_200.png'),                "&Global Config", self, priority=QAction.LowPriority,triggered=self.addModule)
        tb.addAction(actionSelectModule)
        menu.addAction(actionSelectModule)


    def showModules(self):
         WinModules = ModulesWindow(self)
         WinModules.load()
         
    
    def setupModulesActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle("Module Actions")
        self.addToolBar(tb)
        

        menu = QMenu("&Modules", self)
        self.menuBar().addMenu(menu)

              


        actionShow = QAction(QIcon(rsrcPath + '/pkg_add_200.png'),
                "&Show", self, priority=QAction.LowPriority, triggered=self.showModules)
        
        menu.addAction(actionShow)
        tb.addAction(actionShow)
        


        actionClean= QAction(QIcon(rsrcPath + '/edit-clear.png'),
                "&CleanAll", self, priority=QAction.LowPriority, triggered=self.showModules)
        
        menu.addAction(actionClean)
        tb.addAction(actionClean)

    def newProject(self):
        fn, fp = QFileDialog.getSaveFileName(self, "Save project as...", self.LAST_DIR,
                "Project Files mk(*.mk);;All Files (*)")

        if not fn:
            return False

        if not fn.endswith(".mk"):
            fn +=".mk"

        self.listSrc.clearAll()
        self.LAST_PROJECT=fn
        self.LAST_DIR = os.path.dirname(fn)
        self.actionSaveProject.setEnabled(True)


    def loadProject(self,filename):
        try:
            self.LAST_DIR=os.path.dirname(filename)
            project = Project(self)
            project.load(filename)
            self.LAST_PROJECT=filename
            self.load(project.Src.Src[0])
            self.listSrc.clearAll()
            self.projects.append(project)
            for src in project.Src.Src:
                self.listSrc.addSrcFile(src)
            textEdit = self.codeTab.currentWidget()
            textEdit.project=None
            textEdit.project=project        
        except  Exception as error:
            print(" Error  Load  project :",error)  
            
        
    def openProject(self):
        fn, _ = QFileDialog.getOpenFileName(self, "Open Project...", self.LAST_DIR,
                 "Project Files mk(*.mk);;All Files (*)")

        self.loadProject(fn)
            

    def saveProject(self):
        textEdit = self.codeTab.currentWidget()
        if textEdit.project:
            textEdit.project.save(None)
        pass

    def projectSaveAs(self):
        fn, fp = QFileDialog.getSaveFileName(self, "Save project as...", self.LAST_DIR,
                "Project Files mk(*.mk);;All Files (*)")

        if not fn:
            return False

        self.LAST_DIR=os.path.dirname(fn)
        self.LAST_PROJECT=fn

        if not fn.endswith(".mk"):
            fn +=".mk"
        
        textEdit = self.codeTab.currentWidget()
        textEdit.project= Project(self)
        textEdit.project.save(fn)
        self.actionSaveProject.setEnabled(True)


    
    def setupProjectActions(self):
        menu = QMenu("&Project", self)
        self.menuBar().addMenu(menu)

        self.actionNewProject = QAction(
                QIcon.fromTheme('document-new',
                        QIcon(rsrcPath + '/filenew.png')),
                "&New", self, priority=QAction.LowPriority, triggered=self.newProject)
        
        menu.addAction(self.actionNewProject)

        self.actionOpenProject = QAction(
                QIcon.fromTheme('document-open',
                        QIcon(rsrcPath + '/fileopen.png')),
                "&Open", self,
                triggered=self.openProject)
        
        menu.addAction(self.actionOpenProject)
        menu.addSeparator()

        self.actionSaveProject = QAction(
                
                        QIcon(rsrcPath + '/filesave.png'),
                "&Save", self,                 triggered=self.saveProject, enabled=False)
        
        menu.addAction(self.actionSaveProject)

        self.actionSaveProjectAs = QAction(QIcon(rsrcPath + '/menu_saveas_200.png'),"Save &As...", self,
                priority=QAction.LowPriority,                triggered=self.projectSaveAs)
        menu.addAction(self.actionSaveProjectAs)
        menu.addSeparator()
 


        menu.addSeparator()
    def setupFileActions(self):
        tb = QToolBar(self)
        tb.setWindowTitle("File Actions")
        self.addToolBar(tb)

        menu = QMenu("&File", self)
        self.menuBar().addMenu(menu)

        self.actionNew = QAction(
                
                        QIcon(rsrcPath + '/NewFile.png'),
                "&New Src Code", self, priority=QAction.LowPriority,
                shortcut=QKeySequence.New, triggered=self.fileNew)
        tb.addAction(self.actionNew)
        menu.addAction(self.actionNew)

        self.actionOpen = QAction(
                
                        QIcon(rsrcPath + '/OpenFile.png'),
                "&Open Src File.", self, shortcut=QKeySequence.Open,
                triggered=self.fileOpen)
        tb.addAction(self.actionOpen)
        menu.addAction(self.actionOpen)
        menu.addSeparator()

        self.actionSave = QAction(
                
                        QIcon(rsrcPath + '/filesave.png'),
                "&Save", self, shortcut=QKeySequence.Save,
                triggered=self.fileSave, enabled=False)
        tb.addAction(self.actionSave)
        menu.addAction(self.actionSave)

        self.actionSaveAs = QAction(  QIcon(rsrcPath + '/menu_saveas_200.png'),"Save File &As...", self,
                priority=QAction.LowPriority,enabled=False,
                shortcut=Qt.CTRL + Qt.SHIFT + Qt.Key_S,
                triggered=self.fileSaveAs)

        menu.addAction(self.actionSaveAs)
        tb.addAction(self.actionSaveAs)
        menu.addSeparator()
 


        menu.addSeparator()

        self.actionQuit = QAction("&Quit", self, shortcut=QKeySequence.Quit,
                triggered=self.close)
        menu.addAction(self.actionQuit)

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
    def setProgress(self,value,code):
        print("Compile ",code," ",value)
    def compileFile(self,FileName,plataform):
        Name=os.path.splitext(os.path.basename(FileName))[0]
        Dir=os.path.dirname(os.path.abspath(FileName))
        filename, file_extension = os.path.splitext(FileName)
        useCPP=False
        if len(file_extension)>=3:
            useCPP=True
        
        code=[]
        code.append(FileName)
        if plataform==0:
            print("Compile linux")
            print(FileName)
            print(Dir)
            print(Name)
            objs = LinuxCompile(self,Dir,Name,code,self.GLOBALARGS.ARGCC,self.GLOBALARGS.ARGCPP,True)
            if (objs):
                LinuxBuild(self,Dir,Name,objs,useCPP,self.GLOBALARGS.ARGLD,False)
    
    def execute(self,cmd,args):
        args = [cmd] + args
        re = subprocess.Popen(args, shell=False,close_fds=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #re.wait()
        chkdata = re.stdout.readlines()
        for line in chkdata:
            lstr=line.decode('utf-8')
            self.trace(lstr)
            
    def runFile(self,FileName,plataform):
        Name=os.path.splitext(os.path.basename(FileName))[0]
        Dir=os.path.dirname(os.path.abspath(FileName))
        filename, file_extension = os.path.splitext(FileName)
        
        if plataform==0:
            print("Run linux")
            print(filename)
            print(Dir)
            print(Name)
            if os.path.exists(filename):
                #self.execute('x-terminal-emulator',['-e','/bin/sh',filename])
                #call_cmd('x-terminal-emulator',['-e',filename])
                # call_cmd('x-terminal-emulator',['-e','bash','-c','/media/djoker/code/linux/python/guis/tabs.py'])
                #self.execute(filename,[])
                #x-terminal-emulator -e 'bash -c "test.py"
                #cmd =shlex.split("""x-terminal-emulator -e '/bin/sh "/media/djoker/code/linux/python/projects/CppEditor/projects/main"'""")
                try:
                    #newCall(filename,[])
                     #self.execute("gnome-terminal",["-e",filename])
                     #self.execute(filename,[])
                             
                    self.worker = ExecuteWorker(self,filename)
                    self.worker.start()
                    
                    #self.runnable = RunWorker(self)
                    #self.runnable.start()
                                 
                except Exception as e:
                    self.trace('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

                #process = subprocess.Popen(
                #shlex.split("""x-terminal-emulator -e 'bash -c "/media/djoker/code/linux/python/guis/tabs.py"'"""), stdout=subprocess.PIPE)
                #shlex.split("""x-terminal-emulator -e '/bin/sh "/media/djoker/code/linux/python/projects/CppEditor/projects/main"'"""), stdout=subprocess.PIPE)
                #process.wait()
                #print (process.returncode)
        
        
            
        
    def compile(self):
        self.ClearConsole()
        self.fileSave()
        textEdit = self.codeTab.currentWidget()
        project = textEdit.project
        if project:
            project.compile(self.currentPlataform)
        else:
            self.compileFile(textEdit.fileName,self.currentPlataform)

    def compileRun(self):
        self.ClearConsole()
        textEdit = self.codeTab.currentWidget()
        project = textEdit.project
        if project:
            project.run(self.currentPlataform)
        else:
            self.runFile(textEdit.fileName,self.currentPlataform)

    def compileAndRun(self):
        self.ClearConsole()
        self.ClearConsole()
        textEdit = self.codeTab.currentWidget()
        project = textEdit.project
        if project:
            project.compile(self.currentPlataform)
            project.run(self.currentPlataform)
    
    def onAbort(self):
        print("Abort")

    def compileClean(self):
        textEdit = self.codeTab.currentWidget()
        project = textEdit.project

        if project:
            project.clean(self.currentPlataform)
            
                
    def load(self, f):
        print("load :",f)
        if not f in self.files:
            self.files.append(f)
        else:
            return False
        
        if not QFile.exists(f):
            return False

        fh = QFile(f)
        if not fh.open(QFile.ReadOnly):
            return False

        data = fh.readAll()
        
        codec = QTextCodec.codecForHtml(data)
        unistr = codec.toUnicode(data)
        self.createEditorFromFile(f,unistr)
        


        return True

    def maybeSave(self):
    
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

    def setCurrentFileName(self):
        textEdit = self.codeTab.currentWidget()
        index= self.codeTab.currentIndex()
        if textEdit:
            self.codeTab.setTabText(index,os.path.basename(textEdit.fileName))
            self.setWindowTitle(self.tr("%s[*] - %s" % (os.path.basename(textEdit.fileName), "Cross IDE Editor @DjokerSoft.")))
        self.setWindowModified(False)
    
    def setCursor(self,x,y):
        textEdit = self.codeTab.currentWidget()
        if textEdit:
            textEdit.setCursorPosition(x,y)

    def fileNew(self):
        
        self.actionSaveAs.setEnabled(True)
        self.createEditor()
        
        
    def fileOpen(self):
        fn, _ = QFileDialog.getOpenFileName(self, "Open File...", self.LAST_DIR,
                "Code files (*.cpp *.c);;All Files (*)")

        self.LAST_DIR=os.path.dirname(fn)
        if fn:
            self.load(fn)

    def fileSave(self):


        index =self.codeTab.currentIndex() 
        textEdit = self.codeTab.currentWidget() 
        textEdit.setModified(False)
        self.setCurrentFileName()


        if not textEdit.fileName:
            return self.fileSaveAs()
        
        
        try:
            with open(textEdit.fileName, 'w') as file:
                file.write(textEdit.text())
        except  Exception as error:
            print(" Error :",error)
            return False
        return True
        

    def fileSaveAs(self):
        textEdit = self.codeTab.currentWidget() 
        fn, _ = QFileDialog.getSaveFileName(self, "Save as...", self.LAST_DIR, "Code Files (*.cpp *.c);;Header files (*.h);;All Files (*)")
        if not fn:
            return False
        

        lfn = fn.lower()
        if not lfn.endswith(('.cpp', '.h', '.c')):
            fn += '.c'
        
        textEdit.fileName=fn
        self.LAST_DIR=os.path.dirname(fn)

        
        

        
        
        #print(textEdit)
        #print(fn)
        #print(self.codeTab.currentIndex())
        #print(self.codeTab.count())
        #print(textEdit.text())
        #self.setCurrentFileName(fn)
        return self.fileSave()

 


    def clipboardDataChanged(self):
        self.actionPaste.setEnabled(len(QApplication.clipboard().text()) != 0)

    def about(self):
        QMessageBox.about(self, "About", 
                "Cross Plataform compiler "
                "Djokersoft "
                "Luis Santos @2021")



 
    def createEditorFromFile(self,fileName,data):
        textEdit = CodeEditor(self)
        textEdit.setLexer(self.cpplexer)
        textEdit.setFocus()
        
        textEdit.fileName=fileName
        textEdit.setText(data)
        self.actionUndo.triggered.connect(textEdit.undo)
        self.actionRedo.triggered.connect(textEdit.redo)
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)
        self.actionCut.triggered.connect(textEdit.cut)
        self.actionCopy.triggered.connect(textEdit.copy)
        self.actionPaste.triggered.connect(textEdit.paste)
        textEdit.copyAvailable.connect(self.actionCut.setEnabled)
        textEdit.copyAvailable.connect(self.actionCopy.setEnabled)
        tabIndex = self.codeTab.addTab(textEdit, os.path.basename(fileName))
        self.codeTab.setCurrentIndex(tabIndex)
        textEdit.modificationChanged.connect(self.actionSave.setEnabled)  
        self.setCurrentFileName()
        self.setCursor(1,1)
        

    def createEditor(self):
        textEdit = CodeEditor(self)
        textEdit.setLexer(self.cpplexer)
        textEdit.setFocus()
        
        textEdit.fileName="untitled.c"
        textEdit.setText("""\
int main(void) 
{
    return 0;
}\
                        """)
        self.actionUndo.triggered.connect(textEdit.undo)
        self.actionRedo.triggered.connect(textEdit.redo)
        self.actionCut.setEnabled(False)
        self.actionCopy.setEnabled(False)
        self.actionCut.triggered.connect(textEdit.cut)
        self.actionCopy.triggered.connect(textEdit.copy)
        self.actionPaste.triggered.connect(textEdit.paste)
        textEdit.copyAvailable.connect(self.actionCut.setEnabled)
        textEdit.copyAvailable.connect(self.actionCopy.setEnabled)
        tabIndex = self.codeTab.addTab(textEdit, os.path.basename(textEdit.fileName))
        self.codeTab.setCurrentIndex(tabIndex)
        textEdit.modificationChanged.connect(self.actionSave.setEnabled)
        self.setCurrentFileName()
        self.setCursor(1,1)
        
    def textChnaged(self):
        print("text change")        


    


    def printFile(self):
        editor = self.codeTab.currentWidget()
        print(editor.Text())

    def loadModules(self,realod=False):
        if realod==True:
            print("Realod")
            
            #self.modulesData=[]
            #self.modulesList=[]
            self.modulesData.clear()
            self.modulesList.clear()
        else:
            if len(self.modulesData)>=1:
                print("modules is loaded")
                return
           

        for root, directories, files in os.walk(modulesPath, topdown=False):
            for name in files:
                ext = os.path.splitext(name)[1]
                if (ext==".json"):
                    #print(os.path.join(root, name)," ",ext," ",directories)
                    module=os.path.join(root, name)
                    self.modulesList.append(module)
                    #print("Load :",module)
                    
                    with open(module) as data:
                        jdata = json.load(data)
                        cModule=CppModule(self)
                        cModule.Dir=root
                        cModule.Name = jdata["module"]
                        cModule.About = jdata["about"]
                        cModule.Author = jdata["author"]
                        cModule.Version = jdata["version"]

                        self.trace("Load ",cModule.Name," module .")
                        self.trace("About ",cModule.About)
                        self.trace("Author ",cModule.Author)
                        self.trace("Version ",cModule.Version)

                        depends = jdata["depends"]
                        for depend in depends:
                            cModule.Depends.append(depend)

                        system = jdata["system"]
                        for sys in system:
                            cModule.System.append(sys)
                        cModule.MainWindow=self
                        
                        for src in jdata["src"]:
                            data = src.strip()
                            if len(data)<=1:
                                continue
                            cModule.MainSrc.Src.append(data)
                            obj=os.path.splitext(data)[0]+'.o'
                            obj = obj.replace("src","obj")
                            if len(obj)>=1:
                                cModule.MainSrc.Objs.append(obj)
                            if showSRCLoad:
                                print("src: ",data)

                        for src in jdata["include"]:
                            cModule.MainSrc.Include.append(src.strip())
                            
                        
                        plataform = jdata["plataforms"]
                        if not plataform:
                            continue

                        if (isLinux):
                            linux = plataform ["linux"]
                            for src in linux["src"]:
                                data = src.strip()
                                if len(data)<=1:
                                    continue
                                cModule.DesktopSrc.Src.append(data)
                                obj=os.path.splitext(data)[0]+'.o'
                                obj = obj.replace("src","obj")
                                if len(obj)>=1:
                                    cModule.DesktopSrc.Objs.append(obj)

                                if showSRCLoad:
                                    print("linux ",data)       

                                
                            for src in linux["include"]:
                                cModule.DesktopSrc.Include.append(src.strip())
                            
                            cppargs = linux["CPP_ARGS"].split(" ")
                            if len(cppargs)>=1:
                                for arg in cppargs:
                                    value =arg.strip()
                                    if len(value)>=1:
                                        cModule.DesktopSrc.ARGS.addCPP(value)

                            ccargs = linux["CC_ARGS"].split(" ")
                            if len(ccargs)>=1:
                                for arg in ccargs:
                                    value =arg.strip()
                                    if len(value)>=1:
                                        cModule.DesktopSrc.ARGS.addCC(value)


                            ldargs = linux["LD_ARGS"].split(" ")
                            if len(ldargs)>=1:
                                for arg in ldargs:
                                    value =arg.strip()
                                    if len(value)>=1:
                                        cModule.DesktopSrc.ARGS.addLD(value)            
                        else:
                            windows = plataform ["windows"]

                            for src in windows["src"]:
                                data = src.strip()
                                if len(data)<=1:
                                    continue
                                cModule.DesktopSrc.Src.append(data)
                                obj=os.path.splitext(data)[0]+'.o'
                                obj=obj.replase("src","obj")
                                if len(obj)>=1:
                                    cModule.DesktopSrc.Objs.append(obj)
                                if showSRCLoad:
                                    print("window ",src)                            
                                
                            for src in windows["include"]:
                                cModule.DesktopSrc.Include.append(src.strip())
                                    
                            cppargs = windows["CPP_ARGS"].split(" ")
                            if len(cppargs)>=1:
                                for arg in cppargs:
                                    value =arg.strip()
                                    if len(value)>=1:
                                        cModule.DesktopSrc.ARGS.addCPP(value)

                            ccargs = windows["CC_ARGS"].split(" ")
                            if len(ccargs)>=1:
                                for arg in ccargs:
                                    value =arg.strip()
                                    if len(value)>=1:
                                        cModule.DesktopSrc.ARGS.addCC(value)


                            ldargs = windows["LD_ARGS"].split(" ")
                            if len(ldargs)>=1:
                                for arg in ldargs:
                                    value =arg.strip()
                                    if len(value)>=1:
                                        cModule.DesktopSrc.ARGS.addLD(value)  
                        
                        android = plataform["android"]
                        for src in android["src"]:
                            data = src.strip()
                            if len(data)<=1:
                                continue
                            cModule.AndroidSrc.Src.append(data)
                            obj=os.path.splitext(data)[0]+'.o'
                            obj = obj.replace("src","obj")
                            if len(obj)>=1:
                                cModule.AndroidSrc.Objs.append(obj)

                            if showSRCLoad:
                                print("android ",src)                            

                            
                        for src in android["include"]:
                            cModule.AndroidSrc.Include.append(src.strip())

                        cppargs = android["CPP_ARGS"].split(" ")
                        if len(cppargs)>=1:
                            for arg in cppargs:
                                value =arg.strip()
                                if len(value)>=1:
                                    cModule.AndroidSrc.ARGS.addCPP(value)

                        ccargs = android["CC_ARGS"].split(" ")
                        if len(ccargs)>=1:
                            for arg in ccargs:
                                value =arg.strip()
                                if len(value)>=1:
                                    cModule.AndroidSrc.ARGS.addCC(value)


                        ldargs = android["LD_ARGS"].split(" ")
                        if len(ldargs)>=1:
                            for arg in ldargs:
                                value =arg.strip()
                                if len(value)>=1:
                                    cModule.AndroidSrc.ARGS.addLD(value)  


                        emscripten = plataform ["emscripten"]
                        for src in emscripten["src"]:
                            data = src.strip()
                            if len(data)<=1:
                                continue
                            cModule.WebSrc.Src.append(data)
                            obj=os.path.splitext(data)[0]+'.o'
                            obj = obj.replace("src","obj")
                            if len(obj)>=1:
                                cModule.WebSrc.Objs.append(obj)                        
                            if showSRCLoad:
                                print("emscripten ",src)                            

                            
                        for src in emscripten["include"]:
                            cModule.WebSrc.Include.append(src.strip())     

                        cppargs = android["CPP_ARGS"].split(" ")
                        if len(cppargs)>=1:
                            for arg in cppargs:
                                value =arg.strip()
                                if len(value)>=1:
                                    cModule.WebSrc.ARGS.addCPP(value)

                        ccargs = emscripten["CC_ARGS"].split(" ")
                        if len(ccargs)>=1:
                            for arg in ccargs:
                                value =arg.strip()
                                if len(value)>=1:
                                    cModule.WebSrc.ARGS.addCC(value)


                        ldargs = emscripten["LD_ARGS"].split(" ")
                        if len(ldargs)>=1:
                            for arg in ldargs:
                                value =arg.strip()
                                if len(value)>=1:
                                    cModule.WebSrc.ARGS.addLD(value)
                        self.modulesData.append(cModule)  
    def getModules(self):
        return self.modulesData

    def getModule(self,name):
        for module in self.modulesData:
            if module.name==name:
                return module
    def closeEvent(self, event):
        
        projList=[]
        for project in self.projects:
            projList.append(project.Root)
        
        
        with open("config.json", 'w') as f:
                f.write('{ \n')
                
                f.write('  "Global":{ \n')
                f.write('  "ArgCPP":'+str(self.GLOBALARGS.ARGCPP).replace("'",'"')+',\n')
                f.write('  "ArgCC":'+str(self.GLOBALARGS.ARGCC).replace("'",'"')+',\n')
                f.write('  "ArgLD":'+str(self.GLOBALARGS.ARGLD).replace("'",'"')+',\n')
                f.write('  "Modules":'+str(self.GLOBALMODULES).replace("'",'"')+',\n')
                f.write('  "Projects":'+str(projList).replace("'",'"')+',\n')
                f.write('  "Files":'+str(self.files).replace("'",'"')+'\n')
                f.write('            }\n')
                f.write('} \n')
                
        self.GLOBALARGS=Args()
        self.GLOBALARGS.ARGCC.append("-std=c99")
        self.GLOBALARGS.ARGCPP.append("-std=c++11")
        self.GLOBALMODULES=[]
        
        
        event.accept()
        '''
        close = QMessageBox()
        close.setText("You sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        '''



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
    if (sys.platform=="linux"):
        isLinux=True
        print(sys.platform)
    else:
        isLinux=False
        print(sys.platform)


    '''proj = Project()
    proj.load("projects/main.mk")
    proj = Project()
    proj.Dir="projects/main"
    proj.Modules.append("raylib")
    proj.Modules.append("box2d")
    proj.Modules.append("jpg")

    proj.addSrc("main/main.c")
    proj.addSrc("main/core.c")
    proj.addSrc("main/utils.c")

    proj.save("main.mk")'''

                   
                
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1024, 780)
    centerPoint = QDesktopWidget().availableGeometry().center()
    
    qtRectangle = window.frameGeometry()
    qtRectangle.moveCenter(centerPoint)
    
    window.move(qtRectangle.topLeft())
    
    window.show()
    #window.createSample()
    sys.exit(app.exec_())
