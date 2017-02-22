import FileSequencerLib
import os
import sys

def HelloWorld():
    print("This is TestRun!")


TOP = "D:\\temp\\test\\integration"
REPOTOP = "D:\\Maya\\git_dev\\maya\\worktrees\\main\\Maya"
#ROOT = "D:\\temp\\RenderDoc_0.32_64"
#ROOT = "D:\\temp\\RenderDoc_0.30_64"
ROOT = "D:\\code\\renderdoc\\x64\\Release"
VERSION = "0.32"
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

FileSequencerLib.FileSequencerInit()

logger = FileSequencerLib.Logger()
logger.Inf("working dir is: %s" % os.getcwd(), 'blue')

f = open("D:\\code\\FileSequencer\\intrenderdoc.txt", 'r')
data = f.read()
f.close()
lines = data.splitlines()

CommandParser = FileSequencerLib.CreateCommandParser()
PathParser = FileSequencerLib.CreatePathParser()


for l in lines:
    try:
        result = CommandParser.parseString(l)
        src = ''
        dst = ''
        cmd = ''
        flt = ''
        cnd = ''

        if('src' in result.keys()):
            src = result.src[0]
            stats = PathParser.parseString(src)
            for ele in stats:
                tmp = ele.replace("%", "")
                txt = eval(tmp)
                src = src.replace(ele, txt)

        if('dst' in result.keys()):
            dst = result.dst[0]
            stats = PathParser.parseString(dst)
            for ele in stats:
                tmp = ele.replace("%", "")
                txt = eval(tmp)
                dst = dst.replace(ele, txt)

        cmd = result.cmd[0]
        isLoop = result.cmd[1].endswith(">>")
        if('filter' in result.keys()):
            flt = result.filter[0]
        if('condition' in result.keys()):
            for c in result.condition:
                cnd += c + " "
        
        logger.Inf("src:%s; filter:%s; cmd:%s; dst:%s; condition:%s" % (src, flt, cmd, dst, cnd), "")
        if(isLoop):
            FileSequencerLib.ExecuteCommandLoop(src, flt, cmd, dst, cnd)
        else:
            FileSequencerLib.ExecuteCommand(src, flt, cmd, dst, cnd)

    except:
        logger.Inf(l, "red")