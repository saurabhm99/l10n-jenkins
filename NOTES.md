# L10n practical notes

## Merge (`feature/de-locale` into `feature/sau19-locale-qa`)

Conflict was only in `locales/en.json`.

- **Kept both** `nav.support` (main) and `nav.help` (DE). They are different keys; dropping one loses a nav item.
- **Picked one** `battery.status`: main's `Battery: {percent}%`. Keeping both sides would duplicate the key and break JSON.
- **Footer:** kept `© {year} Lenovo Group Limited. All rights reserved.` from main (legal entity). Discarded DE's `Copyright {year} Lenovo...`. I would ask legal if they prefer the word "Copyright" vs the © symbol.

Did not blindly keep both sides of each hunk.

## Validator

`tools/check_locales.py` reports missing keys, extra keys, placeholder mismatches, and empty values. After the merge it also flags `de.json` (`{prozent}`, missing keys). I did not "fix" fr/ja/de — the task is to detect them. First Jenkins build is red on purpose.

## Jenkins

Ran Jenkins in Docker with `file:///repo`. Used `sudo docker` because `/var/run/docker.sock` is `root:root`. Installed python3 in the container. Build #1 failed as expected.

Failed vs unstable: missing / empty / placeholder → **failed** (ship-stoppers). Extra keys could be unstable later if we split severities.

## `count_keys.sh`

`grep -c '":'` is not JSON-aware. It can mis-count. Better: `json.load` and `len(...)`.

## AI

Used Cursor. I had to: add `import re` (copied a sketch that was not a full script); convert `run_checks.sh` from CRLF to LF (`pipefail: invalid option name`); forward `"$@"` so `--locales-dir` reaches Python.

## Unfinished

(If you skipped a screenshot or the Jenkins linter, say so here.)