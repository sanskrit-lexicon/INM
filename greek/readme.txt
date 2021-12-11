versions from Andhrabharati.
See links in https://github.com/sanskrit-lexicon/csl-devanagari/issues/34
temp_inm-devanagari-main_L0.txt
temp_inm-devanagari-main_L1.txt
temp_inm-devanagari_consolidated.Andhrabharati.txt
 for uniformity of naming, rename the consolidated version to
 temp_inm-devanagari-main_L2.txt

==========================================================================
change to unix line endings:
python /c/xampp/htdocs/cologne/unixify.py temp_inm-devanagari-main_L0.txt
python /c/xampp/htdocs/cologne/unixify.py temp_inm-devanagari-main_L1.txt
python /c/xampp/htdocs/cologne/unixify.py temp_inm-devanagari-main_L2.txt
==========================================================================
PREPARE for transcoding of L1,L2,L3  to slp1
==========================================================================
The invertibility constraint requires some minor changes in L0, L1, and L2

Change one Headword spelling in L0: L=7794  ॐकार -> ओंकार
  in L0:  new file is temp_inm-devanagari-main_L0_00.txt
  change_L0_00.txt (1)

Change <h2> to <h>2 in L1 (L=8426.1)
  new L1 file is temp_inm-devanagari-main_L1_00.txt
  change_L1_00.txt (1)

Changes in L2
    L=7504, 7505, 7506, 7507, 7713, 7714
    See: https://github.com/sanskrit-lexicon/INM/issues/3
  change_L2_00.txt (6)

NOTE: The versions L0_00 etc can be computed directly using the change files:
python updateByLine.py temp_inm-devanagari-main_L0.txt change_L0_00.txt temp_inm-devanagari-main_L0_00.txt
python updateByLine.py temp_inm-devanagari-main_L1.txt change_L1_00.txt temp_inm-devanagari-main_L1_00.txt
python updateByLine.py temp_inm-devanagari-main_L2.txt change_L2_00.txt temp_inm-devanagari-main_L2_00.txt


==========================================================================
Transcode to slp1
==========================================================================

Then transcode L1, L2, L3 to slp1 and confirm invertibility.
Devanagari occurs in L0, L1, L2 only in the metalines

python transcode_L.py deva slp1 temp_inm-devanagari-main_L0_00.txt temp_inm_slp1_L0.txt
python transcode_L.py deva slp1 temp_inm-devanagari-main_L1_00.txt temp_inm_slp1_L1.txt
python transcode_L.py deva slp1 temp_inm-devanagari-main_L2_00.txt temp_inm_slp1_L2.txt

==========================================================================
check invertibility of transcoding
==========================================================================
# L0
python transcode_L.py slp1 deva temp_inm_slp1_L0.txt temp.txt 
diff temp_inm-devanagari-main_L0_00.txt temp.txt
# no difference.

# L1
python transcode_L.py slp1 deva temp_inm_slp1_L1.txt temp.txt
diff temp_inm-devanagari-main_L1_00.txt temp.txt
# no difference.

# L2
python transcode_L.py slp1 deva temp_inm_slp1_L2.txt temp.txt
diff temp_inm-devanagari-main_L2_00.txt temp.txt
# no difference.


==========================================================================
Cologne digitization start 
==========================================================================
temp_inm_00.txt  This is a copy of inm.txt in csl-orig.
It can be retrieved with git show:
cd to inm directory in csl-orig: csl-orig/v02/inm
git show b31e3c7db8:v02/inm/inm.txt > temp_inm_00.txt

==========================================================================
compare temp_inm_00.txt with temp_inm_slp1_L0.txt
==========================================================================
At this point, it is unclear what changes have been introduced into L0.
The number of lines are almost the same:
wc -l temp_inm_00.txt temp_inm_slp1_L0.txt
  138297 temp_inm_00.txt
  138290 temp_inm_slp1_L0.txt

However, a simple 'diff' shows a huge number of differences:
diff temp_inm_00.txt temp_inm_slp1_L0.txt | wc -l
188934

A visual comparison shows one major cause of the difference:  
L0 removed <div n="lb">.
(The other two versions, L1 and L2) also removed this.)
A program, divlb.py, was developed to construct a version of 
These occur (in temp_inm_00) only on lines that
a) not metalines
b) not begin with <div n="P"> or with <div n="HI">
c) not on 1st line after metalines (lines with '¦')
d) not a page break line: [Page...]
e) not a line that startswith '<sup>'  (25 lines)
f) not a line that startswith '<F>'  (25)
g) not a line that startswith '<C ' (2)
option arg means:
 remove: remove <div n="lb">
 insert: insert <div n="lb">

