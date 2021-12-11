#-*- coding:utf-8 -*-
"""greek_changeb.py
 
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
  self.L = L
  self.greek_texts = []
  self.greek_langs = []
  self.greek_texts1 = []
  self.greek_texts2 = []
  self.changes = []  # change transactions for this entry
  
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

class Change(object):
 def __init__(self,lnum,old,new):
  self.lnum = lnum
  self.old = old
  self.new = new

def mark_changes(entry,entry1):
 oldlines = entry.datalines
 oldtext = '\n'.join(oldlines)
 greek_texts2 = entry1.greek_texts2
 xgreek = [0]
 def fsub(m):
  ngreek = xgreek[0]
  greek = greek_texts2[ngreek]
  ans = '<lang n="greek">%s</lang>' % greek
  ngreek = ngreek + 1
  xgreek[0] = ngreek
  return ans
  
 newtext = re.sub(r'<lang n="greek"></lang>',fsub,oldtext)
 ngreek = xgreek[0]
 assert ngreek == len(entry.greek_langs)
 assert ngreek == len(greek_texts2)
 newlines = newtext.split('\n')
 nchange = 0
 for iline,line in enumerate(oldlines):
  newline = newlines[iline]
  if newline == line:
   continue
  nchange = nchange + 1
  # generate change from line to newline
  lnum = entry.linenum1 + iline + 1
  changerec = Change(lnum,line,newline)
  entry.changes.append(changerec)

def read(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"lines read from",filein)
 return lines

def write(fileout,entries):
 outrecs = []  # list of entry change text lines
 for entry in entries:
  ne = len(entry.changes) # number of lines changed in this entry
  if ne == 0:
   continue
  outarr = [] # change text for this entry
  nlang = len(entry.greek_langs)
  outarr.append('; ---------------------------------------------')
  shortmeta = re.sub(r'<k2>.*$','',entry.metaline)
  outarr.append('; %s : %s greek text in %s lines' % (shortmeta,nlang,ne))
  for ichange,change in enumerate(entry.changes):
   lnum = change.lnum
   old = change.old
   new = change.new
   outarr.append('%s old %s' %(lnum,old))
   outarr.append('%s new %s' %(lnum,new))
   outarr.append(';')
  outrecs.append(outarr)
 # now, write outrecs
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print('change records written to',fileout)

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

def generate_greek_strings1(line):
 ans = re.findall(r'[\u0370-\u03ff]+',line)
 return ans

def generate_greek_strings2(line):
 a = re.findall(r'.[\u0370-\u03ff]+',line)
 ans = [x[1:] for x in a if x[0]!= '>']
 return ans

def mark_entries(entries):
 for entry in entries:
  for line in entry.datalines:
   a = re.findall(r'<lang n="greek"></lang>',line)
   entry.greek_langs = entry.greek_langs + a
   #b = re.findall(r'[\u0370-\u03ff]+',line) # Greek unicode block
   b = list(generate_greek_strings(line))
   entry.greek_texts = entry.greek_texts + b
   c = generate_greek_strings2(line)
   entry.greek_texts2 = entry.greek_texts2 + c
   if False:
    if b != c:
     print(line)
     print('b = ',b)
     print('c = ',c)
     exit(1)
    

if __name__=="__main__":
 filein = sys.argv[1] #  cologne digitization of inm
 filein1 = sys.argv[2] #  Andhrabharati digitization of inm
 fileout = sys.argv[3] # changes for filein
 #lines = read(filein)
 entries = init_entries(filein)
 Ldict = Entry.Ldict
 Entry.Ldict = {}
 entries1 = init_entries(filein1)
 Ldict1 = Entry.Ldict
 mark_entries(entries)
 mark_entries(entries1)
 nprob1 = 0  # nlangs!=0 and L not in Ldict1
 nprob2 = 0  # nlangs != ntexts1
 n = 0 # nlangs != 0
 
 for entry in entries:
  L = entry.L
  nlangs = len(entry.greek_langs)
  if nlangs == 0:
   continue
  n = n + 1
  if L not in Ldict1:
   nprob1 = nprob1 + 1
   continue
  entry1 = Ldict1[L]
  ntexts2 = len(entry1.greek_texts2)
  if nlangs != ntexts2:
   nprob2 = nprob2 + 1
   if True:
    print(L,nlangs,ntexts2)
   continue
  mark_changes(entry,entry1)
 print(n,'entries in %s with nlangs != 0' % filein)
 print('nprob1=',nprob1)
 print('nprob2=',nprob2)  # 103
 
 write(fileout,entries)
 
