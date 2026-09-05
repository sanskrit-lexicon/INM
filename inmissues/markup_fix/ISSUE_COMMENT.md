_Created: 22-05-2026 · Last updated: 05-09-2026_

### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `inm.txt`.

I ran the same two-job recipe over `csl-orig/v02/inm/inm.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `inmissues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — please review the findings listed below.

## Markup fixer + audit for `inm.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>X</ab> Y</ab>` | `<ab>X Y</ab>` |
| `<sup> word </sup>` | `<sup>word</sup>` |
| `<is> word </is>` | `<is>word</is>` |
| `<F> word </F>` | `<F>word</F>` |

Whitespace trimming applies to all 4 paired tag(s) in `inm.txt`: `<sup>`, `<is>`, `<F>`, `<lang>`. The original file is never modified — output goes to `inm_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format). 1 line(s) changed.

### Closing-tag inventory in current `inm.txt`

| Tag | Count |
|---|---:|
| `</sup>` | 6 |
| `</942)>` | ? |
| `</is>` | 338 |
| `</F>` | 25 |
| `</lang>` | 1 |

### What it found in current `inm.txt`

- 1 whitespace trim applied: trailing space in one `<is>` tag.
- 0 adjacent `</ab> <ab>` — no `<ab>` tag in inm.txt.
- 0 `<ab n="…">` attributes.
- 92 `{{old → new || …}}` correction records present.

### Usage

```
cd inmissues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/inm/inm.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `inm_fixed.txt`, `markup_fix_changes.txt`, `markup_audit.txt`.

### Summary

No <ab> or <ls>; <sup> and <is> are the main paired tags.

### Severity

`minor`

_Dr. Mārcis Gasūns_
