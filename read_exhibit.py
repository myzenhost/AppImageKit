#!/usr/bin/env python3
"""
APRA Litigation - Read Specific Exhibit
Reads full content of an exhibit by ID or filename search.
Usage: python read_exhibit.py "filename search term"
       python read_exhibit.py --id 42
"""

import sqlite3
import sys
import os

DB_PATH = r"C:\APRA_Litigation\Memory\memories.db"
OUTPUT_DIR = r"C:\APRA_Litigation\Search_Results"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def read_by_id(exhibit_id):
    """Read exhibit by database ID."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, filename, filepath, content, tags, page_count
        FROM exhibits WHERE id = ?
    """, (exhibit_id,))
    result = cur.fetchone()
    conn.close()
    return result

def search_and_read(search_term):
    """Search for exhibit and display matches."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, filename, filepath, LENGTH(content) as chars, tags
        FROM exhibits
        WHERE LOWER(filename) LIKE ? OR LOWER(content) LIKE ?
        ORDER BY chars DESC
        LIMIT 20
    """, (f"%{search_term.lower()}%", f"%{search_term.lower()}%"))
    results = cur.fetchall()
    conn.close()
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python read_exhibit.py \"search term\"")
        print("       python read_exhibit.py --id 42")
        print("       python read_exhibit.py --list   (show all exhibits)")
        sys.exit(1)

    if sys.argv[1] == "--id" and len(sys.argv) > 2:
        exhibit_id = int(sys.argv[2])
        result = read_by_id(exhibit_id)
        if result:
            print(f"=" * 60)
            print(f"EXHIBIT ID: {result[0]}")
            print(f"FILENAME: {result[1]}")
            print(f"PATH: {result[2]}")
            print(f"TAGS: {result[4]}")
            print(f"PAGES: {result[5]}")
            print(f"=" * 60)
            print(f"\nCONTENT:\n")
            print(result[3])

            # Save to file
            safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in result[1])[:50]
            output_file = os.path.join(OUTPUT_DIR, f"exhibit_{exhibit_id}_{safe_name}.txt")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"EXHIBIT ID: {result[0]}\n")
                f.write(f"FILENAME: {result[1]}\n")
                f.write(f"PATH: {result[2]}\n")
                f.write(f"TAGS: {result[4]}\n")
                f.write(f"PAGES: {result[5]}\n")
                f.write("=" * 60 + "\n\n")
                f.write(result[3])
            print(f"\n\nSaved to: {output_file}")
        else:
            print(f"No exhibit found with ID {exhibit_id}")

    elif sys.argv[1] == "--list":
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT id, filename, tags, LENGTH(content) as chars
            FROM exhibits ORDER BY filename
        """)
        results = cur.fetchall()
        conn.close()
        print(f"{'ID':>4} | {'Filename':<60} | {'Chars':>8} | Tags")
        print("-" * 120)
        for r in results:
            print(f"{r[0]:>4} | {r[1][:60]:<60} | {r[3]:>8} | {r[2][:30] if r[2] else ''}")

    else:
        search_term = " ".join(sys.argv[1:])
        results = search_and_read(search_term)
        if results:
            print(f"Found {len(results)} exhibits matching '{search_term}':\n")
            print(f"{'ID':>4} | {'Filename':<60} | {'Chars':>8}")
            print("-" * 80)
            for r in results:
                print(f"{r[0]:>4} | {r[1][:60]:<60} | {r[3]:>8}")
            print(f"\nTo read full content: python read_exhibit.py --id <ID>")
        else:
            print(f"No exhibits found matching '{search_term}'")

if __name__ == "__main__":
    main()
