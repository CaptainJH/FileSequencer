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
CndTokensPerLine = []

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

def FileSequencerRun(script, defines = []):
    from __main__ import *
    colorama.init(autoreset=True)   

    logger = Logger()
    logger.Inf("working dir is: %s" % os.getcwd(), 'blue')

    if(not os.path.exists(script)):
        logger.Inf("script: %s doesn't exist!" % script, "red")
        return    

    f = open(script, 'r')
    data = f.read()
    f.close()
    lines = data.splitlines()

    CommandParser = CreateCommandParser()
    PathParser = CreatePathParser()

    global CndTokensPerLine

    for l in lines:
        CndTokensPerLine = []
        try:
            result = CommandParser.parseString(l)
            src = ''
            dst = ''
            cmd = ''
            flt = ''
            cnd = []

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

            cmd = result.cmd
            cmd2= result.cmd2
            isLoop = cmd2.endswith(">>")
            isRecursive = cmd2.startswith("-=") or cmd2.startswith("==")
            if('filter' in result.keys()):
                flt = result.filter[0]

            if('condition' in result.keys() and len(defines) > 0):
                parseResult = result.condition.asList()
                if(not ShouldExecute(defines, parseResult)):
                    continue
            
                
            logger.Inf("src:%s; filter:%s; cmd:%s; dst:%s; condition:%s" % (src, flt, cmd, dst, cnd), "")
            if(isLoop):
                ExecuteCommandLoop(src, flt, isRecursive, cmd, dst, cnd)
            else:
                ExecuteCommand(src, flt, isRecursive, cmd, dst, cnd)

        except:
            logger.Inf(l, "red")

def ShouldExecute(defines, parseResult):
    #print(parseResult)
    global CndTokensPerLine
    resultMapping = {}
    for token in CndTokensPerLine:
        if("+" in token):
            findkey = token.replace("+", "")
            resultMapping[token] = findkey in defines
        elif("-" in token):
            findkey = token.replace("-", "")
            resultMapping[token] = findkey not in defines

    evalStr = ''
    for token in parseResult:
        if("+" in token or "-" in token):
            evalStr += str(resultMapping[token])
        else:
            evalStr += token
    
    evalStr = evalStr.replace("&", " and ")
    evalStr = evalStr.replace("|", " or ")
    result = eval(evalStr)
    return result


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

def IPDBFilter(p):
    if(os.path.isdir(p)):
        return True
    return isExt(p, ".ipdb")

def IOBJFilter(p):
    if(os.path.isdir(p)):
        return True
    return isExt(p, ".iobj")

def AFilter(p):
    if(os.path.isdir(p)):
        return True
    return isExt(p, ".a")

def SOFilter(p):
    if(os.path.isdir(p)):
        return True
    return isExt(p, ".so")

def DEBUGFilter(p):
    if(os.path.isdir(p)):
        return True
    return isExt(p, ".debug")

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

def AddToCndTokensPerLine(p):
    global CndTokensPerLine
    CndTokensPerLine.append(p[0])

def CreateConditionParser():
    expression = Forward()
    term = Or(Combine(Word("+"+"-") + Word(alphanums+".")).setParseAction(AddToCndTokensPerLine) | Literal("(") + expression + Literal(")"))
    expression << term + ZeroOrMore(Or(Literal("|") | Literal("&")) + term)

    return expression


def CreateCommandParser():
    pathElementName = Word(alphanums+"_"+"-"+"."+"%")
    pathElement = "\\" + pathElementName
    quot = Literal("\"").suppress()
    root = Or( (Word(alphas) + Literal(":")) | pathElementName )
    #root =  pathElementName
    Path = quot + Combine( root + ZeroOrMore(pathElement) ) + quot

    Action = Word(alphas).setResultsName("cmd") + Combine(Or( Literal("-") | Literal("=")) + Optional(Literal("=")) + Literal(">") + Optional(Literal(">"))).setResultsName("cmd2")

    Filter = Literal(":").suppress() + Word(alphanums+".") 

    Toggle = CreateConditionParser()

    Command = Path.setResultsName("src") + Optional(Filter).setResultsName('filter') + Action + Optional(Path).setResultsName('dst') + Optional(Toggle).setResultsName("condition")

    return Command

