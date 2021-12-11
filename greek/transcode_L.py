#-*- coding:utf-8 -*-
"""transcode_L.py
 
"""
from __future__ import print_function
import sys, re,codecs
import transcoder
transcoder.transcoder_set_dir('transcoder')

def transcode(x,tranin,tranout):
 y = transcoder.transcoder_processString(x,tranin,tranout)
 return y

def transcode_lines(lines,tranin,tranout):
 def f(m):
  a = m.group(1)
  b = m.group(2)
  c = m.group(3)
  b1 = transcode(b,tranin,tranout)
  return a+b1+c
 newlines = []
 for iline,line in enumerate(lines):
  if not line.startswith('<L>'):
   newlines.append(line)
   continue
  # for metaline, transcode the <k1> and <k2> items
  if '<h>' in line:
   newline = re.sub(r'(<k1>)(.*?)(<)',f,line)
   newline = re.sub(r'(<k2>)(.*?)(<)',f,newline)
  else:
   newline = re.sub(r'(<k1>)([^<]*)(<)',f,line)
   newline = re.sub(r'(<k2>)(.*?)($)',f,newline)
  if False: #dbg
   if '<h>' in line:
    print(line)
    print(newline)
    exit(1)
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
 
