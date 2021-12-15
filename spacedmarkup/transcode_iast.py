#-*- coding:utf-8 -*-
"""transcode_iast.py
 
"""
from __future__ import print_function
import sys, re,codecs
import transcoder
transcoder.transcoder_set_dir('transcoder')

def transcode(x,tranin,tranout):
 y = transcoder.transcoder_processString(x,tranin,tranout)
 return y

def transcode_lines(lines,tranin,tranout):
 newlines = []
 for iline,line in enumerate(lines):
  line = line.replace('sh','s2')
  newline = transcode(line,tranin,tranout)
  newlines.append(newline)
 return newlines


def read(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"lines read from",filein)
 return lines

def write(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in lines:
   f.write(line+'\n')
 print(len(lines),'written to',fileout)

if __name__=="__main__":
 tranin = sys.argv[1]
 tranout = sys.argv[2]
 filein = sys.argv[3] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[4] # 
 lines = read(filein)
 newlines = transcode_lines(lines,tranin,tranout)
 write(fileout,newlines)
 
