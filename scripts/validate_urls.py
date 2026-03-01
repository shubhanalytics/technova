#!/usr/bin/env python3
"""
Comprehensive URL validation script for data.json
Checks for:
1. Stock exchange URLs (NYSE, NASDAQ, etc.)
2. Suspicious descriptions that may indicate copy-paste errors
3. URLs that don't match company names
4. Empty or missing URLs
"""

import json
import re
from collections import Counter
from urllib.parse import urlparse

# Load data
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total entries: {len(data)}")
print("=" * 80)

# Check 1: Stock exchange and financial URLs
print("\n1. STOCK EXCHANGE / FINANCIAL URLs (should be company websites):")
stock_patterns = [
    r'nyse\.com',
    r'nasdaq\.com',
    r'yahoo\.com/quote',
    r'finance\.yahoo',
    r'bloomberg\.com/quote',
    r'marketwatch\.com/investing',
    r'google\.com/finance',
    r'seekingalpha\.com/symbol',
    r'tradingview\.com/symbols',
    r'/quote/[A-Z]+:',
    r'/market-activity/stocks/',
]

stock_issues = []
for item in data:
    url = item.get('url', '')
    for pattern in stock_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            stock_issues.append(item)
            print(f"  - {item['name']}: {url}")
            break

if not stock_issues:
    print("  None found - OK!")

# Check 2: Duplicate descriptions (sign of copy-paste errors)
print("\n2. SUSPICIOUS DUPLICATE DESCRIPTIONS:")
descriptions = [item.get('description', '') for item in data if item.get('description')]
desc_counts = Counter(descriptions)
duplicate_descs = {desc: count for desc, count in desc_counts.items() if count > 3 and len(desc) > 20}

if duplicate_descs:
    for desc, count in sorted(duplicate_descs.items(), key=lambda x: -x[1])[:10]:
        print(f"\n  Description used {count} times: \"{desc}\"")
        items_with_desc = [item['name'] for item in data if item.get('description') == desc][:5]
        print(f"    Examples: {', '.join(items_with_desc)}")
else:
    print("  No suspicious duplicates found - OK!")

# Check 3: Empty or missing URLs
print("\n3. EMPTY OR MISSING URLs:")
empty_urls = [item for item in data if not item.get('url') or item.get('url', '').strip() == '']
if empty_urls:
    for item in empty_urls[:20]:
        print(f"  - {item['name']}")
    if len(empty_urls) > 20:
        print(f"  ... and {len(empty_urls) - 20} more")
else:
    print("  None found - OK!")

# Check 4: URLs with unusual patterns
print("\n4. POTENTIALLY SUSPICIOUS URL PATTERNS:")
suspicious = []
for item in data:
    url = item.get('url', '')
    name = item.get('name', '').lower()
    
    # Check for obvious mismatches (e.g., GoDaddy URL shouldn't be nyse.com)
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    # Skip if URL contains part of the name (likely correct)
    name_parts = re.findall(r'[a-z0-9]+', name)
    
    # Flag if domain looks like it's a third-party financial/investor site
    investor_patterns = [
        'investor', '/ir/', 'shareholders', 'sec.gov', 
        'edgar', 'annualreports', 'stockwatch'
    ]
    
    for pat in investor_patterns:
        if pat in url.lower() and not any(part in domain for part in name_parts if len(part) > 3):
            suspicious.append((item['name'], url))
            break

if suspicious:
    for name, url in suspicious[:20]:
        print(f"  - {name}: {url}")
else:
    print("  No suspicious patterns found - OK!")

# Check 5: HTTP URLs (potential security concern)
print("\n5. INSECURE HTTP URLs (should be HTTPS):")
http_urls = [item for item in data if item.get('url', '').startswith('http://')]
print(f"  Found {len(http_urls)} HTTP URLs (consider updating to HTTPS)")
if http_urls and len(http_urls) <= 20:
    for item in http_urls:
        print(f"  - {item['name']}: {item['url']}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY:")
print(f"  - Stock exchange URLs: {len(stock_issues)}")
print(f"  - Suspicious duplicate descriptions: {len(duplicate_descs)}")
print(f"  - Empty URLs: {len(empty_urls)}")
print(f"  - HTTP (insecure) URLs: {len(http_urls)}")
print("=" * 80)
