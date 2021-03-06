# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_org.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import io
import os
import sys
from subprocess import STDOUT, PIPE
import argparse
import shutil
import time
import json
import re
import subprocess
from subprocess import check_output, CalledProcessError, STDOUT
from datetime import datetime

import http.server
import socketserver


import zipfile


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

ANDROID_SDK="/home/djoker/Android/Sdk"
ANDROID_NDK="/home/djoker/Android/Sdk/ndk/23.1.7779620"
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

PORT = 8080
DIRECTORY = "/media/djoker/code/linux/python/projects/CppEditor/projects/Web/main"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)



def trace(*args):
    result = ""
    for x in args:
        result += x
    print(result)
 


SHOW_COMMAND=True
    
        
def runProcess(command, args=[],wait=True):
    args = [command] + args
    def cmd_args_to_str(cmd_args):
        return ' '.join([arg if not ' ' in arg else '"%s"' % arg for arg in cmd_args])


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
                
    #else:
    #    print("Process directory ",maindir," already exists")


#buildType 0 app 1, shared 2 static

            


def androidCompileJavaNative(mainRoot,appName,ANDROID_PACK,ANDROID_LABEL,ANDROID_ACTIVITY,runApp):


    OSP=os.path.sep
    binFolder=mainRoot+OSP+"Android"+OSP+appName+OSP

   



    
    java = binFolder+"java"
    if not os.path.exists(java):
        trace("Create :"+java)
        os.mkdir(java)

    tmp = binFolder+"tmp"
    if not os.path.exists(tmp):
        trace("Create :"+tmp)
        os.mkdir(tmp)

    javaOut =binFolder+"out"
    if not os.path.exists(javaOut):
        trace("Create :"+javaOut)
        os.mkdir(javaOut)


    res = binFolder+"res"
    if not os.path.exists(res):
        trace("Create :"+res)
        os.mkdir(res)

    dexFiles = binFolder+"dex"
    if not os.path.exists(dexFiles):
        trace("Create :"+dexFiles)
        os.mkdir(dexFiles)


    javaFileDirs =java + OSP +ANDROID_PACK.replace(".",OSP)
    
    createFolderTree(javaFileDirs)




    #createFolderTree(javaFileDirs)


    manifFile=binFolder+"AndroidManifest.xml"
    global nativeManifeste

    nativeManifeste=nativeManifeste.replace("@apppkg@",ANDROID_PACK)
    nativeManifeste=nativeManifeste.replace("@applbl@",ANDROID_LABEL)
    nativeManifeste=nativeManifeste.replace("@appactv@",ANDROID_PACK+"."+ANDROID_ACTIVITY)
    if not os.path.exists(binFolder+"AndroidManifest.xml"):
        with open(binFolder+"AndroidManifest.xml", "w") as text_file:
            text_file.write(nativeManifeste)

    global javaNative
    javaNative=javaNative.replace("@apppkg@",ANDROID_PACK)
    javaNative=javaNative.replace("@appactv@",ANDROID_ACTIVITY)
    if not os.path.exists(javaFileDirs+OSP+ANDROID_ACTIVITY+".java"):
        with open(javaFileDirs+OSP+ANDROID_ACTIVITY+".java", "w") as text_file:
            text_file.write(javaNative)

    

    debugKey=binFolder+appName+".key"
    if not os.path.exists(debugKey):
        trace(" Generate "+debugKey+" keystor")
        args=[]
        args.append("-genkeypair")
        args.append("-validity")
        args.append("1000")  # mil anos???
        args.append("-dname")
        args.append("CN=djokersoft,O=Android,C=PT")
        args.append("-keystore")
        args.append(debugKey)
        args.append("-storepass")
        args.append("14781478")  #change pass
        args.append("-keypass")
        args.append("14781478")
        args.append("-alias")
        args.append("djokersoft")
        args.append("-keyalg")
        args.append("RSA")

        finalCommand = cmd_args_to_str(args)
        trace("keytool "+finalCommand)
        code, out, err=runProcess("keytool",args)
        if code!=0:
            trace("Error on generate keystore:"+err.decode("utf-8") )
            return False
        trace(out.decode("utf-8"))  


        


    args=[]
    args.append("package")
    args.append("-f")
    args.append("-m")
    args.append("-J")
    args.append(java)
    args.append("-M")
    args.append(manifFile)
    args.append("-S")
    args.append(res)
    args.append("-I")
    args.append(PLATFORM)

    trace("Generate resources .")
    code, out, err=runProcess(AAPT,args)
    if code!=0:
        trace("Error on generate resources:"+err.decode("utf-8") )
        return False
    trace(out.decode("utf-8"))    
    trace("Search java files ") 

    javaSrcFiles=[]
    for root, dirs, files in os.walk(java):
        for file in files:
            if file.endswith(".java"):
                print(os.path.join(root, file))   
                javaSrcFiles.append(os.path.join(root, file))

    javaSrcFiles.sort(reverse=True) 

    for src in javaSrcFiles:
        trace("Compile "+ src.strip())
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
        args.append(javaOut)
        #args.append("-bootclasspath")
        #args.append(JAVA_LIB_RT)
        args.append("-classpath")
        args.append(PLATFORM+":"+javaOut)
        args.append("-sourcepath")
        args.append(java+":"+java+"/org"+":"+javaOut)
        args.append(src)

        src_modified_time = os.path.getmtime(src)
        src_convert_time = time.ctime(src_modified_time)

        filename, file_extension = os.path.splitext(src)
        basename = os.path.basename(src)
        basename_without_ext = os.path.splitext(os.path.basename(src))[0]
        maindir = os.path.dirname(os.path.abspath(src))
        maindir = maindir.replace("java","out")
        objName=maindir+os.path.sep+basename_without_ext+".class"

        if os.path.exists(objName):
            obj_modified_time = os.path.getmtime(objName)
            obj_convert_time = time.ctime(obj_modified_time)
            if (src_convert_time<obj_convert_time):
                trace("Skip "+ src)
                continue
        
        
        code, out, err=runProcess("javac",args)
        if code!=0:
            trace("Error  compiling :"+err.decode("utf-8") )
            return False
        trace(out.decode("utf-8"))  
       

    trace('Java is compiled ...')

    trace('Translating in Dalvik bytecode...')
    args=[]
    args.append("--dex")
    args.append("--output="+dexFiles+os.path.sep+"classes.dex")
    args.append(javaOut)
    
    code, out, err=runProcess(DX,args)
    if code!=0:
        trace("Error  Translating java do dex :"+err.decode("utf-8") )
        return False
    trace(out.decode("utf-8"))  

    trace('Making APK...')

    args=[]
    args.append("package")
    args.append("-f")
    args.append("-m")
    args.append("-F")
    args.append(tmp+os.path.sep+appName+".unaligned.apk")
    args.append("-M")
    args.append(manifFile)
    args.append("-S")
    args.append(res)
    args.append("-I")
    args.append(PLATFORM)
    
    
    code, out, err=runProcess(AAPT,args)
    if code!=0:
        trace("Error  packing apk :"+err.decode("utf-8") )
        return False
    trace(out.decode("utf-8")) 

    trace("File is created in "+tmp+os.path.sep+appName+".unaligned.apk")

    zip = zipfile.ZipFile(tmp+os.path.sep+appName+".unaligned.apk",'a')
    buildOutputArm='armeabi-v7a'
    appBin = binFolder+buildOutputArm+os.path.sep+"lib"+appName+".so"
    
    if os.path.exists(appBin):
        trace("insert ",appBin)
        zip.write(appBin,"lib/armeabi-v7a/"+"lib"+appName+".so")
    else:
        trace("missing ",appBin)

    buildOutputArm='arm64-v8a'
    appBin = binFolder+buildOutputArm+os.path.sep+"lib"+appName+".so"
    
    if os.path.exists(appBin):
        trace("insert ",appBin)
        zip.write(appBin,"lib/arm64-v8a/"+"lib"+appName+".so")
    else:
        trace("missing ",appBin)


    dexListFiles=[]
    trace("look for dex files on ",dexFiles)
    for root, dirs, files in os.walk(dexFiles):
        for file in files:
            if file.endswith(".dex"):
                print("DEX: ",os.path.join(root, file)," filename :",os.path.basename(file))   
                dexListFiles.append(os.path.join(root, file))
    
    for dex in dexListFiles:
        trace("Insert ", dex ," to "+os.path.basename(dex))
        zip.write(dex,os.path.basename(dex))


    #zip.write(dexFiles+"classes.dex","classes.dex")
    zip.close()

    appSigned = binFolder+appName+".signed.apk"
    trace("Sign app ")
    args=[]
    args.append("sign")
    args.append("--ks")
    args.append(debugKey)
    args.append("--ks-key-alias")
    args.append("djokersoft")
    args.append("--ks-pass")
    args.append("pass:14781478")
    args.append("--in")
    args.append(tmp+os.path.sep+appName+".unaligned.apk")
    args.append("--out")
    args.append(appSigned)
    
    trace(cmd_args_to_str(args))
    
    code, out, err=runProcess(APKSIGNER,args)
    if code!=0:
        trace("Error  packing apk :"+err.decode("utf-8") )
        return False
    trace(out.decode("utf-8")) 

    trace("Build competed ;D ")

    trace("Try stop  "+ANDROID_PACK+"...")
    args=[]
    args.append("shell")
    args.append("am")
    args.append("force-stop")
    args.append(ANDROID_PACK+"/."+ANDROID_ACTIVITY)
    code, out, err=runProcess(ANDROID_SDK+"/platform-tools/adb",args)
    if code!=0:
        trace("Error  stoping  apk :"+err.decode("utf-8") )
    trace(out.decode("utf-8")) 

    trace('Try remove app ...')
    args=[]
    args.append("uninstall")
    args.append(ANDROID_PACK)
    code, out, err=runProcess(ANDROID_SDK+"/platform-tools/adb",args)
    if code!=0:
        trace("Error  uninstall  apk :"+err.decode("utf-8") )
    trace(out.decode("utf-8")) 

    trace('Try install app ...')
    args=[]
    args.append("install")
    args.append("-r")
    args.append(appSigned)
    code, out, err=runProcess(ANDROID_SDK+"/platform-tools/adb",args)
    if code!=0:
        trace("Error  installing  apk :"+err.decode("utf-8") )
        
    trace(out.decode("utf-8")) 

    trace('Try run app ...')
    args=[]
    args.append("shell")
    args.append("am")
    args.append("start")
    args.append("-n")
    args.append(ANDROID_PACK+"/."+ANDROID_ACTIVITY)
    
    code, out, err=runProcess(ANDROID_SDK+"/platform-tools/adb",args)
    if code!=0:
        trace("Error  running  apk :"+err.decode("utf-8") )
        return False
    trace(out.decode("utf-8")) 
    return True




