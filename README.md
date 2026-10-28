# bulk-renamer

Rename every file in a folder by pattern. Dry-run by default, so nothing
changes until you pass `--apply`. No dependencies, Python 3 only.

## What it does

- Renames files with a pattern: `{name}` (original name without extension),
  `{n}` (running number), `{ext}` (original extension).
- `--prefix` / `--suffix` add fixed text; `--replace OLD:NEW` substitutes text.
- `--ext` limits the run to one extension, e.g. `.jpg`.
- Skips a rename if the target name already exists instead of overwriting.

## How to run

```bash
# Preview only (safe default, changes nothing)
python rename.py ./photos "{n}_{name}{ext}"

# Actually rename
python rename.py ./photos "{n}_{name}{ext}" --apply

# Add a prefix to every file
python rename.py ./photos --prefix "trip-" --apply
```

## Example output

```
$ python rename.py ./photos "{n}_{name}{ext}"
alpha.txt -> 01_alpha.txt
beta.txt -> 02_beta.txt
gamma.jpg -> 03_gamma.jpg

Preview only: 3 file(s) would be renamed. Re-run with --apply to rename.
```

## Options

| Flag | Meaning |
| --- | --- |
| `directory` | Folder containing the files |
| `pattern` | Rename pattern (default: `{name}{ext}`) |
| `--start N` | First number for `{n}` (default: 1) |
| `--width N` | Zero-padding width for `{n}` (default: 2) |
| `--ext .jpg` | Only rename files with this extension |
| `--prefix TEXT` | Text prepended to every new name |
| `--suffix TEXT` | Text appended before the extension |
| `--replace OLD:NEW` | Substitute text inside names |
| `--apply` | Actually rename (without it, preview only) |

Exit codes: 0 on success or "nothing to rename", 2 on a bad directory
or a malformed `--replace` value.
