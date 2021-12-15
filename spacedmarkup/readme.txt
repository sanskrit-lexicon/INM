
python transcode_iast.py as roman temp_inm.spaced.word.markings.in.utf8.file.txt wide_iast.txt

temp_inm.txt from csl-orig/v02/inm/inm.txt at commit
 36ca643c51eb6ad89a5fce8c872f1508128b03da
temp_inm_slp1_L2_02.txt from ../greek/ at commit
 783d282d803c8194e1b49ab1a8da8d42828a8d4e

Similarly temp_inm_ac.txt, temp_inm_concord.txt,
temp_inm_abbr.txt, temp_inm_preface.txt, temp_inm_postscript.txt

Use wide_iast.txt to add markup <is>X</is>.

Add markup to temp_inm.txt, temp_concord.txt and temp_ac.txt based on wide_iast.txt.
  Note also used server file
  scans/INMScan/2013/orig/inm_orig_utf8.txt, which has {|X|} markup consistent with
  wide_iast.txt.
 
  For cases where the wide text appears over two lines, care must be taken.
  Example:
  PROBLEM:
  Śveta against Bhīṣma), 1970.—({%b%}) <is>2nd
  day of the battle</is>:
  SOLUTION:
  Śveta against Bhīṣma), 1970.—({%b%}) <is>2nd</is>
  <is>day of the battle</is>:

The reason this is a problem has to do with the way line-breaks are handled in
the construction of inm.xml by make_xml.py.
 There is inserted a '<dib n="lb">' tag, and then the div is closed
 XML: from problem
  <div n="lb">Śveta against Bhīṣma), 1970.—({%b%}) <is>2nd</div>
  <div n="lb">day of the battle</is>:</div>
 With this coding, the 'is' element *straddles* the div, which is
 not valid xml.
 XML: from solution
  <div n="lb">Śveta against Bhīṣma), 1970.—({%b%}) <is>2nd</is></div>
  <div n="lb"><is>day of the battle</is>:</div>
 Here, the two 'is' elements are safely WITHIN the enclosing 'div' elements.

NOTE:  It is likely possible to alter the way line breaks are introduced in
 the xml, in such a way that 'PROBLEM' solution is actually not a problem.
 Namely, by using an EMPTY XML ELEMENT for the line break.
 Have not fully explored this possibility.
 
Also removed <> line-break markup in the other files (inm_concord.txt, etc.)
from csl-orig/v02/inm/

---------------------------------------------------------------------
installation of changes
The files to be copied back to csl-orig:

cp temp_inm.txt /c/xampp/htdocs/cologne/csl-orig/v02/inm/inm.txt
cp temp_inm_abbr.txt /c/xampp/htdocs/cologne/csl-orig/v02/inm/inm_abbr.txt
cp temp_inm_ac.txt /c/xampp/htdocs/cologne/csl-orig/v02/inm/inm_ac.txt
cp temp_inm_concord.txt /c/xampp/htdocs/cologne/csl-orig/v02/inm/inm_concord.txt
cp temp_inm_preface.txt /c/xampp/htdocs/cologne/csl-orig/v02/inm/inm_preface.txt

Check validity of inm.txt
In csl-pywork/v02:
sh generate_dict.sh inm  ../../inm
sh xmlchk_xampp.sh inm
Then commit and push in csl-orig/v02/inm/
And do similar on cologne server:
 git pull [for csl-orig]
 update in csl-pywork/v02
 
