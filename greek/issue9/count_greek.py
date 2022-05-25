#-*- coding:utf-8 -*-
"""count_greek.py
 
"""
from __future__ import print_function
import sys, re,codecs

from parseheadline import parseheadline

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  # linenum1,2 are int
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  self.greek_texts = []
  self.greek_langs = []
  
def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs

def read(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"lines read from",filein)
 return lines

def write(fileout,entries):
 ngtot = 0
 nltot = 0
 nge = 0
 nle = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for entry in entries:
   ng = len(entry.greek_texts)
   nl = len(entry.greek_langs)
   meta = re.sub('<k2>.*$','',entry.metaline)
   out = '%s : ng = %s, nl = %s' % (meta,ng,nl)
   ngtot = ngtot + ng
   nltot = nltot + nl
   if ng != 0:
    nge = nge + 1
   if nl != 0:
    nle = nle + 1
   f.write(out+'\n')
 print(len(entries),'written to',fileout)
 print('%s entries have a total of %s Greek strings' %(nge,ngtot))
 print('%s entries have a total of %s empty Greek lang ' %(nle,nltot))

g1 = '\u0370'
g2 = '\u03ff'
def generate_greek_strings(x):
 """ 
  Assume x a (unicode) string. In utf-8 encoding?
 """
 gcs = []  # sequence of greek characters
 ingreek = False
 for c in x:
  if g1 <= c <= g2:
   if not ingreek:
    # starting a new string
    gcs = [c]
    ingreek = True
   else:
    # continuing a greek string
    gcs.append(c)
  else:
   # c not greek
   if ingreek:
    s = ''.join(gcs)
    yield(s)
    ingreek = False
    gcs = []
   else:
    pass # c not greek, and previous character not greek.
 if ingreek:
  # last string
  s = ''.join(gcs)
  yield(s)

def mark_entries(entries):
 for entry in entries:
  for line in entry.datalines:
   a = re.findall(r'<lang n="greek"></lang>',line)
   entry.greek_langs = entry.greek_langs + a
   #b = re.findall(r'[\u0370-\u03ff]+',line) # Greek unicode block
   b = list(generate_greek_strings(line))
   entry.greek_texts = entry.greek_texts + b

if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[2] # 
 #lines = read(filein)
 entries = init_entries(filein)
 mark_entries(entries)
 
 write(fileout,entries)
 
