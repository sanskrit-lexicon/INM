#-*- coding:utf-8 -*-
"""replace_div_L.py
 
"""
from __future__ import print_function
import sys, re,codecs

def adjust_lines_div(lines,option):
 newlines = []
 metaflag = False  # is previous line a meta-line
 inentry = False
 for iline,line in enumerate(lines):
  if line.startswith('<L>'): 
   newline = line
   inentry = True
   metaflag = True
  elif line.startswith('<LEND>'):
   inentry = False
   newline = line
  elif metaflag:
   # prev line is meta-line. Don't adjust current line
   metaflag = False
   newline = line
  elif not inentry:
   newline = line
  elif line.startswith('<div n="P">'):
   newline = line
  elif line.startswith('<div n="HI">'):
   newline = line
  elif line.startswith('[Page'):
   newline = line
  elif line.startswith('<sup>'):  # 25 Why?
   newline = line
  elif line.startswith('<F>'):  # 25 Why?
   newline = line
  elif line.startswith(('<C n="4"/>(4) Jahnu','<C n="6"/>(6) Ṛcīka')):  # 2 Why?
   newline = line
   #print('chk',line)
  else:
   # In an entry
   # not a meta line
   # previous line not a meta line
   # line doesn't start with '<div n="P">'
   # line doesn't start with '[Page'
   # NOW: insert or remove <div n="lb"> depending on option
   dlb = '<div n="lb">'
   if option == 'remove':
    # remove
    assert line.startswith(dlb)
    newline = line[len(dlb):]
   else:
    # insert
    newline = dlb+line
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
 option = sys.argv[1] # no yes
 assert option in ['remove','insert']
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[3] # 
 lines = read(filein)
 newlines = adjust_lines_div(lines,option)
 write(fileout,newlines)
 
