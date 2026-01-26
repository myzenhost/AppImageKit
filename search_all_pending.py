#!/usr/bin/env python3
"""
APRA Litigation - Batch Search Script
Searches the exhibit database for all pending queries and outputs results.
Run in PowerShell: python C:\APRA_Litigation\Scripts\search_all_pending.py
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = r"C:\APRA_Litigation\Memory\memories.db"
STATUS_FILE = r"C:\APRA_Litigation\APRA_PROJECT_STATUS.json"
OUTPUT_DIR = r"C:\APRA_Litigation\Search_Results"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# All pending searches
SEARCHES = [
    {"id": 1, "query": "Nadia Wardrip", "alt_queries": ["Wardrip transcript", "Wardrip email", "family civil custody Wardrip"]},
    {"id": 2, "query": "Jacob Otto", "alt_queries": ["Otto transcript", "Otto email", "family civil Otto"]},
    {"id": 3, "query": "immunity agreement", "alt_queries": ["Kastigar", "use derivative", "immunity Kastigar"]},
    {"id": 4, "query": "court order prosecutor", "alt_queries": ["NOT use information", "ordered not to use", "prohibition order"]},
    {"id": 5, "query": "plea agreement", "alt_queries": ["November 2021 plea", "plea Porter County", "plea transfer"]},
    {"id": 6, "query": "sentencing order", "alt_queries": ["November 2021 sentencing", "sentencing Porter", "sentence transfer"]},
    {"id": 7, "query": "Porter County docket", "alt_queries": ["CCS Porter", "Mycase Porter", "transfer acceptance Porter"]},
    {"id": 8, "query": "Rachel Stark", "alt_queries": ["Attorney General acknowledgment", "OAG Stark", "Stark August"]},
    {"id": 9, "query": "Lake County Prosecutor", "alt_queries": ["prosecutor denial", "prosecutor response", "final demand prosecutor"]},
    {"id": 10, "query": "IDOC denial", "alt_queries": ["Department of Correction denial", "IDOC response letter"]},
]

def search_database(query_terms):
    """Search database for terms, return matching records."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    words = query_terms.lower().split()
    conditions = []
    params = []

    for word in words:
        conditions.append("(LOWER(content) LIKE ? OR LOWER(filename) LIKE ? OR LOWER(tags) LIKE ?)")
        params.extend([f"%{word}%", f"%{word}%", f"%{word}%"])

    where_clause = " AND ".join(conditions)

    cur.execute(f"""
        SELECT id, filename, filepath, tags, LENGTH(content) as chars,
               SUBSTR(content, 1, 2000) as preview
        FROM exhibits
        WHERE {where_clause}
        ORDER BY chars DESC
        LIMIT 20
    """, params)

    results = cur.fetchall()
    conn.close()
    return results

def run_all_searches():
    """Run all pending searches and save results."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    master_output = []

    print(f"=" * 60)
    print(f"APRA LITIGATION - BATCH SEARCH")
    print(f"Running at: {datetime.now()}")
    print(f"=" * 60)

    for search in SEARCHES:
        print(f"\n[Search {search['id']}] {search['query']}")
        print("-" * 40)

        all_results = []
        seen_ids = set()

        # Search primary query
        results = search_database(search['query'])
        for r in results:
            if r[0] not in seen_ids:
                all_results.append(r)
                seen_ids.add(r[0])

        # Search alternate queries
        for alt in search.get('alt_queries', []):
            results = search_database(alt)
            for r in results:
                if r[0] not in seen_ids:
                    all_results.append(r)
                    seen_ids.add(r[0])

        search_result = {
            "search_id": search['id'],
            "query": search['query'],
            "alt_queries": search.get('alt_queries', []),
            "total_found": len(all_results),
            "files": []
        }

        if all_results:
            print(f"  Found {len(all_results)} matching exhibits:")
            for r in all_results[:10]:  # Show top 10
                print(f"    - {r[1]}")
                print(f"      Tags: {r[3]}")
                print(f"      Chars: {r[4]}")
                search_result["files"].append({
                    "id": r[0],
                    "filename": r[1],
                    "filepath": r[2],
                    "tags": r[3],
                    "chars": r[4],
                    "preview": r[5][:500] if r[5] else ""
                })
        else:
            print(f"  No results found")

        master_output.append(search_result)

        # Save individual search result
        output_file = os.path.join(OUTPUT_DIR, f"search_{search['id']:02d}_{search['query'].replace(' ', '_')[:20]}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(search_result, f, indent=2, ensure_ascii=False)

    # Save master results
    master_file = os.path.join(OUTPUT_DIR, f"ALL_SEARCH_RESULTS_{timestamp}.json")
    with open(master_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": timestamp,
            "total_searches": len(SEARCHES),
            "results": master_output
        }, f, indent=2, ensure_ascii=False)

    print(f"\n" + "=" * 60)
    print(f"SEARCH COMPLETE")
    print(f"Results saved to: {OUTPUT_DIR}")
    print(f"Master file: {master_file}")
    print(f"=" * 60)

    # Summary
    print(f"\nSUMMARY:")
    for result in master_output:
        status = "FOUND" if result['total_found'] > 0 else "NOT FOUND"
        print(f"  [{status:9}] Search {result['search_id']}: {result['query']} ({result['total_found']} files)")

    return master_output

if __name__ == "__main__":
    run_all_searches()
