#-*- coding:utf-8 -*-
"""deva_unicode.py
 
 
"""
from __future__ import print_function
import sys, re,codecs

def print_unicode(u,f):
 """ Sample output:
u = arbitrary unicode
0905 | अ | DEVANAGARI LETTER A
0951 | ॑ | DEVANAGARI STRESS SIGN UDATTA
0902 | ं | DEVANAGARI SIGN ANUSVARA
0936 | श | DEVANAGARI LETTER SHA
2014 | — | EM DASH
092D | भ | DEVANAGARI LETTER BHA
0942 | ू | DEVANAGARI VOWEL SIGN UU
0951 | ॑ | DEVANAGARI STRESS SIGN UDATTA
 """
 import unicodedata
 outarr = []
 outarr.append('INPUT = %s' %u)
 for c in u:
  name = unicodedata.name(c)
  icode = ord(c)
  a = f"{icode:04X} | {c} | {name}"
  outarr.append(a)
 for out in outarr:
  f.write(out+'\n')
 f.write('\n')

def test(fileout):
 tests = [
  'नैर्ऋति',
  'नैरृति',
 ]
 f = codecs.open(fileout,"w","utf-8")
 for x in tests:
  print_unicode(x,f)
 exit(1)

if __name__=="__main__":
 fileout = sys.argv[1]
 test(fileout)
 #test1()
 tranout = sys.argv[2]
 filein = sys.argv[3] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[4] # 
 
 with codecs.open(filein,"r","utf-8") as f:
  with codecs.open(fileout,"w","utf-8") as fout:
   inentry = False
   for iline,line in enumerate(f):
    line = line.rstrip('\r\n')
    if inentry:
     # inentry = True
     if line.startswith('<LEND>'):
      lineout = line
      inentry = False
     elif line.startswith('<L>'):  # error
      print('Error 1. Not expecting <L>')
      print("line # ",iline+1)
      print(line)
      exit(1)
     else:
      # keep looking for <LEND
      lineout = convert(line,tranin,tranout)
    else:
     # inentry = False
     if line.startswith('<L>'):
      lineout = convert_metaline(line,tranin,tranout)
      inentry = True
     elif line.startswith('<LEND>'): # error
      print('Error 2. Not expecting <LEND>')
      print("line # ",iline+1)
      print(line)
      exit(1)
     else:
      # line outside of <L>...<LEND>
      lineout = line
    fout.write(lineout+'\n')
    if False: # True:
     if iline > 1000:
      print('quit at iline=',iline)
      break
