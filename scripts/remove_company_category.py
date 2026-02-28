#!/usr/bin/env python3
"""Remove entries with category == 'Company' from data.json.

Creates a backup `data.json.company.bak` before writing the filtered file.
Prints counts of removed and remaining items.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / 'data.json'


def main():
    if not DATA_FILE.exists():
        print('data.json not found')
        return
    data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
    total = len(data)
    keep = [it for it in data if (it.get('category') or '').strip() != 'Company']
    removed = total - len(keep)

    bak = DATA_FILE.with_name('data.json.company.bak')
    bak.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    DATA_FILE.write_text(json.dumps(keep, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f'Total items: {total}')
    print(f'Removed items with category "Company": {removed}')
    print(f'Remaining items: {len(keep)}')
    print(f'Backup written to: {bak}')


if __name__ == '__main__':
    main()
