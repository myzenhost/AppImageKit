#!/usr/bin/env python3
"""
APRA Litigation - Update Project Status
Updates the APRA_PROJECT_STATUS.json file after completing work.
Usage: python update_project_status.py
"""

import json
import os
from datetime import datetime

STATUS_FILE = r"C:\APRA_Litigation\APRA_PROJECT_STATUS.json"

def load_status():
    """Load current status."""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_status(status):
    """Save updated status."""
    status['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
    print(f"Status saved to {STATUS_FILE}")

def mark_task_complete(status, task_description):
    """Move a task from pending to completed."""
    if task_description in status['pending_tasks']:
        status['pending_tasks'].remove(task_description)
        status['completed_tasks'].append(task_description)
        print(f"Marked complete: {task_description}")
    else:
        print(f"Task not found in pending: {task_description}")
    return status

def mark_search_complete(status, search_id, found=True):
    """Mark a pending search as complete."""
    for search in status['pending_searches']:
        if search['id'] == search_id:
            search['status'] = 'found' if found else 'not_found'
            print(f"Search {search_id} marked as {'found' if found else 'not found'}")
            return status
    print(f"Search ID {search_id} not found")
    return status

def add_finding(status, category, key, value):
    """Add or update a critical finding."""
    if category not in status['critical_findings']:
        status['critical_findings'][category] = {}
    status['critical_findings'][category][key] = value
    print(f"Added finding: {category}.{key}")
    return status

def add_pending_task(status, task):
    """Add a new pending task."""
    if task not in status['pending_tasks']:
        status['pending_tasks'].append(task)
        print(f"Added pending task: {task}")
    return status

def set_session_name(status, name):
    """Set the last session name."""
    status['last_session'] = name
    return status

def interactive_menu():
    """Interactive menu for updating status."""
    status = load_status()
    if not status:
        print("Could not load status file!")
        return

    while True:
        print("\n" + "=" * 50)
        print("APRA PROJECT STATUS UPDATER")
        print("=" * 50)
        print("1. Mark task complete")
        print("2. Mark search complete")
        print("3. Add new pending task")
        print("4. Add critical finding")
        print("5. Set session name")
        print("6. View current status")
        print("7. Save and exit")
        print("8. Exit without saving")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            print("\nPending tasks:")
            for i, task in enumerate(status['pending_tasks']):
                print(f"  {i+1}. {task}")
            idx = input("Enter task number to complete: ").strip()
            if idx.isdigit() and 0 < int(idx) <= len(status['pending_tasks']):
                task = status['pending_tasks'][int(idx)-1]
                status = mark_task_complete(status, task)

        elif choice == '2':
            print("\nPending searches:")
            for s in status['pending_searches']:
                if s['status'] == 'pending':
                    print(f"  {s['id']}. {s['query']} - {s['purpose']}")
            sid = input("Enter search ID to mark complete: ").strip()
            found = input("Was it found? (y/n): ").strip().lower() == 'y'
            if sid.isdigit():
                status = mark_search_complete(status, int(sid), found)

        elif choice == '3':
            task = input("Enter new task description: ").strip()
            if task:
                status = add_pending_task(status, task)

        elif choice == '4':
            category = input("Category (e.g., 'immunity_violation'): ").strip()
            key = input("Key (e.g., 'status'): ").strip()
            value = input("Value: ").strip()
            if category and key and value:
                status = add_finding(status, category, key, value)

        elif choice == '5':
            name = input("Session name: ").strip()
            if name:
                status = set_session_name(status, name)

        elif choice == '6':
            print("\n" + json.dumps(status, indent=2))

        elif choice == '7':
            save_status(status)
            break

        elif choice == '8':
            print("Exiting without saving.")
            break

if __name__ == "__main__":
    interactive_menu()
