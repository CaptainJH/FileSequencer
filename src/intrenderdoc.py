import FileSequencerLib
import os
import sys


TOP = "D:\\temp\\test\\integration"
REPOTOP = "D:\\Maya\\git_dev\\maya\\worktrees\\main\\Maya"
#ROOT = "D:\\temp\\RenderDoc_0.32_64"
#ROOT = "D:\\temp\\RenderDoc_0.30_64"
ROOT = "D:\\code\\renderdoc\\x64\\Release"
VERSION = "0.33"
ZipApp = "D:\\Program Files\\7-Zip\\7z.exe"
ArtifactoryAPI = "https://art-bobcat.autodesk.com/artifactory/api/storage"
ArtifactoryROOT = "/team-maya-generic/renderdoc"
ArtifactoryUserName = 'juhe'
ArtifactoryPassword = 'wOw39001' 
jfrogPath = "C:\\Users\\juhe\\Downloads\\jfrog.exe" # replace with your local path
curlPath = "C:\\Users\\juhe\\AppData\\Local\\Apps\\cURL\\bin\\curl.exe" # replace with your local path


def FilterRETest1(p):
    if(os.path.isdir(p)):
        return True
    return not FileSequencerLib.reMatch(p, "^.*vector.*$")

def MakeJamfileForRenderdoc(src, filelist, dst):
    #SHA = FileSequencerLib.ArtifactorySHADict[src]
    SHA = "574a2cbaf277702ed27a76b8fa539da95c72e8d7"
    return FileSequencerLib.MakeJamfiles(src, filelist, dst, REPOTOP, SHA, "renderdoc", VERSION)

def MakeJamfileForRenderdocCommon(src, filelist, dst):
    SHA = "f96e53de53c24e662dbe05b09a5785733e16f4f4"
    return FileSequencerLib.MakeJamfiles(src, filelist, dst, REPOTOP, SHA, "renderdoc", VERSION)

script = "D:\\code\\FileSequencer\\intrenderdoc.txt"
FileSequencerLib.FileSequencerRun(script)