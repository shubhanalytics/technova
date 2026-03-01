#!/usr/bin/env python3
"""
Comprehensive URL reachability checker for data.json.
Checks if all URLs are accessible and reports issues.
"""

import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import time
import sys

# Configuration
TIMEOUT = 10  # seconds
MAX_WORKERS = 20  # concurrent requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

def check_url(item):
    """Check if a URL is reachable and returns status info."""
    name = item.get('name', 'Unknown')
    url = item.get('url', '')
    category = item.get('category', '')
    
    if not url:
        return {
            'name': name,
            'url': url,
            'category': category,
            'status': 'NO_URL',
            'error': 'Empty URL',
            'final_url': None
        }
    
    # Skip certain URL patterns that are known to block automated requests
    skip_patterns = ['linkedin.com', 'facebook.com', 'twitter.com', 'x.com']
    if any(p in url.lower() for p in skip_patterns):
        return {
            'name': name,
            'url': url,
            'category': category,
            'status': 'SKIPPED',
            'error': 'Social media (blocks bots)',
            'final_url': url
        }
    
    try:
        # First try HEAD request (faster)
        response = requests.head(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        
        # If HEAD fails with 405 or similar, try GET
        if response.status_code >= 400:
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True, stream=True)
            response.close()
        
        final_url = response.url
        status_code = response.status_code
        
        # Check for significant redirects
        redirect_info = None
        if final_url != url:
            # Check if it's a meaningful redirect (not just http->https or www addition)
            orig_domain = urlparse(url).netloc.replace('www.', '')
            final_domain = urlparse(final_url).netloc.replace('www.', '')
            if orig_domain != final_domain:
                redirect_info = f"Redirects to different domain: {final_domain}"
        
        if status_code >= 400:
            return {
                'name': name,
                'url': url,
                'category': category,
                'status': f'HTTP_{status_code}',
                'error': f'HTTP {status_code}',
                'final_url': final_url
            }
        
        return {
            'name': name,
            'url': url,
            'category': category,
            'status': 'OK' if not redirect_info else 'REDIRECT',
            'error': redirect_info,
            'final_url': final_url
        }
        
    except requests.exceptions.SSLError as e:
        return {
            'name': name,
            'url': url,
            'category': category,
            'status': 'SSL_ERROR',
            'error': 'SSL certificate error',
            'final_url': None
        }
    except requests.exceptions.ConnectionError as e:
        return {
            'name': name,
            'url': url,
            'category': category,
            'status': 'CONNECTION_ERROR',
            'error': 'Connection failed (site may be down)',
            'final_url': None
        }
    except requests.exceptions.Timeout:
        return {
            'name': name,
            'url': url,
            'category': category,
            'status': 'TIMEOUT',
            'error': f'Request timed out after {TIMEOUT}s',
            'final_url': None
        }
    except requests.exceptions.TooManyRedirects:
        return {
            'name': name,
            'url': url,
            'category': category,
            'status': 'TOO_MANY_REDIRECTS',
            'error': 'Too many redirects',
            'final_url': None
        }
    except Exception as e:
        return {
            'name': name,
            'url': url,
            'category': category,
            'status': 'ERROR',
            'error': str(e)[:100],
            'final_url': None
        }

def main():
    print("Loading data.json...")
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total = len(data)
    print(f"Checking {total} URLs (this will take several minutes)...")
    print(f"Using {MAX_WORKERS} concurrent workers with {TIMEOUT}s timeout\n")
    
    results = {
        'ok': [],
        'redirect': [],
        'broken': [],
        'timeout': [],
        'ssl_error': [],
        'skipped': [],
        'other_error': []
    }
    
    checked = 0
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_item = {executor.submit(check_url, item): item for item in data}
        
        for future in as_completed(future_to_item):
            result = future.result()
            checked += 1
            
            status = result['status']
            if status == 'OK':
                results['ok'].append(result)
            elif status == 'REDIRECT':
                results['redirect'].append(result)
            elif status == 'SKIPPED':
                results['skipped'].append(result)
            elif status == 'TIMEOUT':
                results['timeout'].append(result)
            elif status == 'SSL_ERROR':
                results['ssl_error'].append(result)
            elif status.startswith('HTTP_') or status in ['CONNECTION_ERROR', 'NO_URL']:
                results['broken'].append(result)
            else:
                results['other_error'].append(result)
            
            # Progress update every 50 items
            if checked % 50 == 0 or checked == total:
                elapsed = time.time() - start_time
                rate = checked / elapsed if elapsed > 0 else 0
                remaining = (total - checked) / rate if rate > 0 else 0
                print(f"Progress: {checked}/{total} ({checked*100//total}%) - " +
                      f"OK: {len(results['ok'])}, Broken: {len(results['broken'])}, " +
                      f"Timeout: {len(results['timeout'])} - ETA: {remaining:.0f}s")
    
    elapsed = time.time() - start_time
    print(f"\n{'='*80}")
    print(f"COMPLETED in {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
    print(f"{'='*80}")
    
    print(f"\n✅ OK: {len(results['ok'])}")
    print(f"🔄 Redirects (different domain): {len(results['redirect'])}")
    print(f"❌ Broken: {len(results['broken'])}")
    print(f"⏱️  Timeout: {len(results['timeout'])}")
    print(f"🔒 SSL Errors: {len(results['ssl_error'])}")
    print(f"⏭️  Skipped (social media): {len(results['skipped'])}")
    print(f"⚠️  Other Errors: {len(results['other_error'])}")
    
    # Report broken links
    if results['broken']:
        print(f"\n{'='*80}")
        print("BROKEN LINKS (need fixing or removal):")
        print(f"{'='*80}")
        for r in sorted(results['broken'], key=lambda x: x['category']):
            print(f"\n  [{r['category']}] {r['name']}")
            print(f"    URL: {r['url']}")
            print(f"    Error: {r['error']}")
    
    # Report timeouts
    if results['timeout']:
        print(f"\n{'='*80}")
        print("TIMEOUT (may be slow or blocking bots):")
        print(f"{'='*80}")
        for r in sorted(results['timeout'], key=lambda x: x['category']):
            print(f"\n  [{r['category']}] {r['name']}")
            print(f"    URL: {r['url']}")
    
    # Report SSL errors
    if results['ssl_error']:
        print(f"\n{'='*80}")
        print("SSL ERRORS (certificate issues):")
        print(f"{'='*80}")
        for r in sorted(results['ssl_error'], key=lambda x: x['category']):
            print(f"\n  [{r['category']}] {r['name']}")
            print(f"    URL: {r['url']}")
    
    # Report significant redirects
    if results['redirect']:
        print(f"\n{'='*80}")
        print("REDIRECTS TO DIFFERENT DOMAIN (may need URL update):")
        print(f"{'='*80}")
        for r in sorted(results['redirect'], key=lambda x: x['category']):
            print(f"\n  [{r['category']}] {r['name']}")
            print(f"    Original: {r['url']}")
            print(f"    Redirects to: {r['final_url']}")
    
    # Save detailed report
    report = {
        'summary': {
            'total': total,
            'ok': len(results['ok']),
            'broken': len(results['broken']),
            'timeout': len(results['timeout']),
            'ssl_error': len(results['ssl_error']),
            'redirect': len(results['redirect']),
            'skipped': len(results['skipped']),
            'other_error': len(results['other_error'])
        },
        'broken': results['broken'],
        'timeout': results['timeout'],
        'ssl_error': results['ssl_error'],
        'redirect': results['redirect'],
        'other_error': results['other_error']
    }
    
    with open('url_check_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Detailed report saved to url_check_report.json")

if __name__ == '__main__':
    main()
