from pyparsing import *
import shutil
import os
import sys
import stat
import colorama
import ast
import re
from subprocess import check_output

PrintStyle = {
    'black'     : colorama.Fore.BLACK, 
    'red'       : colorama.Fore.RED, 
    'green'     : colorama.Fore.GREEN, 
    'yellow'    : colorama.Fore.YELLOW, 
    'blue'      : colorama.Fore.BLUE, 
    'magenta'   : colorama.Fore.MAGENTA, 
    'cyan'      : colorama.Fore.CYAN , 
    'white'     : colorama.Fore.WHITE,
}

ArtifactorySHADict = {}

class Logger:

    def Inf(self, content, style=""):
        if PrintStyle.has_key(style):
            print(PrintStyle[style] + content)
        else:
            print(content)


def FileSequencerInit():
    print("===FileSequencer===")
    colorama.init(autoreset=True)
    from __main__ import *

def isCppFile(p):
    name, ext = os.path.splitext(p)
    if(ext == ".h" or ext == ".hpp" or ext == ".cpp"):
        return True
    else:
        return False

def isExt(p, extIn):
    name, ext = os.path.splitext(p)
    return ext == extIn

def reMatch(p, matchStr):
    pattern = re.compile(matchStr)
    return pattern.match(p) != None

def CppFileFilter(p):
    if(os.path.isdir(p)):
        return True
    return isCppFile(p)

def NotCppFileFilter(p):
    if(os.path.isdir(p)):
        return True
    return not isCppFile(p)

def PDBFilter(p):
    if(os.path.isdir(p)):
        return True
    return isExt(p, ".pdb")

def DLLFilter(p):
    if(os.path.isdir(p)):
        return True
    return isExt(p, ".dll")

def LIBFilter(p):
    if(os.path.isdir(p)):
        return True
    return isExt(p, ".lib")

def JamFilter(p):
    if(os.path.isdir(p)):
        return True
    return isExt(p, ".jam")

def NotJamFilter(p):
    if(os.path.isdir(p)):
        return True
    return not JamFilter(p)


def CreateCommandParser():
    pathElementName = Word(alphanums+"_"+"-"+"."+"%")
    pathElement = "\\" + pathElementName
    quot = Literal("\"").suppress()
    root = Or( (Word(alphas) + Literal(":")) | pathElementName )
    #root =  pathElementName
    Path = quot + Combine( root + ZeroOrMore(pathElement) ) + quot

    ActionSymbolNormal = Literal("=>")
    ActionSymbolSilent = Literal("->")
    ActionSymbolNormalLoop = Literal("=>>")
    ActionSymbolSilentLoop = Literal("->>")
    Action = Word(alphas) + Or( ActionSymbolNormalLoop | ActionSymbolSilentLoop | ActionSymbolNormal | ActionSymbolSilent)

    Filter = Literal(":").suppress() + Word(alphanums+".") 

    ToggleElement = Combine(Word("+"+"-") + Word(alphanums))
    Toggle = ToggleElement + ZeroOrMore(Literal("|").suppress() + ToggleElement)

    Command = Path.setResultsName("src") + Optional(Filter).setResultsName('filter') + Action.setResultsName('cmd') + Optional(Path).setResultsName('dst') + Optional(Toggle).setResultsName("condition")

    return Command

def CreatePathParser():
    PathElement = Word(alphanums+"_"+"-"+"\\"+".").suppress()
    Element = ZeroOrMore(PathElement) + Combine("%" + Word(alphanums) + "%") + ZeroOrMore(PathElement)
    Line = ZeroOrMore(Element)  

    return Line

def ExtractFileList(path, filter=""):
    from __main__ import *
    filelist = []
    if(not os.path.exists(path)):
        return filelist
    if(os.path.isfile(path)):
        if(filter != ""):
            line = r'%s(path)' % (filter)
            if( not eval(line) ) :
                return []
        filelist.append(path)
        return filelist

    items = os.listdir(path)
    for item in items:
        fullpath = os.path.join(path, item)
        if(filter != ""):
            line = r'%s(fullpath)' % (filter)
            if(not eval(line)):
                continue
        if(os.path.isdir(fullpath)):
            filelist.extend(ExtractFileList(fullpath, filter))
        else:
            filelist.append(fullpath)
    
    return filelist

def ExecuteCommand(src, filter, cmd, dst, condition):
    from __main__ import *
    srcList = ExtractFileList(src, filter)
    print(len(srcList))

    line = r'%s(src, srcList, dst)' %(cmd)
    eval(line)

def ExecuteCommandLoop(src, filter, cmd, dst, condition):
    srcList = ExtractFileList(src, filter)
    print(len(srcList))

    for it in srcList:
        li = [it]
        line = r'%s(it, li, dst)' %(cmd)
        eval(line)

