#!/usr/bin/env python3
"""
Normalize ML-related categories in data.json to `AI/ML` and add `AI/ML` domain tag when missing.

Usage: python scripts/normalize_ml_categories.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data.json"

ML_CATEGORIES = {
    "ml framework",
    "ml frameworks",
    "ml library",
    "ml libraries",
    "ml ops",
    "mlops",
    "machine learning",
    "machine-learning",
}


def normalize(item: dict) -> bool:
    """Return True if item was changed."""
    changed = False
    cat = item.get("category") or item.get("Category") or ""
    if isinstance(cat, str) and cat.strip().lower() in ML_CATEGORIES:
        item["category"] = "AI/ML"
        changed = True

    # Ensure domains/tags list includes AI/ML
    domains = item.get("domains") or item.get("tags") or item.get("domain")
    if domains is None:
        # create domains field
        item["domains"] = ["AI/ML"]
        changed = True
    else:
        # normalize to list of lowercased strings
        if isinstance(domains, str):
            domains_list = [d.strip() for d in domains.split(",") if d.strip()]
        elif isinstance(domains, list):
            domains_list = domains
        else:
            domains_list = list(domains)

        # check case-insensitively
        low = {str(d).strip().lower() for d in domains_list}
        if "ai/ml" not in low and "ai" not in low and "ml" not in low:
            domains_list.append("AI/ML")
            item["domains"] = domains_list
            changed = True
        else:
            # preserve existing list form (but ensure `domains` key exists)
            if item.get("domains") is None:
                item["domains"] = domains_list
                changed = True

    return changed


def main():
    if not DATA.exists():
        print(f"data.json not found at {DATA}")
        return

    data = json.loads(DATA.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("Expected data.json to contain a top-level list of items.")
        return

    changed_count = 0
    for item in data:
        try:
            if normalize(item):
                changed_count += 1
        except Exception:
            # skip problematic items but continue
            continue

    if changed_count:
        backup = DATA.with_suffix(".bak")
        DATA.rename(backup)
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Normalized {changed_count} items. Backup saved to {backup}")
    else:
        print("No ML-category items needed normalization.")


if __name__ == "__main__":
    main()
