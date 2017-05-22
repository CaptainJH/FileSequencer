import FileSequencerLib
import os
import sys


TOP = "D:\\temp\\test\\integration"
REPOTOP = "D:\\Maya\\git_dev\\maya\\worktrees\\main\\Maya"
#ROOT = "D:\\temp\\RenderDoc_0.32_64"
#ROOT = "D:\\temp\\RenderDoc_0.30_64"
ROOT = "D:\\code\\renderdoc\\x64\\Release"
VERSION = "0.34"
ZipApp = "D:\\Program Files\\7-Zip\\7z.exe"
ArtifactoryAPI = "https://art-bobcat.autodesk.com/artifactory/api/storage"
ArtifactoryROOT = "/team-maya-generic/renderdoc"
ArtifactoryUserName = 'juhe'
ArtifactoryPassword = 'wOw39001' 
jfrogPath = "C:\\Users\\juhe\\Downloads\\jfrog.exe" # replace with your local path
curlPath = "C:\\Users\\juhe\\AppData\\Local\\Apps\\cURL\\bin\\curl.exe" # replace with your local path


def MakeJamfileForRenderdoc(src, filelist, folderlist, dst):
    #SHA = FileSequencerLib.ArtifactorySHADict[src]
    SHA = "be4173bf8753d57997907374535441d7399e3f01 "
    return FileSequencerLib.MakeJamfiles(src, filelist, dst, REPOTOP, SHA, "renderdoc", VERSION)

def MakeJamfileForRenderdocCommon(src, filelist, folderlist, dst):
    SHA = "498937042187271ca07b2ae41970d31279730548 "
    return FileSequencerLib.MakeJamfiles(src, filelist, dst, REPOTOP, SHA, "renderdoc", VERSION)

script = "D:\\code\\FileSequencer\\intrenderdoc.txt"

# Step1:
FileSequencerLib.FileSequencerRun(script, ['WIN', 'Packaging'])
# Step2:
#FileSequencerLib.FileSequencerRun(script, ['WIN', 'Install'])