# Construct a (temporary) version of L0 with these 'div' phrases inserted:
python divlb.py insert temp_inm_slp1_L0.txt temp_inm_slp1_L0_01.txt
# and compare to temp_inm_00:

diff temp_inm_00.txt temp_inm_slp1_L0_01.txt | wc -l
 37 line (about 9 differences)

Investigate the differences (i.e., look at tempdiff.txt):
diff temp_inm_00.txt temp_inm_slp1_L0_01.txt > tempdiff.txt

temp_inm_01.txt
Two lines in temp_inm_00 should start with <div...>, but
instead start with `<lang n="greek">` --
  changed by inserting '<div n="lb">' Saved as temp_inm_01.txt
change_01.txt contains the changes.

The rest are due to corrections in temp_inm_00 for sup,
which were made after the L0 file constructed.
  (see commit 6af7b3c54d73e1d0c0f0fca4d834abf9406f9821 for csl-orig:
  https://github.com/sanskrit-lexicon/csl-orig/commit/6af7b3c54d73e1d0c0f0fca4d834abf9406f9821)

temp_inm_slp1_L0_02.txt: 
change_L0_02.txt has these changes.
  Manual changes in temp_inm_slp1_L0_02.txt
python updateByLine.py temp_inm_slp1_L0_01.txt change_L0_02.txt temp_inm_slp1_L0_02.txt

# now, do the comparison again
diff temp_inm_01.txt temp_inm_slp1_L0_02.txt > tempdiff.txt
 tempdiff.txt has 9 lines.  The csl version (temp_inm_01.txt) has
 7 extra lines, which are not important.
$ cat tempdiff.txt
1,3d0
< ;
< ; ENTRIES
< ;
138294,138297d138290
< [Page788]
< blank
< [Page789]
< blank


#shows only 3 extra lines at top, and 4 at bottom, in temp_inm_01.txt.
# Create temp_inm_02.txt with the 'sed' Unix utility:
# copy lines 4-138293 from temp_inm_01.txt  to temp_inm_02.txt
sed -n '4,138293 p' temp_inm_01.txt > temp_inm_02.txt
# Now temp_inm_slp1_L0_02.txt and temp_inm_02.txt are the same
diff temp_inm_slp1_L0_02.txt temp_inm_02.txt
# No difference

This completes the comparison with L0.  Since L1 and L2 are believed
to be further revisions of L0,  we will make use of change_L0_02.txt
And temp_inm_02.txt is the starting point.
==========================================================================
Partial comparison of L0 and L1
Some use was made of L1 in headword corrections of temp_inm_02 (see next section)
My current work makes very little use of L1.
Here are notes that might be useful if L1 is further examined.
==========================================================================

wc -l temp_inm_slp1_L0.txt temp_inm_slp1_L1.txt
  138290 temp_inm_slp1_L0.txt
  138527 temp_inm_slp1_L1.txt
#So, a few more lines
#But the diff is very large:
diff temp_inm_slp1_L0.txt temp_inm_slp1_L1.txt | wc -l
#  143351

Examination of the diff indicates several kinds of changes - not known
whether this list is comprehensive, but probably not:
1. Punctuation in the first line of entry (before broken bar) is often eliminated in L1:
 '{@Abala.@}¦ § 492' -> '{@Abala@}¦ § 492 '
2. Commas at end of italic is moved outside markup:
 '{%yajñamuṣo devāḥ,%}' -> '{%yajñamuṣo devāḥ%},'
2a. Similarly with Semicolons.
3. Many entries are 'split' into two or more entries.
   All entries have L values without a decimal point in L0, but 540 have L0 WITH '.' in L1:
grep -E '<L>[0-9]+[.]' temp_inm_slp1_L0.txt | wc -l  # 0
grep -E '<L>[0-9]+[.]' temp_inm_slp1_L1.txt | wc -l  # 540.
First example:
L0:
<L>930<pc>099-1<k1>aTarvaSiras<k2>aTarvaSiras<h>1
{@Atharvaśiras@}<sup>1</sup>,¦ an Upaniṣad (v. BR.): I, 2882; III,
17066; XIII, 4298. Do.<sup>2</sup> = Mahāpuruṣa (Ma° Pu°st°).
<LEND>

L1:
<L>930<pc>099-1<k1>aTarvaSiras<k2>aTarvaSiras<h>1
{@Atharvaśiras@}<sup>1</sup>¦ an Upaniṣad (v. BR.): I, 2882; III,
17066; XIII, 4298.
<LEND>

<L>930.1<pc>099-1<k1>???<k2>???<h>2
Do.<sup>2</sup> = Mahāpuruṣa (Ma° Pu°st°).
<>[Note. This is split from the earlier entry]
<LEND>

4. Only a few Greek text items are filled in in L1.


==========================================================================
temp_inm_03a.txt : headword corrections based on L1
change_03a.txt
beginning comparison of temp_inm_02.txt to temp_inm_slp1_L1.txt

---------------------------------------------------------------------
the L-number is always an integer in temp_inm_02.txt
# of lines:
 temp_inm_02.txt 138290
 temp_inm_slp1_L1.txt 138527

grep -E '<L>' temp_inm_02.txt | wc -l
 12655
grep -E '<L>[0-9]+<' temp_inm_02.txt | wc -l
 12655  (so )
 
---------------------------------------------------------------------
but decimal point appears in some L1 L values
grep -E '<L>' temp_inm_slp1_L1.txt | wc -l
 13200  # total number of L values
grep -E '<L>[0-9]+<' temp_inm_slp1_L1.txt | wc -l
 12660  Why 5 more than temp_inm_02.txt?
grep -E '<L>[0-9]+[.][0-9]+<' temp_inm_slp1_L1.txt | wc -l
  540  # an example is given in previous section
  (+ 12660 540) = 13200

==========================================================================
Resolve L-value headword differences between
  temp_inm_02.txt and temp_inm_slp1_L1.txt
Revised versions:
temp_inm_03a.txt   change_03a.txt (4)
temp_inm_slp1_L1_01.txt  change_L1_01.txt (5)
==========================================================================


grep -E '<L>[0-9]+<' temp_inm_02.txt > temp_inm_L_02.txt
grep -E '<L>[0-9]+<' temp_inm_slp1_L1.txt > temp_L_int_L1.txt
diff temp_L_inm_02.txt temp_L_int_L1.txt | wc -l
 # 18  Compare the diff and generate the changes.
 
Verify that the INT headwords are the same in two revised files:
grep -E '<L>[0-9]+<' temp_inm_03a.txt > temp_inm_L_03a.txt
grep -E '<L>[0-9]+<' temp_inm_slp1_L1_01.txt > temp_L_int_L1_01.txt
diff temp_L_inm_03a.txt temp_L_int_L1_01.txt | wc -l
 # 0 : no difference.

There are a few more non-standard headwords in temp_inm_slp1_L1_01.txt
grep -E '<L>[0-9]+[.][0-9]+<' temp_inm_slp1_L1_01.txt | wc -l
 545  These are 'non-standard' headwords.
-------------------------------

Only a few greek words are entered  in inm_slp1_L1_01.txt
10778 matches in 9509 lines for "<lang n="greek"" in buffer: temp_inm_03a.txt
8120 matches in 7368 lines for "[0-9]<lang n="greek"" in buffer: temp_inm_03.txt

10766 matches in 9498 lines for "<lang n="greek"></lang>" in buffer: inm_slp1_L1_01.txt
So, are only a few Greek text values filled in in L1?

python count_greek.py inm_slp1_L1_01.txt temp_count_greek_L1_01.txt
4 entries have a total of 15 Greek strings
2966 entries have a total of 10766 empty Greek lang
This completes our work with L1 version of inm.

==========================================================================
Prepare to count entries of L2 with greek text.
Previous slp1 version of L2 is  temp_inm_slp1_L2.txt
and of Cologne version is temp_inm_03a.txt.
Make new versions of both,
 temp_inm_03b.txt   change_inm_03b.txt (237)
 temp_inm_slp1_L2_01.txt  change_L2_01.txt (26)
  
 The L2 changes are primarily revising L-values so there will be no duplicate L-values.
 There are a couple of other changes, two changes in headword spelling.

 For inm, there are numerous headword changes prompted by comparing to headwords of L2.
 After the revisions, the headwords of inm agree

changenotes_meta_diff.txt provides further documentation of changes made.
See below for where it arises.
THERE ARE SEVERAL PRINT CHANGES to inm noted, due to Andhrabharati.

 documents changes made to temp_inm_slp1_L2_01.txt  and to temp_inm_slp1_L2_01.txt
 based on the above comparison of (integral) meta lines.

 temp_inm_slp1_L2_01.txt has extra headwords, with [.] in cologne id.'

 grep -E '<L>[0-9]+<' temp_inm_slp1_L2_01.txt | wc -l
   12641
 grep -E '<L>[0-9]+[.]' temp_inm_slp1_L2_01.txt | wc -l
   845
 
 grep -E '<L>[0-9]+<' temp_inm_03b.txt | wc -l
   12647   6 'extra' (integer) headwords in csl after corrections
 grep -E '<L>[0-9]+[.]' temp_inm_03b.txt | wc -l
   0

Resolve the difference between 12642 and 12655 (13)
grep -E '<L>[0-9]+<' temp_inm_slp1_L2_01.txt > temp_meta_temp_inm_slp1_L2_01.txt
grep -E '<L>[0-9]+<' temp_inm_03b.txt > temp_meta_inm_03.txt

diff temp_meta_inm_03.txt temp_meta_temp_inm_slp1_L2_01.txt > temp_meta_diff.txt
changenotes_meta_diff.txt is an editing of temp_meta_diff.txt and
 documents changes made to temp_inm_slp1_L2_01.txt  and to temp_inm_slp1_L2_01.txt
 based on the above comparison of (integral) meta lines.
 Most of these are due to homonym differences, as L2 takes into account the addenda,
 and also adds many 'Do' entries (which sometimes also introduce homonyms on prior entry)
 
Compare metalines, but exclude differences in homonym
grep -E '<L>[0-9]+<' temp_inm_slp1_L2_01.txt > temp_meta_temp_inm_slp1_L2_01.txt
grep -E '<L>[0-9]+<' temp_inm_03b.txt > temp_meta_inm_03.txt

sed -E 's/<h>[12345]//g' temp_meta_temp_inm_slp1_L2_01.txt > temp_L2_01.txt
sed -E 's/<h>[12345]//g' temp_meta_inm_03.txt > temp_03.txt
diff temp_03.txt temp_L2_01.txt > temp_meta_diff_noh.txt


There are 6 additional headwords (with all digit L) in cologne version temp_inm_03b.txt.
These are replaced by 'deletion' comments in temp_inm_slp1_L2_01.txt.
Here are the 'extra' metalines.
<L>210<pc>016-2<k1>Adya<k2>Adya
<L>405<pc>030-1<k1>amaraRa<k2>amaraRa
<L>2492<pc>196-2<k1>SArNgacakragadApAni<k2>SArNgacakragadApAni
<L>2493<pc>196-2<k1>SArNgacakrAsipARi<k2>SArNgacakrAsipARi
<L>3266<pc>237-1<k1>devarAja<k2>devarAja
<L>3397<pc>241-2<k1>Dara<k2>Dara

==========================================================================
L2 file has all the Greek text !
==========================================================================
python count_greek.py temp_inm_slp1_L2_00.txt temp.txt

python count_greek.py temp_inm_slp1_L2_01.txt temp.txt
83788 lines read from temp_inm_slp1_L2_01.txt
13485 entries found
13485 written to temp.txt
2993 entries have a total of 10794 Greek strings   <<<< 
0 entries have a total of 0 empty Greek lang


python count_Greek.py temp_inm_03b.txt temp1.txt
138290 lines read from temp_inm_03b.txt
12655 entries found
12655 written to temp1.txt
1 entries have a total of 1 Greek strings
2962 entries have a total of 10778 empty Greek lang
 That one entry with Greek string is at L=57, line 3 

<L>57<pc>004-2<k1>aSlezA<k2>aSlezA
{@Aśleṣā@}¦ (No. 43; cf. No. 44), a nakṣatra (the ninth when
<div n="lb">beginning with Aśvinī; its star of junction is supposed to be
<div n="lb">ε Hydræ; v. Sū° Si°, p. 188). XIII, {@64,@} 3262 (C. has A°,

==========================================================================
First step of generation of greek text for cologne version based on
Andhrabharati's version.
==========================================================================

The two files are difficult to align.

Basic idea:  'L' code which has an entry in the csl version and in the L2 version,
 make a sequence s1,s2,...,sn of the <lang n="greek"></lang> instances in the csl entry and
 a sequence g1,g2,...,gm of the greek texts in the L2 entry.
 If n = m,  then replace si by <lang n="greek">gi</lang> in the csl entry (for i=1,...,n).
 if n != m, then do no changes in the csl entry -- investigate further.

First, estimate how many lang tag instances to do:
python count_greek1.py temp_inm_03b.txt temp.txt
2962 entries have a total of 10778 empty Greek lang

Try to generate Greek text changes according to the 'basic idea'
  for temp_inm_03b.txt using  temp_inm_slp1_L2_01.txt.
The file of changes is change_04.txt.

python greek_changea.py temp_inm_03b.txt temp_inm_slp1_L2_01.txt change_04.txt

python updateByLine.py temp_inm_03b.txt change_04.txt temp_inm_04.txt
  7744 change transactions from change_04.txt

==========================================================================
Finishing the Greek text task
==========================================================================
How much is left?
python count_greek1.py temp_inm_04.txt temp.txt
138290 lines read from temp_inm_04.txt
12647 entries found
12647 written to temp.txt
2860 entries have a total of 8664 Greek strings
103 entries have a total of 2115 empty Greek lang

What is left?
The remaining ones occur in those 103 entries where there is a mismatch between
(a) number of greek instances in the temp_inm_slp1_L2_01.txt entry
(b) number of empty lang tags in the temp_inm_03b.txt entry.

We must resolve these mismatches.
Make a new copy of the two digitizations:
temp_inm_05.txt is a copy of temp_inm_04.txt and
temp_inm_slp1_L2_02.txt is a copy of temp_inm_slp1_L2_01.txt.

Use a program that generates context for the mismatches for each of the 103 entries.
And make adjustments in whichever digitization is required.
This process is iterative.
One context generator is:
python greek_mismatch.py temp_inm_05.txt temp_inm_slp1_L2_02.txt temp_greek_mismatch.txt

The changes are mostly of a few types:
1) csl has represented a Greek letter as a Latin letter.  Correct csl.
   Aśvinī (star of junction Vega or {%a%} Lyræ'  {%a%} -> <lang n="greek"></lang>
2) csl has used one lang tag, where there should be two lang tags
   csl: the Pāṇḍavas), 4209; {@95@} (<lang n="greek"></lang>),
   L2:  'the Pāṇḍavas), 4209; {@95@}(δδ, εε)'
   csl chg: the Pāṇḍavas), 4209; {@95@} (<lang n="greek"></lang>, <lang n="greek"></lang>)
