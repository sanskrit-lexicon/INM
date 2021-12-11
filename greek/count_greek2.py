#-*- coding:utf-8 -*-
"""count_greek2.py
 
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
  self.greek_primary = []   # primary match
  self.greek_secondary = []   # secondary match
  self.L = L
  
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
 nge = 0   # entries with ng != 0
 nge1 = 0  # entries with ng1 != 0
 ng1tot = 0 # total of ng1 over all entries
 ngtot = 0  # total of ng over all entries
 with codecs.open(fileout,"w","utf-8") as f:
  for entry in entries:
   ng = len(entry.greek_primary)
   ng1 = len(entry.greek_secondary)
   ngtot = ngtot + ng
   ng1tot = ng1tot + ng1
   if ng1 != 0:
    nge1 = nge1 + 1
   
   if ng == 0:
    continue
   nge = nge + 1
   meta = re.sub('<k2>.*$','',entry.metaline)
   out = '%s : ng = %s' % (meta,ng)
   f.write(out+'\n')
 print(len(entries),'found')
 print(nge,'entries written to',fileout)
 print('These have %s primary Greek strings' % ngtot)
 print('There are also %s secondary Greek strings' %ng1tot)
 

def mark_entries_A(entries):
 for entry in entries:
  for line in entry.datalines:
   a = re.findall(r'<lang n="greek">[\u0370-\u03ff]+</lang>',line)
   entry.greek_primary = entry.greek_primary + a
   b = re.findall(r'<lang n="greek1">[\u0370-\u03ff]+</lang>',line)
   entry.greek_secondary = entry.greek_secondary + b

def mark_entries_B(entries):
 for entry in entries:
  if not re.search(r'^[0-9]+$',entry.L):
   # the non-integer L entries are revisions for B 
   continue
  for line in entry.datalines:
   a = re.findall(r'.[\u0370-\u03ff]+',line)
   a1 = [x[1:] for x in a if x[0] != '>']
   entry.greek_primary = entry.greek_primary + a1
   a2 = [x[1:] for x in a if x[0] == '>']
   entry.greek_secondary = entry.greek_secondary + a2


if __name__=="__main__":
 option = sys.argv[1]  # A == temp_inm_06, B = inm_slp1_L2_02
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[3] # 
 entries = init_entries(filein)
 assert option in ['A','B']
 if option == 'A':
  mark_entries_A(entries)
 else:
  mark_entries_B(entries)
 write(fileout,entries)
 
