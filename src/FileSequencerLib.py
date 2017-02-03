from pyparsing import *

def FileSequencerInfo():
    print("===FileSequencer===")

def InitSyntax():
    num = Word(nums)
    data = Combine( num + "/" + num + "/" + num )
    schoolName = OneOrMore( Word(alphas) )

    score = Word(nums)
    schoolAndScore = schoolName + score
    gameResult = data + schoolAndScore + schoolAndScore

    tests = """\
        09/04/2004 Virginia 44  Temple          14
        09/04/2004 LSU      22  Oregon State    21""".splitlines()

    for test in tests:
        stats = gameResult.parseString(test)
        print stats.asList()

def InitSyntax2():
    pathElementName = Word(alphanums+"_"+"-")
    pathElement = "\\" + pathElementName
    quot = Literal("\"").suppress()
    Path = quot + Combine( Word( alphas ) + ":" + OneOrMore( pathElement ) ) + quot

    ActionSymbol = Literal("=>").suppress()
    Action = Word(alphas) + ActionSymbol

    Command = Path + Action + Path

    tests = """\
        "D:\\te-mp\\te_mp2" Copy=>  "D:\\temp"
        "C:\\temp" Archive=> "D:\\temp" """.splitlines()
    for test in tests:
        stats = Command.parseString(test)
        print stats.asList()