3) L2 has split the entry, and some greek text is in 2nd part, which doesn't have
   a matching L in csl version. Example is with L=1081, k1=bahu.
   Here, the csl text has 3 empty lang tags; L2 has only 1 in L=1081, the other two
   being in L=1081.1.
   In this case, we change the empty lang tags corresponding to L=1081.1 to
   non-empty lang tags such as '<lang n="greek1">γ</lang>'. Note, we chose to use
   a different attribute value "greek1" instead of "greek" so that these cases could
   later be identified.
4) L2 has modified the entry based on the Addendum/Correction sections, and there is
   Greek text in the modified material.
   In this case, we add a 'gx' markup in L2, such as '<gx>γ</gx>'.  And we modify
   the change program ignore such text in L2 when generating the sequence of greek texts.

The end result of all the adjustments are
a) revised temp_inm_05.txt and the 
   set of 111 changes in change_05.txt
b) revised temp_inm_slp1_L2_02.txt and the
   set of 53 changes in change_L2_02.txt

Now we generate changes to temp_inm_05.txt using the same alignment idea:

python greek_changeb.py temp_inm_05.txt temp_inm_slp1_L2_02.txt change_06.txt
 81 entries with changed lines.
and apply these to get the next version:
python updateByLine.py temp_inm_05.txt change_06.txt temp_inm_06.txt
  1681 change transactions from change_06.txt

