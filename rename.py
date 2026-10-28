#!/usr/bin/env python3
"""bulk-renamer: rename files in a folder by pattern, dry-run by default.

Pattern placeholders:
  {name}  original filename without extension
  {n}     running number, starting at --start (zero-padded to --width)
  {ext}   original extension (including the dot)

Nothing is renamed unless --apply is passed. Without --apply the script
prints "old -> new" pairs and exits 0. Use --ext to limit to one
extension (e.g. --ext .jpg), --prefix / --suffix to add fixed text, and
--replace OLD:NEW to substitute text inside the original name.

Examples:
  python rename.py ./photos "{n}_{name}{ext}"            # preview only
  python rename.py ./photos "{n}_{name}{ext}" --apply    # actually rename
  python rename.py ./photos --prefix "trip-" --apply     # prefix every file
"""

import argparse
import os
import sys


def build_name(pattern, name, number, width):
    base, ext = os.path.splitext(name)
    return pattern.format(name=base, n=str(number).zfill(width), ext=ext)


def plan(directory, pattern, start, width, ext_filter, prefix, suffix, replace):
    files = sorted(
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
        and (ext_filter is None or os.path.splitext(f)[1] == ext_filter)
    )
    pairs = []
    for i, old in enumerate(files, start=start):
        new_base = build_name(pattern, old, i, width)
        stem, ext = os.path.splitext(new_base)
        if replace:
            old_text, new_text = replace
            stem = stem.replace(old_text, new_text)
        new = prefix + stem + suffix + ext
        if new != old:
            pairs.append((old, new))
    return pairs


def main(argv=None):
    parser = argparse.ArgumentParser(description="Rename files by pattern (dry-run by default).")
    parser.add_argument("directory", help="Folder containing the files to rename")
    parser.add_argument("pattern", nargs="?", default="{name}{ext}",
                        help='Rename pattern, e.g. "{n}_{name}{ext}" (default: {name}{ext})')
    parser.add_argument("--start", type=int, default=1, help="First number for {n} (default: 1)")
    parser.add_argument("--width", type=int, default=2, help="Zero-padding width for {n} (default: 2)")
    parser.add_argument("--ext", default=None, help="Only rename files with this extension, e.g. .jpg")
    parser.add_argument("--prefix", default="", help="Text to prepend to every new name")
    parser.add_argument("--suffix", default="", help="Text to append before the extension")
    parser.add_argument("--replace", default=None,
                        help="Substitute text inside names, as OLD:NEW")
    parser.add_argument("--apply", action="store_true",
                        help="Actually rename (without this flag, only preview)")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.directory):
        print(f"error: not a directory: {args.directory}", file=sys.stderr)
        return 2
    if args.replace is not None and ":" not in args.replace:
        print("error: --replace needs OLD:NEW format", file=sys.stderr)
        return 2

    replace = tuple(args.replace.split(":", 1)) if args.replace else None
    pairs = plan(args.directory, args.pattern, args.start, args.width,
                 args.ext, args.prefix, args.suffix, replace)
    if not pairs:
        print("Nothing to rename.")
        return 0

    for old, new in pairs:
        print(f"{old} -> {new}")
    if not args.apply:
        print(f"\nPreview only: {len(pairs)} file(s) would be renamed. Re-run with --apply to rename.")
        return 0

    for old, new in pairs:
        src, dst = os.path.join(args.directory, old), os.path.join(args.directory, new)
        if os.path.exists(dst):
            print(f"skipped (target exists): {old} -> {new}", file=sys.stderr)
            continue
        os.rename(src, dst)
    print(f"Renamed {len(pairs)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
