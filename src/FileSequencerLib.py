from pyparsing import *
import shutil
import os
import sys
import colorama

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



def CreateCommandParser():
    pathElementName = Word(alphanums+"_"+"-"+".")
    pathElement = "\\" + pathElementName
    quot = Literal("\"").suppress()
    root = Or( (Word(alphas) + Literal(":")) | "%" + pathElementName + "%" )
    #root =  pathElementName
    Path = quot + Combine( root + OneOrMore(pathElement) ) + quot

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
            line = r'%s("%s")' % (filter, path)
            if( eval(line) ) :
                filelist.append(path)
        return filelist

    items = os.listdir(path)
    for item in items:
        fullpath = os.path.join(path, item)
        if(filter != ""):
            line = "%s(\"%s\")" % (filter, fullpath)
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

    line = r'%s(srcList, dst)' %(cmd)
    eval(line)

def Copy(filelist, dst):
    for f in filelist:
        shutil.copy(f, dst)

def InitSyntax2():
    pathElementName = Word(alphanums+"_"+"-")
    pathElement = "\\" + pathElementName
    quot = Literal("\"").suppress()
    Path = quot + Combine( Word( alphas ) + ":" + OneOrMore( pathElement ) ) + quot

    ActionSymbolNormal = Literal("=>")
    ActionSymbolSilent = Literal("->")
    Action = Word(alphas) + Or(ActionSymbolNormal | ActionSymbolSilent)

    Filter = Literal(":").suppress() + Word(alphanums+".") 

    ToggleElement = Combine(Word("+"+"-") + Word(alphanums))
    Toggle = ToggleElement + ZeroOrMore(Literal("|").suppress() + ToggleElement)

    Command = Path + Optional(Filter) + Action + Optional(Path) + Optional(Toggle)

    tests = """\
        "D:\\te-mp\\te_mp2":Filter1                     Copy=>          "D:\\temp"  +WIN|-OSX
        "D:\\temp\\temp":FileSequencerLib.Filter2       Copy=>          
        "C:\\temp"                              Archive->       "D:\\temp" \
        """.splitlines()
    # p = "C:\\Users\\juhe\\desktop\\commands.txt"
    # f = open(p, 'r')
    # data = f.read()
    # f.close()
    # tests = data.splitlines()
    # print tests
    for test in tests:
        stats = Command.parseString(test)
        l = stats.asList()
        print l

def InitSyntax3():
    TOP = "C:"
    ROOT = "AnotherTemp"
    s = "%TOP%\\temp\\%ROOT%\\"
    PathElement = Word(alphanums+"_"+"-"+"\\").suppress()
    Element = ZeroOrMore(PathElement) + Combine("%" + Word(alphanums) + "%") + ZeroOrMore(PathElement)
    Line = ZeroOrMore(Element)
    stats = Line.parseString(s)
    print stats.asList()
    for ele in stats.asList():
        tmp = ele.replace("%", "")
        txt = eval(tmp)
        s = s.replace(ele, txt)
        
    print(s)