We make a new version of the Greek count routine that knows about the "greek" and "<gx>"
tricks:
python count_greek2.py B temp_inm_slp1_L2_02.txt temp_count_greek2_L2_02.txt
2943 entries written to temp_count_greek2_L2_02.txt
These have 10702 primary Greek strings
There are also 49 secondary Greek strings

python count_greek2.py A temp_inm_06.txt temp_count_greek2_06.txt
2943 entries written to temp_count_greek2_06.txt
These have 10702 primary Greek strings
There are also 11 secondary Greek strings

Thus, we now have the same number (10702) of 'primary' Greek strings in both
digitizations.

We have filled in all the empty lang tags:
grep -E '<lang n="greek"></lang>' temp_inm_06.txt | wc -l
  0 # as expected
  

==========================================================================
A final comparison
==========================================================================
A final comparison prints context strings from all greek instances from both versions.
Let 'A' refer to temp_inm_0
This compares the context of all greek text in the two digitizations, as a
further support to accuracy of insertion of greek text from B into A.
Several adjustments to the A text are made corresponding to additional changes
present in L2, and the two context strings are evaluated as the SAME or DIFFerent.

python greek_compare.py temp_inm_06.txt temp_inm_slp1_L2_02.txt temp_greek_compare.txt
2943  records written to temp_greek_compare.txt
7665 contexts are the same (..SAME..)
3037 contexts are different (..DIFF..)

