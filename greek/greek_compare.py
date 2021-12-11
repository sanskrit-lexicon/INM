#-*- coding:utf-8 -*-
"""greek_compare.py
 
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
  # specialize parameters
  self.greek_primary = []   # primary match
  self.greek_secondary = []   # secondary match
  self.L = L
  self.entry1 = None
  
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

def extract1_helper(line):
 ans = []
 for m in re.finditer(r'(.)([\u0370-\u03ff]+)',line):
  x = m.group(1)
  if x == '>':
   continue
  greek = m.group(2)
  i1 = m.start(2)
  i2 = m.end(2)
  j1 = max(0,i1 - 15)
  j2 = min(len(line),i2 + 15)
  context = line[j1:j2]
  ans.append((greek,context))
 return ans

def extract1(entry):
 datalines = entry.datalines
 #lnum = entry.linenum1
 outarr = []
 outarr.append('')
 icount = 0
 for iline,line in enumerate(datalines):
  a = extract1_helper(line)
  if len(a) == 0:
   continue
  for x in a:
   greek,context = x
   icount = icount + 1
   out = '%s %s' %(icount,context)   
   outarr.append(out)
 outarr[0] = '; Source B (%s)' % icount
 return outarr

def extract0_helper(line):
 ans = []
 for m in re.finditer(r'(<lang n="greek">)(.*?)(</lang>)',line):
  greek = m.group(2)
  i1 = m.start(1) # opening <
  i2 = m.end(3) # closing >
  j1 = max(0,i1 - 15)
  j2 = min(len(line),i2 + 15)
  g = '%s' % greek
  context = line[j1:i1] + g + line[i2:j2]
  ans.append((greek,context))
 return ans

def extract0(entry):
 datalines = entry.datalines
 alltext = ' '.join(datalines)
 #textadj = re.sub(r'<div n=.*?>','',alltext,re.DOTALL)
 textadj = re.sub(r'<div n=.*?>','',alltext)
 textadj = re.sub(r'({@[0-9]+)(<lang n="greek">[^<]*?</lang>),(@})',
                  r'\1\3\2,',textadj)
 textadj = textadj.replace(',@}','@},')
 textadj = textadj.replace(',%}','%},')
 textadj = textadj.replace(';%}','%};')
 textadj = re.sub(r'{%\(([^%]*)\)%}',r'({%\1%})',textadj)
 degree = '°'
 laghava = '॰'
 textadj = textadj.replace(degree,laghava)
 outarr = []
 outarr.append('')
 icount = 0
 a = extract0_helper(textadj)
 #if len(a) == 0:
 # return outarr
 for x in a:
  greek,context = x
  icount = icount + 1
  out = '%s %s' %(icount,context)   
  outarr.append(out)
 outarr[0] = '; Source A (%s)' % icount
 return outarr

def write(fileout,entries):
 outrecs = []  # list of entry change text lines
 nsame = 0
 ndiff = 0
 for entry in entries:
  entry1 = entry.entry1
  if entry1 == None:
   continue
  outarr1 = extract1(entry1)
  outarr0 = extract0(entry)
  outarr = []
  outarr.append('; ---------------------------------------------')
  shortmeta = re.sub(r'<k2>.*$','',entry.metaline)
  outarr.append('; %s' % shortmeta)
  n1 = len(outarr1)
  n0 = len(outarr0)
  n = max(n0,n1)
  assert n0 == n1
  for i in range(n):
   if i < n0:
    t0 = outarr0[i]
   else:
    t0 = ' '
   if i < n1:
    t1 = outarr1[i]
   else:
    t1 = ' '
   x0 = t0.ljust(30)
   x1 = t1.ljust(30)
   if i == 0:
    middle = ' ........ '
   elif x0 == x1:
    middle = ' ..SAME.. '
    nsame = nsame + 1
   else:
    middle = ' ..DIFF.. '
    ndiff = ndiff + 1
   x = x0 + middle + x1
   outarr.append(x)
  outrecs.append(outarr)
 # now, write outrecs
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print(len(outrecs),' records written to',fileout)
 print(nsame,"contexts are the same (..SAME..)")
 print(ndiff,"contexts are different (..DIFF..)")
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
 filein = sys.argv[1] #  cologne digitization of inm
 filein1 = sys.argv[2] #  Andhrabharati digitization of inm
 fileout = sys.argv[3] # mismatch text
 entries = init_entries(filein)
 Ldict = Entry.Ldict
 Entry.Ldict = {}
 entries1 = init_entries(filein1)
 Ldict1 = Entry.Ldict
 mark_entries_A(entries)
 mark_entries_B(entries1)
 nprob1 = 0  # nlangs!=0 and L not in Ldict1
 nprob2 = 0  # nlangs != ntexts1
 n = 0 # nlangs != 0
 for entry in entries:
  ng = len(entry.greek_primary)
  if ng == 0:
   continue
  L = entry.L
  entry1 = Ldict1[L]
  entry.entry1 = entry1
 write(fileout,entries)
 