def CreatePathParser():
    PathElement = Word(alphanums+"_"+"-"+"\\"+".").suppress()
    Element = ZeroOrMore(PathElement) + Combine("%" + Word(alphanums) + "%") + ZeroOrMore(PathElement)
    Line = ZeroOrMore(Element)  

    return Line

def ExtractFileList(path, isRecursive, filter=""):
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
        if(os.path.isdir(fullpath) and isRecursive):
            filelist.extend(ExtractFileList(fullpath, isRecursive, filter))
        elif(os.path.isfile(fullpath)):
            if(filter != ""):
                line = r'%s(fullpath)' % (filter)
                if(not eval(line)):
                    continue           
            filelist.append(fullpath)
    
    return filelist

def ExtractFolderList(path, isRecursive, filter=""):
    from __main__ import *
    folderlist = []
    if(not os.path.exists(path)):
        return folderlist
    if(os.path.isfile(path)):
        return folderlist

    items = os.listdir(path)
    for item in items:
        fullpath = os.path.join(path, item)
        if(os.path.isfile(fullpath)):
            continue

        if(isRecursive):
            folderlist.extend(ExtractFolderList(fullpath, isRecursive, filter))

        if(filter != ""):
            line = r'%s(fullpath)' % (filter)
            if(not eval(line)):
                continue 

        folderlist.append(fullpath)
    
    return folderlist

def ExecuteCommand(src, filter, isRecursive, cmd, dst, condition):
    from __main__ import *
    srcFileList = ExtractFileList(src, isRecursive, filter)
    srcFolderList = ExtractFolderList(src, isRecursive, filter)

    outputStr = "files: %d | folders: %d" % (len(srcFileList), len(srcFolderList))
    print(outputStr)

    line = r'%s(src, srcFileList, srcFolderList, dst)' %(cmd)
    eval(line)

def ExecuteCommandLoop(src, filter, isRecursive, cmd, dst, condition):
    srcFileList = ExtractFileList(src, isRecursive, filter)
    print(len(srcFileList))

    srcFolderList = ExtractFolderList(src, isRecursive, filter)
    print(len(srcFolderList))

    for it in srcFileList:
        li = [it]
        line = r'%s(it, li, dst)' %(cmd)
        eval(line)


def Copy(src, filelist, folderlist, dst):
    if(len(filelist) > 1 and os.path.isfile(dst)):
        return
    for f in filelist:
        dirPath = os.path.dirname(dst)
        if(not os.path.exists(dirPath)):
            os.makedirs(dirPath)
        shutil.copy(f, dst)

def CopyToFolder(src, filelist, folderlist, dst):
    if(len(filelist) > 1 and os.path.isfile(dst)):
        return
    for f in filelist:
        dirPath = dst
        if(not os.path.exists(dirPath)):
            os.makedirs(dirPath)
        shutil.copy(f, dst)    

def CopyTree(src, filelist, folderlist, dst):
    if(os.path.exists(dst) and os.path.isdir(dst)):
        shutil.rmtree(dst)
    if(os.path.isdir(src)):
        shutil.copytree(src, dst)

def Remove(src, filelist, folderlist, dst):
    for f in filelist:
        os.remove(f)

    for f in folderlist:
        RemoveFolder(f, [], [], dst)

def RemoveFolder(src, filelist, folderlist, dst):
    if(os.path.exists(src) and os.path.isdir(src)):
        os.chmod(src, stat.S_IWRITE)
        shutil.rmtree(src)

def MakeWritable(src, filelist, folderlist, dst):
    for item in filelist:
        os.chmod( item, stat.S_IWRITE )

def MakeZipArchive(src, filelist, folderlist, dst):
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

def MakeTarGzArchive(src, filelist, folderlist, dst):
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

def UploadToArtifactory(src, filelist, folderlist, dst):
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
                    jamfileContent += "AWFile " + filename + jamfileLineEnding
                elif(ext == ".dll" or ext == ".pdb" or ext == ".exe"):
                    jamfileContent += "AWInstallFile " + filename + " : bin" + jamfileLineEnding
                elif(ext == ".a" or ext == ".lib"):
                    jamfileContent += "AWInPlaceLib " + filename + " : buildLib" + jamfileLineEnding
                elif(ext == ".so" or ext == ".dylib" or ext == ".debug"):
                    jamfileContent += "AWInstallShared " + filename + " : lib" + jamfileLineEnding
                elif(ext == ".gz"):
                    jamfileContent += "AWInstallTarFile" + filename + " : lib" + jamfileLineEnding

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