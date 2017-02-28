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
    SHA = "2a922324cc3f846a33f0d7ed701b8b7483746089"
    return FileSequencerLib.MakeJamfiles(src, filelist, dst, REPOTOP, SHA, "renderdoc", VERSION)

def MakeJamfileForRenderdocCommon(src, filelist, dst):
    SHA = "fd2e84f4c93764ae7b8e5d879eba668d59925bb2"
    return FileSequencerLib.MakeJamfiles(src, filelist, dst, REPOTOP, SHA, "renderdoc", VERSION)

script = "D:\\code\\FileSequencer\\intrenderdoc.txt"

# Step1:
FileSequencerLib.FileSequencerRun(script, ['WIN', 'Packaging'])
# Step2:
#FileSequencerLib.FileSequencerRun(script, ['WIN', 'Install'])