The reason for the large number of context differences is various additional
changes made in the B version that are considered in the comparison.
A random sampling of greek_compare.txt leads to
the conclusion that the Greek text from B has been properly inserted into A.
(A = temp_inm_06.txt, B = temp_inm_slp1_L2_02.txt)


NOTE: page 474 of pdf is poor quality

L2 uses Devanagari laghava (॰) instead of degree (°)  
==================================================================
temp_inm_07.txt
==================================================================
The attempted installation of temp_inm_06.txt uncovered a few
xml errors. These are corrected in temp_inm_07.txt.
Also, the 'greek1' attribute value is changed back to 'greek' (required by displays)
 change_07.txt (13 corrections)

==================================================================
Installation of temp_inm_07.txt
==================================================================
cp temp_inm_07.txt /c/xampp/htdocs/cologne/csl-orig/v02/inm/inm.txt
modify basicdisplay.php so 'inm' is in the list of dictionaries with Greek filled in.
This modifies basicdisplay.php  in
  csl-websanlexicon/v02/makotemplates/web/webtc AND
  csl-apidev/basicdisplay.php
  Ref: https://github.com/sanskrit-lexicon/INM/issues/4

temp_inm_07.txt is same as csl-orig/v02/inm/inm.txt at
 commit 9fc6ed820c53b3ae5e767f45fb4e66b110f229c1.


