import FileSequencerLib
import os
import sys


TOP = "D:\\temp\\test\\integration"
REPOTOP = "D:\\Maya\\git_dev\\maya\\worktrees\\main\\Maya"
MayaBuildStuff = "D:\\Maya\\MayaBuildStuff"
OGSSourceTop = "D:\\OGS\\juhe_SHAGDFTZ22_9335\\2016.11_RC_Maya\\AIRViz\\Devel"
VERSION = "2017.0301"
ZipApp = "D:\\Program Files\\7-Zip\\7z.exe"
ArtifactoryAPI = "https://art-bobcat.autodesk.com/artifactory/api/storage"
ArtifactoryROOT = "/team-maya-generic/renderdoc"
ArtifactoryUserName = 'juhe'
ArtifactoryPassword = 'wOw39001' 
jfrogPath = "C:\\Users\\juhe\\Downloads\\jfrog.exe" # replace with your local path
curlPath = "C:\\Users\\juhe\\AppData\\Local\\Apps\\cURL\\bin\\curl.exe" # replace with your local path

def WinBinaryEXEFilter(p):
    relist = ["^.+EnGen.+.exe", "^.+OGSFragDebug.+.exe"]
    for re in relist:
        if(FileSequencerLib.reMatch(p, re)):
            return True
    return False

def WinBinaryExcludeFilter(p):
    relist = ["^.+OGSCertificationUtility.+$", "^.+OGSDebugUtil.+$", "^.+OGSDeviceDiag.+$", "^.+OGSDeviceDX9.+$", "^.+OGSDeviceDX10.+$", "^.+OGSDeviceNull.+$", "^.+OGSFBX.+$", "^.+OGSDeviceDX9.+$", "^.+OGS.+FontDevice.+$", "^.+OGSFXCompilerApp.+$", "^.+OGSProtein.+$", "^.+OGSRapidRT.+$", "^.+OGSTrace.+$", "^.+SHFontParser.+$", "^.+tbb.+$", "^.+ZipArchive.+$","^.+NsArchive.+$", "^.+FileDecrypter.+$", "^.+HardwareCompatibility.+$", "^.+RPCNode.+$"]
    for re in relist:
        if(FileSequencerLib.reMatch(p, re)):
            return True
    return False

def LinuxBinaryExcludeFilter(p):
    if(os.path.isdir(p)):
        return False
    relist = ["^.+OGSFBX.+$", "^.+OGS.+FontDevice.+$", "^.+OGSProtein.+$", "^.+FontParser.+$", "^.+OGSFX.+$"]
    for re in relist:
        if(FileSequencerLib.reMatch(p, re)):
            return True
    return False

def MacBinaryExcludeFilter(p):
    relist = ["^.+OGSFBX.+$", "^.+EnGen.+$", "^.+OGSRapidRT.+$", "^.+OGSCertificationUtility.+$", "^.+OGS.+FontDevice.+$", "^.+OGSProtein.+$", "^.+FontParser.+$"]
    for re in relist:
        if(FileSequencerLib.reMatch(p, re)):
            return True
    return False  

def MakeJamfileWindows(src, filelist, folderlist, dst):
    SHA = "486b110344d03089f815da3792deda0e5d5e9da5"
    #SHA = ""
    return FileSequencerLib.MakeJamfiles(src, filelist, dst, REPOTOP, SHA, "ogs", VERSION)

def MakeJamfilesForOGSInclude(src, filelist, dst, TOP, SHA, artifactName, artifactBase):
    if(os.path.exists(src) and os.path.isdir(src)):
        if(src.startswith(TOP)):
            temp = src.replace(TOP, "TOP")
            header = temp.replace("\\", " ")
            items = os.listdir(src)
            folderListUnderSrc = []
            fileListUnderSrc = []
            for item in items:
                fullpath = os.path.join(src, item)
                if(os.path.isdir(fullpath)):
                    folderListUnderSrc.append(fullpath)
                if(os.path.isfile(fullpath)):
                    fileListUnderSrc.append(fullpath)

            if(len(folderListUnderSrc) == 0 and len(fileListUnderSrc) == 0):
                return

            jamfileLineEnding = " ;\n"
            jamfileEmptyLine = " \n"
            jamfileContent = ""
            jamfileContent += "AWSubDir " + header + jamfileLineEnding + jamfileEmptyLine
            if(len(fileListUnderSrc) > 0 and SHA != ''):
                jamfileContent += "3rdparty.%s.path = [ GetArtifact %s : %s : true ] ;\n" % (artifactName, artifactName, SHA)
                l = ['', '']
                if(artifactBase != ""):
                    l = header.split(artifactBase)
                jamfileContent += "AWArtifactSubDir [ FDirName $(3rdparty.%s.path) %s %s ] ;\n" %(artifactName, artifactBase, l[1])
            
            jamfileContent += jamfileEmptyLine
            for f in fileListUnderSrc:
                basename, ext = os.path.splitext(f)
                path, filename = os.path.split(f)
                if(ext == ".h"):
                    l = header.split("include")
                    installHeader = l[1].replace("OGS", "")
                    jamfileContent += "AWFile " + filename + "  : install : " + installHeader + jamfileLineEnding

            jamfileContent += jamfileEmptyLine
            for f in folderListUnderSrc:
                fullpath = os.path.join(src, f)
                temp = fullpath.replace(TOP, "TOP")
                path = temp.replace("\\", " ")
                line = "AWSubInclude " + path + jamfileLineEnding
                jamfileContent += line

            jamfilePath = src + "\\Jamfile.jam"
            file = open(jamfilePath, "w")
            file.write(jamfileContent)
            file.close()

            for f in folderListUnderSrc:
                MakeJamfilesForOGSInclude(f, filelist, dst, TOP, SHA, artifactName, artifactBase)

