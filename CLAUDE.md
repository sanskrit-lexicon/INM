# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**INM** is the corrections and research repository for the Cologne digitization of Sörensen's *Index to the Names in the Mahābhārata* (1904). The canonical source lives in `csl-orig/v02/inm/inm.txt`.

## Architecture

| Directory | Purpose |
|---|---|
| `concordance/` | Concordance data linking INM entries to Mahabharata text references |
| `greek/` | Greek loanword and citation research |
| `spacedmarkup/` | Research on spaced markup conventions in INM entries |

Issues and corrections are tracked via the [GitHub issue tracker](https://github.com/sanskrit-lexicon/INM/issues).

### Issue correction pattern

Standard workflow for any issue:
1. Copy current `inm.txt` to a local `temp_inm_0.txt` (not tracked by git)
2. Apply corrections incrementally as `temp_inm_1.txt`, `temp_inm_2.txt`, etc.
3. Rebuild XML with `generate_dict.sh` and validate with `xmlchk_xampp.sh`
4. Commit the corrected file to `csl-orig`, then sync to Cologne
5. Commit issue documentation here

## Common Commands

### Apply line-level corrections
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh inm ../../INMScan/2020
sh xmlchk_xampp.sh inm
```

## Dependencies

- **Python 3**
- **inm.txt** — in `$BASE/cologne/csl-orig/v02/inm/inm.txt`

## Data format

INM is a names index; entries pair a proper name with Mahābhārata references.

| Tag | Role | Example |
|---|---|---|
| `<L>NNNN` | Entry begin, with `<pc>` print page ref | `<L>1<pc>001-1` |
| `<k1>`, `<k2>` | Primary / secondary headword | `<k1>abala<k2>abala` |
| `<LEND>` | Entry end | |
| `{@…@}` | Proper name / reference number (bold) | `{@Abala@}` |
| `{%…%}` | Italic (e.g. Sanskrit phrases) | `{%yajñamuṣo devāḥ%}` |
| `§ NNN` | Sörensen section reference | `§ 492` |

Annotated example — the first entry of `inm.txt`:
```
<L>1<pc>001-1<k1>abala<k2>abala     # entry 1; headword "abala"
{@Abala@}.¦ § 492 (Āṅgirasa): III, {@220@}, 14166 (...)   # bold name ¦ section + MBh references
<LEND>                              # entry end
```

## GitHub Issue Conventions

This repository uses the Cologne dictionary-repo issue taxonomy. Every issue has exactly one **type**, one **severity**, and one **milestone**:

- **Type** (9): link-target, link-splitting, markup, text-correction, content-enhancement, encoding, scan-quality, bug, question
- **Severity** (3): minor, medium, hard
- **Milestone** (4): Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

See the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md) for label definitions and the type→milestone mapping.
