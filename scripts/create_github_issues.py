#!/usr/bin/env python3
"""Create GitHub issues from data/issues.csv using GitHub CLI (gh)."""
from pathlib import Path
import csv,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]; CSV_PATH=ROOT/'data'/'issues.csv'
def run(args,capture=False): return subprocess.run(args,check=True,text=True,capture_output=capture)
def main():
    try: existing_text=run(['gh','issue','list','--state','all','--limit','500','--json','title','--jq','.[].title'],True).stdout
    except FileNotFoundError:
        print('GitHub CLI gh is not installed. Install it and run gh auth login first.',file=sys.stderr); raise SystemExit(2)
    except subprocess.CalledProcessError:
        print('Could not read issues. Check repository context and run gh auth login.',file=sys.stderr); raise SystemExit(2)
    existing={x.strip() for x in existing_text.splitlines() if x.strip()}
    with CSV_PATH.open(encoding='utf-8-sig',newline='') as f:
        for row in csv.DictReader(f):
            if row['title'] in existing: print('SKIP (already exists): '+row['title']); continue
            args=['gh','issue','create','--title',row['title'],'--body',row['body']]
            for label in [x.strip() for x in row['labels'].split(',') if x.strip()]: args.extend(['--label',label])
            run(args); print('CREATED: '+row['title'])
if __name__=='__main__': main()
