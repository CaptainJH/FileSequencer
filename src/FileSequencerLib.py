from pyparsing import *
import shutil
import os
import sys
import colorama
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


def CppFileFilter(p):
    if(os.path.isdir(p)):
        return True
    name, ext = os.path.splitext(p)
    if(ext == ".h" or ext == ".hpp" or ext == ".cpp"):
        return True
    else:
        return False

def NotCppFileFilter(p):
    if(os.path.isdir(p)):
        return True
    name, ext = os.path.splitext(p)
    if(ext == ".h" or ext == ".hpp" or ext == ".cpp"):
        return False
    else:
        return True


def CreateCommandParser():
    pathElementName = Word(alphanums+"_"+"-"+".")
    pathElement = "\\" + pathElementName
    quot = Literal("\"").suppress()
    root = Or( (Word(alphas) + Literal(":")) | "%" + pathElementName + "%" )
    #root =  pathElementName
    Path = quot + Combine( root + ZeroOrMore(pathElement) ) + quot

    ActionSymbolNormal = Literal("=>")
    ActionSymbolSilent = Literal("->")
    Action = Word(alphas) + Or(ActionSymbolNormal | ActionSymbolSilent)

    Filter = Literal(":").suppress() + Word(alphanums+".") 

    ToggleElement = Combine(Word("+"+"-") + Word(alphanums))
    Toggle = ToggleElement + ZeroOrMore(Literal("|").suppress() + ToggleElement)

    Command = Path.setResultsName("src") + Optional(Filter).setResultsName('filter') + Action.setResultsName('cmd') + Optional(Path).setResultsName('dst') + Optional(Toggle).setResultsName("condition")

    return Command

def CreatePathParser():
    PathElement = Word(alphanums+"_"+"-"+"\\").suppress()
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
    srcList = ExtractFileList(src, filter)
    print(len(srcList))

    line = r'%s(src, srcList, dst)' %(cmd)
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
