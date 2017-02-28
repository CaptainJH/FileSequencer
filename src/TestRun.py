import FileSequencerLib
import os
import sys

def HelloWorld():
    print("This is TestRun!")

def Filter1(p):
    print(p)
    return True


#FileSequencerLib.FileSequencerInit()

TOP = "D:\\temp\\test\\forward"
ROOT = "D:\\temp\\test\\root"
ZipApp = "C:\\Program Files\\7-Zip\\7z.exe"


script = "D:\\codeRepo\\FileSequencer\\testFile.txt"
FileSequencerLib.FileSequencerRun(script, ["WIN"])