def Copy(src, filelist, dst):
    if(len(filelist) > 1 and os.path.isfile(dst)):
        return
    for f in filelist:
        dirPath = os.path.dirname(dst)
        if(not os.path.exists(dirPath)):
            os.makedirs(dirPath)
        shutil.copy(f, dst)

def CopyTree(src, filelist, dst):
    if(os.path.exists(dst) and os.path.isdir(dst)):
        shutil.rmtree(dst)
    if(os.path.isdir(src)):
        shutil.copytree(src, dst)

def Remove(src, filelist, dst):
    for f in filelist:
        os.remove(f)

def RemoveFolder(src, filelist, dst):
    if(os.path.exists(src) and os.path.isdir(src)):
        os.chmod(src, stat.S_IWRITE)
        shutil.rmtree(src)

def MakeWritable(src, filelist, dst):
    for item in filelist:
        os.chmod( item, stat.S_IWRITE )

def MakeZipArchive(src, filelist, dst):
    from __main__ import ZipApp
    if(os.path.exists(src) and os.path.isdir(src)):
        p, e = os.path.splitext(dst)
        dstFolder, basename = os.path.split(dst)
        if(e == ".zip"):
            dstFolder, basename = os.path.split(dst)
        else:
            dstFolder = dst
            basename = "" 
        if(not os.path.exists(dstFolder)):
            os.makedirs(dstFolder)
        if(basename == ""):
            temp0, temp1 = os.path.split(src)
            basename = temp1 + ".zip"
        cmd = '"%s" a %s %s' % (ZipApp, os.path.join(dstFolder, basename), src)
        ret = check_output(cmd, shell = True)
        #print(ret)

def MakeTarGzArchive(src, filelist, dst):
    from __main__ import ZipApp
    if(os.path.exists(src) and os.path.isdir(src)):
        dstFolder, basename = os.path.split(dst)
        if(dst.endswith(".tar.gz")):
            dstFolder, basename = os.path.split(dst)
        else:
            dstFolder = dst
            basename = "" 
        if(not os.path.exists(dstFolder)):
            os.makedirs(dstFolder)
        if(basename == ""):
            temp0, temp1 = os.path.split(src)
            basename = temp1 + ".tar"
        else:
            basename = basename.replace(".gz", "")
        tarPath = os.path.join(dstFolder, basename)
        cmd = '"%s" a %s %s' % (ZipApp, tarPath, src)
        ret = check_output(cmd, shell = True)
        basename += ".gz"
        cmd = '"%s" a %s %s' % (ZipApp, os.path.join(dstFolder, basename), tarPath)
        ret = check_output(cmd, shell = True) 
        os.remove(tarPath) 

def UploadToArtifactory(src, filelist, dst):
    from __main__ import ArtifactoryAPI, ArtifactoryROOT, ArtifactoryUserName, ArtifactoryPassword, jfrogPath, curlPath

    if(os.path.exists(src) and os.path.isfile(src) and src.endswith(".zip")):
        dst = dst.replace("\\", "/")
        # upload archive to Artifactory
        cmd = "%s rt u %s artifactory%s" % (jfrogPath, src, dst)
        #logger.Inf(cmd)
        ret = check_output(cmd, shell = True)
        #logger.Inf(ret)
        # retrieve SHA value from Artifactory
        cmd = "%s -k %s%s -u %s:%s" % (curlPath, ArtifactoryAPI, dst, ArtifactoryUserName, ArtifactoryPassword)
        #logger.Inf(cmd)
        ret = check_output(cmd, shell = True)
        #logger.Inf(ret)
        artifactoryResp = ast.literal_eval(ret)
        key = src.replace(".zip", "")
        ArtifactorySHADict[key] = artifactoryResp["checksums"]["sha1"]

def MakeJamfiles(src, filelist, dst, TOP, SHA, artifactName, artifactBase):
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
            if(len(fileListUnderSrc) > 0 and True):
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
                    jamfileContent += "AWFile " + filename + jamfileLineEnding
                elif(ext == ".dll" or ext == ".pdb" or ext == ".exe"):
                    jamfileContent += "AWInstallFile " + filename + " : bin" + jamfileLineEnding
                elif(ext == ".a"):
                    jamfileContent += "AWInPlaceLib " + filename + " : buildLib" + jamfileLineEnding
                elif(ext == ".so" or ext == ".dylib"):
                    jamfileContent += "AWInstallShared " + filename + " : lib" + jamfileLineEnding
                #elif(ext == ".json" or ext == ".xml" or ext == ".config"):
                #    jamfileContent += "AWInstallFile " + filename + " : bin" + jamfileLineEnding

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
                MakeJamfiles(f, filelist, dst, TOP, SHA, artifactName, artifactBase)