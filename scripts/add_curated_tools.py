#!/usr/bin/env python3
"""Append curated important tools if missing in data.json"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / 'data.json'


def normalize(s: str) -> str:
    return re.sub(r"[^0-9a-zA-Z]","", (s or "").lower())


CURATED = [
    {"name": "Microsoft Excel", "url": "https://www.microsoft.com/en/microsoft-365/excel", "category": "Tool", "sector": "Productivity", "country": "Microsoft", "description": "Spreadsheet software"},
    {"name": "Microsoft Power BI", "url": "https://powerbi.microsoft.com/", "category": "Tool", "sector": "Business Intelligence", "country": "Microsoft", "description": "Business analytics service"},
    {"name": "Tableau", "url": "https://www.tableau.com/", "category": "Tool", "sector": "Business Intelligence", "country": "USA", "description": "Interactive data visualization"},
    {"name": "Qlik", "url": "https://www.qlik.com/", "category": "Tool", "sector": "Business Intelligence", "country": "Sweden", "description": "Analytics and data integration"},
    {"name": "Looker", "url": "https://cloud.google.com/looker", "category": "Tool", "sector": "Business Intelligence", "country": "USA", "description": "Data platform by Google Cloud"},
    {"name": "MicroStrategy", "url": "https://www.microstrategy.com/", "category": "Tool", "sector": "Business Intelligence", "country": "USA", "description": "Enterprise analytics platform"},
    {"name": "SAP BusinessObjects", "url": "https://www.sap.com/products/businessobjects.html", "category": "Tool", "sector": "Business Intelligence", "country": "Germany", "description": "Business intelligence suite"},
    {"name": "Sisense", "url": "https://www.sisense.com/", "category": "Tool", "sector": "Business Intelligence", "country": "USA", "description": "Analytics and BI platform"},
    {"name": "Metabase", "url": "https://www.metabase.com/", "category": "Tool", "sector": "Business Intelligence", "country": "Worldwide", "description": "Open-source business intelligence"},
    {"name": "Grafana", "url": "https://grafana.com/", "category": "Tool", "sector": "Monitoring", "country": "Worldwide", "description": "Observability and metrics dashboard"},
    {"name": "Kibana", "url": "https://www.elastic.co/kibana", "category": "Tool", "sector": "Monitoring", "country": "Worldwide", "description": "Visualization for Elasticsearch"},
    {"name": "Redash", "url": "https://redash.io/", "category": "Tool", "sector": "Business Intelligence", "country": "Worldwide", "description": "Query and visualization tool"},
]


def load_data():
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding='utf-8'))


def save_data(items):
    DATA_FILE.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding='utf-8')


def main():
    items = load_data()
    existing = {normalize(it.get('name','')): it for it in items}
    added = 0
    for ex in CURATED:
        key = normalize(ex['name'])
        if key in existing:
            # if exists but points to wikipedia, prefer curated url
            cur = existing[key]
            if 'wikipedia.org' in (cur.get('url') or '') and 'wikipedia.org' not in ex['url']:
                cur['url'] = ex['url']
                cur['category'] = ex.get('category', cur.get('category',''))
                cur['description'] = cur.get('description') or ex.get('description','')
        else:
            items.append(ex)
            existing[key] = ex
            added += 1
            print(f"Appended curated: {ex['name']}")

    if added:
        save_data(items)
    print(f"Done. Added {added} curated items.")


if __name__ == '__main__':
    main()
