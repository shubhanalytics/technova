import json
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

DATA_PATH = "data.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def is_wikipedia(url: str) -> bool:
    return url and "wikipedia.org" in url


def looks_like_list_or_meta(name: str, url: str) -> bool:
    if not name:
        return True
    lower = name.lower()
    if any(tok in lower for tok in ("list of", "template", "edit", "timeline", "comparison of", "special:")):
        return True
    if url and ("w/index.php" in url or "Template:" in url or "Special:" in url):
        return True
    return False


def find_official_site_from_wikipedia(page_html: str, base_url: str, name: str) -> str | None:
    soup = BeautifulSoup(page_html, "html.parser")

    # 1) Look in infobox for 'Website' or external link
    infobox = soup.find("table", class_=lambda c: c and "infobox" in c)
    if infobox:
        # Try to find between th with 'Website' and following td
        for th in infobox.find_all("th"):
            if th.get_text(strip=True).lower().startswith("website") or th.get_text(strip=True).lower().startswith("official website"):
                td = th.find_next_sibling("td")
                if td:
                    a = td.find("a", href=True)
                    if a and a["href"].startswith("http") and "wikipedia.org" not in a["href"]:
                        return a["href"]
        # As fallback: any external link in the infobox
        for a in infobox.find_all("a", href=True):
            href = a["href"]
            if href.startswith("http") and "wikipedia.org" not in href and "wikimedia.org" not in href:
                return href

    # 2) External links section
    el = soup.find(id="External_links") or soup.find(id="External_links_and_sources")
    if el:
        # external links are usually in the next sibling ul
        for sib in el.parent.find_all_next():
            if sib.name == "ul":
                a = sib.find("a", href=True)
                if a and a["href"].startswith("http") and "wikipedia.org" not in a["href"]:
                    return a["href"]
                break

    # 3) Find first external link in content area
    content = soup.find(id="bodyContent") or soup.find(id="mw-content-text") or soup
    if content:
        for a in content.find_all("a", href=True):
            href = a["href"]
            if href.startswith("//"):
                href = "https:" + href
            if href.startswith("http") and "wikipedia.org" not in href and "wikimedia.org" not in href:
                # Heuristic: avoid links to blogs, citations or social sites when possible
                if any(skip in href for skip in ("/cite.", "#cite", "facebook.com", "twitter.com", "linkedin.com", "youtube.com")):
                    continue
                return href

    return None


def enrich_items(items: list) -> tuple[list, int]:
    changed = 0
    session = requests.Session()
    session.headers.update(HEADERS)

    for it in items:
        url = it.get("url") or ""
        name = it.get("name") or ""
        if not url:
            continue
        if not is_wikipedia(url):
            continue
        if looks_like_list_or_meta(name, url):
            continue

        try:
            resp = session.get(url, timeout=12)
            if resp.status_code != 200:
                continue
            new_url = find_official_site_from_wikipedia(resp.text, url, name)
            if new_url and new_url != url:
                it["url"] = new_url
                changed += 1
                print(f"Replaced wiki link for '{name}' -> {new_url}")
            time.sleep(0.3)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            continue

    return items, changed


def append_missing_items(items: list) -> int:
    # Small curated list of commonly expected items that may be missing
    extras = [
        {"name": "MDN Web Docs", "url": "https://developer.mozilla.org/", "category": "Tool", "sector": "Documentation", "country": "Worldwide", "description": "Web platform documentation"},
        {"name": "Stack Overflow", "url": "https://stackoverflow.com/", "category": "Tool", "sector": "Community", "country": "Worldwide", "description": "Q&A for programmers"},
        {"name": "Amazon Web Services", "url": "https://aws.amazon.com/", "category": "Tool", "sector": "Cloud", "country": "USA", "description": "Cloud services"},
        {"name": "Google Cloud", "url": "https://cloud.google.com/", "category": "Tool", "sector": "Cloud", "country": "USA", "description": "Cloud platform"},
        {"name": "Microsoft Azure", "url": "https://azure.microsoft.com/", "category": "Tool", "sector": "Cloud", "country": "USA", "description": "Cloud platform"},
        {"name": "Vercel", "url": "https://vercel.com/", "category": "Tool", "sector": "Hosting", "country": "USA", "description": "Frontend deployment platform"},
        {"name": "Netlify", "url": "https://www.netlify.com/", "category": "Tool", "sector": "Hosting", "country": "USA", "description": "Static site hosting"},
        {"name": "Heroku", "url": "https://www.heroku.com/", "category": "Tool", "sector": "Hosting", "country": "USA", "description": "Platform as a Service"},
        {"name": "ESLint", "url": "https://eslint.org/", "category": "Tool", "sector": "Developer Tools", "country": "Worldwide", "description": "JavaScript linter"},
        {"name": "Prettier", "url": "https://prettier.io/", "category": "Tool", "sector": "Developer Tools", "country": "Worldwide", "description": "Code formatter"},
    ]

    existing = { (it.get("name","" ).lower(), it.get("url","")) for it in items }
    added = 0
    for ex in extras:
        key = (ex["name"].lower(), ex["url"])
        if not any(it.get("name","" ).lower() == ex["name"].lower() for it in items):
            items.append(ex)
            added += 1
            print(f"Appended missing item: {ex['name']}")

    return added


def main():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    # Backup
    with open(DATA_PATH + ".bak", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"Loaded {len(items)} items; starting enrichment...")
    items, changed = enrich_items(items)
    print(f"Enrichment complete. Replaced {changed} Wikipedia links.")

    added = append_missing_items(items)
    print(f"Appended {added} extra items.")

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"Saved updated {DATA_PATH} (backup at {DATA_PATH}.bak).")


if __name__ == "__main__":
    main()
