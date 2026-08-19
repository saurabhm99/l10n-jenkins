#!/usr/bin/env python3
"""Compare every locales/*.json file against en.json."""

import argparse
import json
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"\{[^{}]+\}")


def placeholders(text):
    return set(PLACEHOLDER.findall(text or ""))


def load_json(path):
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f), None
    except (OSError, json.JSONDecodeError) as err:
        return None, err


def check_locale(en, loc):
    en_keys = set(en)
    loc_keys = set(loc)
    missing = sorted(en_keys - loc_keys)
    extra = sorted(loc_keys - en_keys)
    empty = []
    mismatch = []

    for key in sorted(en_keys & loc_keys):
        value = loc[key]
        if value == "":
            empty.append(key)
        en_ph = placeholders(en[key])
        loc_ph = placeholders(value)
        if en_ph != loc_ph:
            mismatch.append((key, sorted(en_ph), sorted(loc_ph)))

    return missing, extra, empty, mismatch


def main():
    parser = argparse.ArgumentParser(description="Validate locale files against en.json")
    parser.add_argument(
        "--locales-dir",
        default="locales",
        help="Directory that contains en.json and other locale files",
    )
    args = parser.parse_args()

    locales_dir = Path(args.locales_dir)
    en_path = locales_dir / "en.json"
    en, err = load_json(en_path)
    if err:
        print(f"Cannot read {en_path}: {err}")
        return 1

    issues = 0
    locale_files = sorted(
        p for p in locales_dir.glob("*.json") if p.name != "en.json"
    )

    if not locale_files:
        print(f"No locale files found in {locales_dir}")
        return 1

    for path in locale_files:
        print(f"== {path.name} ==")
        loc, err = load_json(path)
        if err:
            print(f"  ERROR: cannot parse JSON ({err})")
            issues += 1
            print()
            continue

        missing, extra, empty, mismatch = check_locale(en, loc)
        count = len(missing) + len(extra) + len(empty) + len(mismatch)
        issues += count

        if count == 0:
            print("  OK")
        else:
            for key in missing:
                print(f"  MISSING      {key}")
            for key in extra:
                print(f"  EXTRA        {key}")
            for key in empty:
                print(f"  EMPTY        {key}")
            for key, en_ph, loc_ph in mismatch:
                print(f"  PLACEHOLDER  {key}: en {en_ph} vs loc {loc_ph}")
        print()

    print(f"Total issues: {issues}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())