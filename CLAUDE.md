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
