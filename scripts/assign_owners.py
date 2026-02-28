#!/usr/bin/env python3
"""Infer and assign `owner` fields in data.json using URL domains and name tokens.

Creates backups and report files:
- data.json.owners.backup (original)
- data.owners.assigned.json (full dataset after assignment)
- data.owners.report.json (summary and list of assignments)

Run from repo root: python scripts/assign_owners.py
"""
import json
from urllib.parse import urlparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / 'data.json'

owner_domain_map = {
    'amazon.com': 'Amazon',
    'aws.amazon.com': 'Amazon',
    'google.com': 'Google',
    'cloud.google.com': 'Google',
    'microsoft.com': 'Microsoft',
    'azure.microsoft.com': 'Microsoft',
    'meta.com': 'Meta',
    'facebook.com': 'Meta',
    'deepmind.com': 'Google',
    'openai.com': 'OpenAI',
    'huggingface.co': 'Hugging Face',
    'alibabacloud.com': 'Alibaba',
    'alibaba.com': 'Alibaba',
    'tencent.com': 'Tencent',
    'baidu.com': 'Baidu',
    'oracle.com': 'Oracle',
    'ibm.com': 'IBM',
    'salesforce.com': 'Salesforce',
    'stripe.com': 'Stripe',
    'paypal.com': 'PayPal',
    'adobe.com': 'Adobe',
    'sap.com': 'SAP',
    'zoho.com': 'Zoho',
    'linkedin.com': 'Microsoft',
    'apple.com': 'Apple',
    'yahoo.com': 'Yahoo',
    'oraclecloud.com': 'Oracle'
}

owner_token_map = {
    'amazon': 'Amazon', 'aws': 'Amazon',
    'google': 'Google', 'gcp': 'Google',
    'microsoft': 'Microsoft', 'azure': 'Microsoft',
    'meta': 'Meta', 'facebook': 'Meta',
    'deepmind': 'Google',
    'openai': 'OpenAI', 'hugging': 'Hugging Face',
    'alibaba': 'Alibaba', 'tencent': 'Tencent', 'baidu': 'Baidu',
    'oracle': 'Oracle', 'ibm': 'IBM', 'salesforce': 'Salesforce',
    'stripe': 'Stripe', 'paypal': 'PayPal', 'adobe': 'Adobe',
    'sap': 'SAP', 'zoho': 'Zoho', 'linkedin': 'Microsoft', 'apple': 'Apple'
}

special_names = {
    'pytorch': 'Meta',
    'tensorflow': 'Google',
    'mlflow': 'Databricks',
    'databricks': 'Databricks'
}


def host_of(url):
    try:
        p = urlparse(url)
        return (p.netloc or '').lower()
    except Exception:
        return ''


def infer_owner(item):
    # return (owner_name, method)
    # check URL domain mapping first
    url = item.get('url') or ''
    host = host_of(url)
    if host:
        for dom, owner in owner_domain_map.items():
            if host.endswith(dom):
                # avoid assigning owner equal to item name
                if owner.lower() != (item.get('name') or '').lower():
                    return owner, 'domain'
    # special name matches
    name = (item.get('name') or '').lower()
    for key, owner in special_names.items():
        if key in name:
            return owner, 'special'
    # token matches in name
    for token, owner in owner_token_map.items():
        if token in name and owner.lower() != name:
            return owner, 'name'
    return None, None


def main():
    data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
    backup = ROOT / 'data.json.owners.backup'
    backup.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    assigned = []
    report = {'total': len(data), 'assigned': 0, 'by_method': {}, 'samples': []}
    for i, item in enumerate(data):
        owner, method = infer_owner(item)
        if owner:
            item['owner'] = owner
            assigned.append({'name': item.get('name'), 'url': item.get('url'), 'owner': owner, 'method': method})
            report['assigned'] += 1
            report['by_method'][method] = report['by_method'].get(method, 0) + 1
            if len(report['samples']) < 200:
                report['samples'].append({'index': i, 'name': item.get('name'), 'owner': owner, 'method': method})

    out_assigned = ROOT / 'data.owners.assigned.json'
    out_report = ROOT / 'data.owners.report.json'
    out_assigned.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    out_report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')

    # Overwrite canonical data.json with assigned owners (safe because backup exists)
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f"Processed {report['total']} items. Assigned owners: {report['assigned']}")
    print(f"Report written to {out_report}\nAssigned dataset written to {out_assigned}\nBackup saved to {backup}")


if __name__ == '__main__':
    main()
