#-*- coding:utf-8 -*-
"""compare_greek.py
 
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
  self.greek_textsab = []
  self.greek_gx = []  # only for ab
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
 nout = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for entry in entries:
   gts = entry.greek_texts
   gtabs = entry.greek_textsab
   gx = entry.greek_gx
   if gts == gtabs:
    if gx != []:
     print('gx anomaly',entry.metaline,gx)
    continue
   
   ngts = len(gts)
   ngtabs = len(gtabs)
   if ngts == ngtabs:
    flag = '=='
   else:
    flag = '!='
   meta = re.sub('<k2>.*$','',entry.metaline)
   outarr = []
   outarr.append('---------------------------------------')
   outarr.append('%s : %s %s %s' % (meta,ngts,flag,ngtabs))
   outarr.append('%3s: %s' %('csl',' '.join(gts)))
   outarr.append('%3s: %s' %('ab',' '.join(gtabs)))
   outarr.append('ab gx text: %s' % gx)
   nout = nout + 1
   for out in outarr:
    f.write(out+'\n')
 print(nout,'differences written to',fileout)


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

def get_gx(lines):
 a = []
 for line in lines:
  b = re.findall(r'<gx>[^<]*</gx>',line)
  a = a + b
 return a

def mark_entries(entries1,entries2):
 for ientry,entry1 in enumerate(entries1):
  entry2 = entries2[ientry]
  for line in entry1.datalines:
   b = list(generate_greek_strings(line))
   entry1.greek_texts = entry1.greek_texts + b
  for line in entry2.datalines:
   b = list(generate_greek_strings(line))
   entry1.greek_textsab = entry1.greek_textsab  + b
  entry1.greek_gx = get_gx(entry2.datalines)
  
 diffs = [e for e in entries1 if e.greek_texts != e.greek_textsab]
 print('mark_entries. # diffs = ',len(diffs))
 
def compare_entries_prep(entries1_init,entries2,Ldict2):
 entries1 = [e for e in entries1_init if 
             e.metad['L'] not in ['210','405','2492','2493','3397','3266']]
 n1 = len(entries1)
 n2 = len(entries2)
 print('compare entries: n1=%s, n2=%s' %(n1,n2))
 for i1,e1 in enumerate(entries1):
  L1 = e1.metad['L']
  if i1 < n2:
   e2 = entries2[i1]
   L2 = e2.metad['L']
   if L1 != L2:
    j = i1+1
    print('No match at entry number %s' % j)
    print('csl: %s' % e1.metaline)
    print(' ab: %s' % e2.metaline)
    exit(1)
  else:
   print("error2",L1)
   exit(1)

def drop_ab_Ldecimal(entries):
 a = []
 ndrop = 0
 for e in entries:
  L = e.metad['L']
  if '.' in L:
   ndrop = ndrop + 1
  else:
   a.append(e)
 print(ndrop,"AB entries with decimal in L")
 return a

def drop_csl_entries(entries):
 drops = ['210','405','2492','2493','3397','3266']
 entries1 = [e for e in entries if
             e.metad['L'] not in drops]
 print('drop %s csl entries' % len(drops))
 return entries1

def compare_entries(entries1,entries2):
 n1 = len(entries1)
 n2 = len(entries2)
 print('compare entries: n1=%s, n2=%s' %(n1,n2))
 if n1 != n2:
  print('compare_entries error 1')
  exit(1)
 for i1,e1 in enumerate(entries1):
  e2 = entries2[i1]
  assert e1.metad['L'] == e2.metad['L']
  #if e1.metaline != e2.metaline:
  # print('%s != %s' %(e1.metaline,e2.metaline))
  
if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 filein1 = sys.argv[2] # ab version
 fileout = sys.argv[3] # 
 #lines = read(filein)
 entries = init_entries(filein)
 entries1 = drop_csl_entries(entries)
 Ldict_csl = Entry.Ldict
 Entry.Ldict = {}
 entriesab = init_entries(filein1)
 Ldict_ab = Entry.Ldict
 entriesab1 = drop_ab_Ldecimal(entriesab)
 # compare_entries_prep(entries,entriesab1,Ldict_ab)
 compare_entries(entries1,entriesab1)
 
 mark_entries(entries1,entriesab1)
 
 write(fileout,entries)
 
