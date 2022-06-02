Revisit greek markup in INM.
 Hypothesis all but 1 of the <lang n="greek">X</lang> instances in
 inm.txt are either
 - part of a star name, OR
 - a label.
start with latest inm.txt in csl-orig/v02, at commit
 771d75bea1e266dedf95bb53457c0679a238417d

cp /c/xampp/htdocs/cologne/csl-orig/v02/inm/inm.txt temp_inm_0.txt
  NOTE: This is NOT the same as ../temp_inm_7.txt

Based on comment at
  https://github.com/sanskrit-lexicon/INM/issues/4#issuecomment-991433302
the Andhrabharati version we start with is from greek directory under
name inm_slp1_L2_02.txt, we use temporary copy
cp ../inm_slp1_L2_02.txt temp_inm_ab_0.txt

There is some question about <gx>X</gx> temporary markup in this AB version
  There are 49 such <gx> instances.
  
First, make an inventory of greek text fragments in the two versions.
python count_greek.py temp_inm_ab_0.txt temp_count_ab.txt
2993 entries have a total of 10794 Greek strings

python count_greek.py temp_inm_0.txt temp_count.txt
2947 entries have a total of 10713 Greek strings

python freq_greek.py csl temp_inm_0.txt freq_greek_csl.txt
12647 entries found
135 different greek strings
python freq_greek.py ab temp_inm_ab_0.txt freq_greek_ab.txt
13485 entries found
135 different greek strings
*****************************************************************************
Investigate differences in number of greek strings in csl and ab versions.
temp_inm_1.txt is modified from temp_inm_0.txt by
 removing <lang n="greek"> and </lang>, except for the one in k1=aSvaka.
 
python compare_greek.py temp_inm_1.txt temp_inm_ab_0.txt compare_greek.txt

-------------------------------------------
python compare_greek1.py temp_inm_1.txt temp_inm_ab_0.txt compare_greek1.txt

