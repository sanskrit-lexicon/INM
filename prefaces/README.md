# Sörensen INM — front matter (Vorspann)

Faithful OCR transcription, plus a Russian translation, of the **front matter** of:

> **An Index to the Names in the Mahābhārata**, with short explanations and a concordance to the Bombay and Calcutta editions and P. C. Roy's translation, by the late **S. Sörensen**, Ph.D. *Published under the auspices of the Government of India.* First published London: Williams & Norgate, 1904; reprinted by **Motilal Banarsidass**, Delhi, 1963.

Source scans come from the Cologne Digital Sanskrit Lexicon (CDSL) csldoc build:
[inmpref.html](https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/inmpref.html). The dictionary data itself lives in [csl-orig `v02/inm/inm.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/inm/inm.txt); this folder covers only the prefatory pages, which are not part of `inm.txt`.

**Source language: English.** The 9 pages comprise the title page and publisher imprint of the 1963 Motilal Banarsidass reprint, the reprint *Foreword* (R. P. Naik, Ministry of Education), Sörensen's original *Preface* (pp. iii–vi, 1902), the *List of Abbreviations*, and the *Postscriptum* (Dines Andersen & Elof Olesen, January 1925) describing how the work was completed and published after Sörensen's death.

### Signatures and dates found
- **Preface** — signed *“S. Sörensen. Copenhagen. February, 1902.”*
- **Postscriptum** — written by the editors who completed the work, *Dines Andersen* and *Elof Olesen*, dated *Copenhagen, January 1925*; it records the author's dates (\*23 November 1849 — †8 December 1902) and that only pages 1–32 had been set in type before his death.
- **Foreword** (reprint) — *R. P. Naik, Ministry of Education, New Delhi.*

The tiny digitizer running-header and footer stamps added to every CDSL scan are **omitted** from the transcription (they are not part of the original).

## File conventions

| Suffix | Contents |
|---|---|
| `inmprefNN.md` | Faithful English transcription of page NN (the source). |
| `inmprefNN.ru.md` | Russian translation of page NN. |

There are **no** `inmprefNN.en.md` files: the source is already English, so the base `inmprefNN.md` *is* the English edition.

## Consolidated editions

| Edition | File | Built by |
|---|---|---|
| English (source) | [inmpref_all.en.md](inmpref_all.en.md) | [build_combined.py](build_combined.py) |
| Russian | [inmpref_all.ru.md](inmpref_all.ru.md) | [build_combined.py](build_combined.py) |

Regenerate with `DICT=inm python build_combined.py` (reads each page's YAML; no hard-coded page list).

## Contents

| Page | Section | Vol. | English (source) | Russian |
|---|---|---|---|---|
| 01 | Title page | 1 | [inmpref01.md](inmpref01.md) | [ru](inmpref01.ru.md) |
| 02 | Publisher imprint (1963 reprint) | 1 | [inmpref02.md](inmpref02.md) | [ru](inmpref02.ru.md) |
| 03 | Foreword (R. P. Naik) | 1 | [inmpref03.md](inmpref03.md) | [ru](inmpref03.ru.md) |
| 04 | Preface (p. iii) | 1 | [inmpref04.md](inmpref04.md) | [ru](inmpref04.ru.md) |
| 05 | Preface (p. iv) | 1 | [inmpref05.md](inmpref05.md) | [ru](inmpref05.ru.md) |
| 06 | Preface (p. v) | 1 | [inmpref06.md](inmpref06.md) | [ru](inmpref06.ru.md) |
| 07 | Preface (p. vi) — signed | 1 | [inmpref07.md](inmpref07.md) | [ru](inmpref07.ru.md) |
| 08 | List of Abbreviations | 1 | [inmpref08.md](inmpref08.md) | [ru](inmpref08.ru.md) |
| 09 | Postscriptum (Andersen & Olesen, 1925) | 1 | [inmpref09.md](inmpref09.md) | [ru](inmpref09.ru.md) |

Scans are kept under [scans/](scans/) (filenames `inm_Page_NNN_Image_0001.png`). The csldoc toctree order is authoritative; note the underlying scan pages run 808–817 with 812 absent and 808 (Postscriptum) ordered last as page 09.

## Transcription notes
- English transcribed in the original orthography. Sörensen's transliteration system is preserved verbatim: palatal sibilant *ç* (= ś), *sh* (= ṣ), vocalic *ṛ*, and the bold/clarendon convention for Bombay-edition chapter numbers.
- The *List of Abbreviations* (3 print columns) is rendered as two Markdown tables — abbreviations and symbols — in print reading order (column 1, then 2, then 3).
- Sanskrit/Devanāgarī kept verbatim with full diacritics; the title-page and imprint Devanāgarī lines are preserved.
- Russian translation: personal and place names in Cyrillic (Sanskrit proper names kept in their Latin transliteration in **bold**, as in the source, with a Cyrillic gloss in the abbreviations table); bibliographic work-titles and all Sanskrit kept in their original script.