def MakeJamfileCommon(src, filelist, folderlist, dst):
    SHA = "5521eb2977e018d3bac687f41a8631b5e9e7397c "
    #SHA = ""
    return MakeJamfilesForOGSInclude(src, filelist, dst, REPOTOP, SHA, "ogs", VERSION)

def ModifyDXJamFile(src, filelist, folderlist, dst):
    f = open(src, "r")
    data = f.read()
    f.close()
    data += "AWOpenMayaHeader d3dx11effect.h ;\n"
    data += "AWOpenMayaHeader d3dxGlobal.h ;\n"
    f = open(src, "w")
    f.write(data)
    f.close()

def ModifyJamFileForFxencrypt(src, filelist, folderlist, dst):
    f = open(src, "r")
    data = f.read()
    f.close()   
    lines = data.splitlines()
    newdata = ''
    for line in lines:
        if "fxencrypt.exe" in line:
            newdata += "AWInstallExe fxencrypt.exe : buildBin ;\n"
            newdata += "OGS_FXENCRYPT = $(awLastInstallTarget) ;\n"
        else:
            newdata += line + "\n"
    
    f = open(src, "w")
    f.write(newdata)
    f.close()

scriptWin = "D:\\code\\FileSequencer\\intogsWin.txt"
scriptMac = "D:\\code\\FileSequencer\\intogsMac.txt"
scriptLinux = "D:\\code\\FileSequencer\\intogsLinux.txt"

defines = ['install', 'deploy']
#defines = ['deploy']

# Windows:
ROOT = "D:\\temp\\OGS\\OGSIntegration2017\\Daily-0206-0700-WIN"
FileSequencerLib.FileSequencerRun(scriptWin, defines)

# Mac:
def ModifyJamFileToAddFxencrypt(src, filelist, folderlist, dst):
    f = open(src, "r")
    data = f.read()
    f.close()
    lines = data.splitlines()
    newdata = ''
    for line in lines:
        if "AWSubDir" in line:
            newdata += line + "\n"
            newdata += "AWInstallExe fxencrypt : buildBin ;\n"
            newdata += "OGS_FXENCRYPT = $(awLastInstallTarget) ;\n"
        else:
            newdata += line + "\n"
    
    f = open(src, "w")
    f.write(newdata)
    f.close()

def MakeJamfileMac(src, filelist, folderlist, dst):
    SHA = "103a4bfecccc3faa054c4665b91d10412b1fb36f"
    return FileSequencerLib.MakeJamfiles(src, filelist, dst, REPOTOP, SHA, "ogs", VERSION)

def DYLIBFolderFilter(p):
    if(os.path.isfile(p)):
        return False
    reStr = "^.+dylib.dSYM$"
    return FileSequencerLib.reMatch(p, reStr)

def MakeGZArchive(src, filelist, folderlist, dst):
    for folder in folderlist:
        FileSequencerLib.MakeTarGzArchive(folder, [], [], dst)
        FileSequencerLib.RemoveFolder(folder, [], [], "")

def ModifyJamFileForLibxerces(src, filelist, folderlist, dst):
    f = open(src, "r")
    data = f.read()
    f.close()
    lines = data.splitlines()
    newdata = ''
    for line in lines:
        if "libxerces-ad-c-3.1.dylib" in line:
            newdata += "AWInstallShared libxerces-ad-c-3.1.dylib : lib ;\n"
            newdata += "AWInstallSymLink $(awLastInstallTarget) : libxerces-ad-c.dylib : lib ;\n"
        elif "libxerces-ad-c.dylib" in line:
            continue
        else:
            newdata += line + "\n"
    
    f = open(src, "w")
    f.write(newdata)
    f.close()

ROOT = "D:\\temp\\OGS\\OGSIntegration2017\\Daily-0206-0700-MAC"
FileSequencerLib.FileSequencerRun(scriptMac, defines)

# Linux:
def MakeJamfileLinux(src, filelist, folderlist, dst):
    SHA = ""
    return FileSequencerLib.MakeJamfiles(src, filelist, dst, REPOTOP, SHA, "ogs", VERSION)

def ModifyJamFileForLinuxLibs(src, filelist, folderlist, dst):
    f = open(src, "r")
    data = f.read()
    f.close()
    lines = data.splitlines()
    newdata = ''
    for line in lines:
        if "libMgMdfModel_d.so" in line:
            newdata += "AWInstallShared libMgMdfModel_d.so : lib : : : -lMgMdfModel_d ;\n"
        elif "libMgMdfModel.so" in line:
            newdata += "AWInstallShared libMgMdfModel.so : lib : : : -lMgMdfModel ;\n"
        elif "libMgMdfParser_d.so" in line:
            newdata += "AWInstallShared libMgMdfParser_d.so : lib : : : -lMgMdfParser_d ;\n"
        elif "libMgMdfParser.so" in line:
            newdata += "AWInstallShared libMgMdfParser.so : lib : : : -lMgMdfParser ;\n"
        elif "libziparch.so" in line:
            newdata += "AWInstallShared libziparch.so : lib : : : -lziparch ;\n"
        elif "libNsArchive10.so" in line:
            newdata += "AWInstallShared libNsArchive10.so : lib : : : -lNsArchive10 ;\n"
        else:
            newdata += line + "\n"
    
    newdata += "AWInstallShared libxerces-c.so.27 : lib ;\n"

    f = open(src, "w")
    f.write(newdata)
    f.close()

ROOT = "D:\\temp\\OGS\\OGSIntegration2017\\Daily-0206-0700-LNX"
FileSequencerLib.FileSequencerRun(scriptLinux, defines)
