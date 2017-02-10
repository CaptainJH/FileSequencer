from pyparsing import *
import shutil
import os

def FileSequencerInfo():
    print("===FileSequencer===")


def CreateCommandParser():
    pathElementName = Word(alphanums+"_"+"-"+"%")
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

    return Command

def CreatePathParser():
    PathElement = Word(alphanums+"_"+"-"+"\\").suppress()
    Element = ZeroOrMore(PathElement) + Combine("%" + Word(alphanums) + "%") + ZeroOrMore(PathElement)
    Line = ZeroOrMore(Element)  

    return Line



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