==================================================================
Some summaries of the different versions
==================================================================
Here are line counts of the versions of inm:

 wc -l temp_inm_??.txt
  138297 temp_inm_00.txt
  138297 temp_inm_01.txt  only 7 differences from 00: <div n="lb"> inserted in two lines
  
  138290 temp_inm_02.txt  delete 3 lines from beginning of 01, and 4 from end.
  138290 temp_inm_03a.txt change_03a.txt  (4)
  138290 temp_inm_03b.txt change_03b.txt (237)  Mainly headword corrections
  138290 temp_inm_04.txt  change_04.txt (7744)  some insertion of greek text, where aligned
  138290 temp_inm_05.txt  change_05.txt (111) preparation for alignment of the rest
  138290 temp_inm_06.txt  change_06.txt (1681) conclude insertion of greek text.
  138290 temp_inm_07.txt  change_07.txt (13) correction of 2 xml errors introduced.
                                           Also, greek1 -> greek. (11)
     Recall <lang n="greek1">X</lang> was introduced to facilitate comparison with L2;
     'greek1' should not be part of production version of inm.txt.
 wc -l inm_slp1_L2*.txt
   83788 temp_inm_slp1_L2.txt
   83788 temp_inm_slp1_L2_00.txt change_L2_00.txt (6)
   83788 temp_inm_slp1_L2_01.txt change_L2_01.txt (26)
   83788 temp_inm_slp1_L2_02.txt change_L2_02.txt (53)


==========================================================================
Save local copy of revised slp1 form of L2:
cp temp_inm_slp1_L2_02.txt inm_slp1_L2_02.txt
 Generate devanagari form for revised
python transcode_L.py slp1 deva inm_slp1_L2_02.txt temp_inm_deva_L2_02.txt

python transcode_L.py deva slp1 temp_inm_deva_L2_02.txt temp.txt
diff inm_slp1_L2_02.txt temp.txt
# no difference, as expected.

