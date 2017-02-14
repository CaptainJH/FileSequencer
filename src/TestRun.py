import FileSequencerLib
import os
import sys

def HelloWorld():
    print("This is TestRun!")

def Filter1(p):
    print(p)
    return True


FileSequencerLib.FileSequencerInit()

TOP = "D:\\temp\\test\\forward"
ROOT = "D:\\temp\\test\\root"
ZipApp = "C:\\Program Files\\7-Zip\\7z.exe"

logger = FileSequencerLib.Logger()
logger.Inf("working dir is: %s" % os.getcwd(), 'blue')

f = open("testFile.txt", 'r')
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
        if('filter' in result.keys()):
            flt = result.filter[0]
        if('condition' in result.keys()):
            for c in result.condition:
                cnd += c + " "
        
        logger.Inf("src:%s; filter:%s; cmd:%s; dst:%s; condition:%s" % (src, flt, cmd, dst, cnd), "")
        FileSequencerLib.ExecuteCommand(src, flt, cmd, dst, cnd)

    except:
        logger.Inf(l, "red")


