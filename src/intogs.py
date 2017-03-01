import FileSequencerLib
import os
import sys


TOP = "D:\\temp\\test\\integration"
REPOTOP = "D:\\Maya\\git_dev\\maya\\worktrees\\main\\Maya"
MayaBuildStuff = "D:\\Maya\\MayaBuildStuff"
OGSSourceTop = "D:\\OGS\\juhe_SHAGDFTZ22_9335\\2016.11_RC_Maya\\AIRViz\\Devel"
VERSION = "2017.0225"
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
        return True
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
    SHA = ""
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
    SHA = ""
    return MakeJamfilesForOGSInclude(src, filelist, dst, REPOTOP, SHA, "ogs", VERSION)

scriptWin = "D:\\code\\FileSequencer\\intogsWin.txt"
scriptMac = "D:\\code\\FileSequencer\\intogsMac.txt"
scriptLinux = "D:\\code\\FileSequencer\\intogsLinux.txt"

# Windows:
ROOT = "D:\\temp\\OGS\\OGSIntegration2017\\Daily-0225-0700-WIN"
FileSequencerLib.FileSequencerRun(scriptWin)
# Mac:
def MakeJamfileMac(src, filelist, folderlist, dst):
    SHA = ""
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

ROOT = "D:\\temp\\OGS\\OGSIntegration2017\\Daily-0225-0700-MAC"
#FileSequencerLib.FileSequencerRun(scriptMac)
# Linux:
def MakeJamfileLinux(src, filelist, folderlist, dst):
    SHA = ""
    return FileSequencerLib.MakeJamfiles(src, filelist, dst, REPOTOP, SHA, "ogs", VERSION)
#ROOT = "D:\\temp\\OGS\\OGSIntegration2017\\Daily-0225-0700-LNX"
#FileSequencerLib.FileSequencerRun(scriptLinux)