def AndroidCompile(folderRoot ,name, srcs ,CARGS,CPPARGS, LDARGS,buildType=0,arm=0,fullBuild=False):
    useCPP=False
    linkCPP=False


        
    OSP=os.path.sep    
    buildPlataform='23'
    buildOutputArm='armeabi-v7a'
    buildArch='armv7a'
    
    armTarget="armv7-none-linux-androideabi16"
    
    
    
    if arm==1:
        buildOutputArm ='arm64-v8a'
        buildArch ='aarch64'
        armTarget='aarch64-none-linux-android21'
    
    
    
    buildHost='linux-x86_64'
    
    CC  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/clang'
    CPP =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/clang++'
    
    AR  =ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/llvm-ar'
    STRIP=ANDROID_NDK+'/toolchains/llvm/prebuilt/'+buildHost+'/bin/llvm-strip'
    
    

    outFolder=folderRoot+OSP+"obj"+OSP+"Android"+OSP+name+OSP+buildOutputArm
    binFolder=folderRoot+OSP+"Android"+OSP+name+OSP+buildOutputArm
    createFolderTree(outFolder)
    createFolderTree(binFolder)
    objsList=[]
    args=[]

    
    

    cExtencions=['.c','.cc']
    cppExtencions=['.cpp','xpp']
    for src in srcs:
        if not os.path.isfile(src):
            trace("File not exists")
            continue
        
        
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


                
                
        args.clear()
        if not fullBuild:       
            if os.path.exists(objName):
                obj_modified_time = os.path.getmtime(objName)
                obj_convert_time   = time.ctime(obj_modified_time)
                if (src_convert_time<obj_convert_time):
                    trace("Skip  file"+ src)
                    continue
            
                 
        cType = CC
       
        if file_extension in cppExtencions:
        #if len(file_extension)>=3:
                cType=CPP
                useCPP=True
                linkCPP=True
        else:
            useCPP=False
            pass
        
        trace (cType," ",os.path.basename(src),">",os.path.basename(objName))

            
        args.append("-target")
        args.append(armTarget)
        args.append("-fdata-sections") 
        args.append("-ffunction-sections")
        args.append("-fstack-protector-strong")
        args.append("-funwind-tables")
        args.append("-no-canonical-prefixes")
        args.append("--sysroot")
        args.append(ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/sysroot")    
        args.append("-g")
        args.append("-Wno-invalid-command-line-argument")
        args.append("-Wno-unused-command-line-argument")
        #args.append("-fno-stack-protector")
        args.append("-D_FORTIFY_SOURCE=2")
        args.append("-fno-exceptions")  #?
        args.append("-fno-rtti")          #?
        
        args.append("-fpic")
        
         
        if arm==0:
            args.append("-march=armv7-a")
            args.append("-mthumb")
            args.append("-Oz")
        elif  arm==1:   
            args.append("-O2")
        args.append("-DNDEBUG")
            
        if arm==0:
            args.append("-I"+ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include/arm-linux-androideabi")
        elif arm==1:
           args.append("-I"+ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include/aarch64-linux-android")
        
        
        if useCPP:
            args.append("-I"+ANDROID_NDK+"/sources/cxx-stl/llvm-libc++/include")
            args.append("-I"+ANDROID_NDK+"/sources/cxx-stl/llvm-libc++abi/include")
            
        args.append("-I"+ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include")
        
           


        args.append("-I"+folderRoot)    
        args.append("-I"+srcFolder)
        #rootFolder=os.getcwd()+OSP+"include"
        #args.append("-I"+rootFolder)
        
  
        #args.append("-nostdinc++")
        
        args.append("-DANDROID")
        args.append("-nostdinc++") 
        args.append("-Wformat")
        args.append("-Werror=format-security")
        args.append("-fno-strict-aliasing") 
        args.append("-DPLATFORM_ANDROID")
        
        




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



        args.append("-c")
        args.append(src)
        args.append("-o")
        args.append(objName)
        #print(args)
        


                    


                        
            
        code, out, err=runProcess(cType,args)
        #print("err: '{}'".format(str(err)))
        #print("exit: {}".format(code))
        if code!=0:
            trace(err.decode("utf-8") )
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
            except:
                print("Erro unknow .. ")
            return False
        trace(out.decode("utf-8") )
    trace("Compiling completed")

     
    
    if buildType==0 or buildType==1:
        args=[]
        linkCPP=True
        export = binFolder+OSP+"lib"+name+".so"
        trace("Build app ",buildArch," ",export )
        args.append("-Wl,-soname,"+"lib"+name+".so")
        args.append("-shared")

        objs=""
        for obj in objsList:
            objs+=obj+' '
            args.append(obj)
  
        rootFolder=os.getcwd()+"/libs/android/"+buildOutputArm      
        args.append("-L"+rootFolder)
        
        
        if linkCPP:    
            #args.append("-L"+ANDROID_NDK+"platforms/android-"+buildPlataform+"/arch-arm/usr/lib")
            args.append("-L"+ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/lib"+OSP)  
            args.append("-L"+ANDROID_NDK+"/sources/cxx-stl/llvm-libc++/libs"+OSP+buildOutputArm+OSP)


        for arg in LDARGS:
            value =arg.strip()
            if len(value)>1:
                args.append(value)

        args.append("-Wl,--no-whole-archive")
        
        #args.append("-lgcc")
        #args.append("-Wl,--exclude-libs,libgcc.a")
        #args.append("-Wl,--exclude-libs,libgcc_real.a")
        if linkCPP:    
            args.append(ANDROID_NDK+"/sources/cxx-stl/llvm-libc++/libs"+OSP+buildOutputArm+OSP+"libc++_static.a")
            args.append(ANDROID_NDK+"/sources/cxx-stl/llvm-libc++/libs"+OSP+buildOutputArm+OSP+"libc++abi.a")
            if arm==0:
                args.append(ANDROID_NDK+"/sources/cxx-stl/llvm-libc++/libs"+OSP+buildOutputArm+OSP+"libandroid_support.a")
        
        if arm==0:
            args.append(ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/lib64/clang/12.0.8/lib/linux/arm/libunwind.a")

        elif arm==1:
            args.append(ANDROID_NDK+"/toolchains/llvm/prebuilt/linux-x86_64/lib64/clang/12.0.8/lib/linux/aarch64/libunwind.a")    
        
        

       
        
        #args.append("-latomic")
        #args.append("-Wl,--exclude-libs,libatomic.a")
        args.append("-target")
        if arm==0:
            args.append("armv7-none-linux-androideabi16")
            
        elif  arm==1:   
            args.append("aarch64-none-linux-android21")
            
        args.append("-no-canonical-prefixes")
        args.append("-Wl,--build-id")
        
        args.append("-nostdlib++")
        args.append("-Wl,--no-undefined")
        args.append("-Wl,--fatal-warnings")
        
        
      
        args.append("-o")
        args.append(export)
        
    

        if linkCPP:
            cType=CPP
        

        code, out, err=runProcess(cType,args)
        if code!=0:
            trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error:'
            return False
        trace(out.decode("utf-8"))


        trace("Strip library ")
        code, out, err=runProcess(STRIP,["--strip-unneeded",export])
        if code!=0:
            trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error:'
            return False
        trace(out.decode("utf-8"))
        trace("Native Done :) ")
        return True
            
      
      

    if buildType==2:
        trace("Build static lib")
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
            trace(err.decode("utf-8") )
            rexp=':(.*?):(.*?): error:'
            return False
        trace(out.decode("utf-8"))
        trace("Static build completed :) ")
        return True

        
srcs=[]
path = os.path.normpath("/media/djoker/code/linux/python/projects/CppEditor/modules/json/src")
for root, directories, files in os.walk(path, topdown=False):
    for name in files:
        ext = os.path.splitext(name)[1]
        if (ext==".c"):
            src=os.path.join(root, name)
            srcs.append(src)
            
            
print(srcs)         


folderRoot="/media/djoker/code/linux/python/projects/CppEditor/modules/json/"
name="json"



CARGS=[]

CARGS.append("-I/media/djoker/code/linux/python/projects/CppEditor/modules/json/src/")
CARGS.append("-I/media/djoker/code/linux/python/projects/CppEditor/modules/json/include/")
CARGS.append("-Wall")
CARGS.append("-std=c99")
CARGS.append("-D_DEFAULT_SOURCE")


CPPARGS=[]
CPPARGS.append("-Wall")
CPPARGS.append("-std=c++11")
CPPARGS.append("-D_DEFAULT_SOURCE")


LDARGS=[]
LDARGS.append("-uANativeActivity_onCreate")
LDARGS.append("-llog")
LDARGS.append("-landroid")
LDARGS.append("-lEGL")
LDARGS.append("-lGLESv1_CM")
LDARGS.append("-llog")
LDARGS.append("-landroid")
LDARGS.append("-lc")
LDARGS.append("-lm")
 
AndroidCompile(folderRoot ,name, srcs ,CARGS,CPPARGS, LDARGS,1,0,True)
#AndroidCompile(folderRoot ,name, src ,CARGS,CPPARGS, LDARGS,0,1,True)

