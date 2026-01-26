# APRA LITIGATION PROJECT - SESSION GUIDE

## FOR ANY CLAUDE SESSION (Chat or Code)

**FIRST ACTION**: Read `C:\APRA_Litigation\APRA_PROJECT_STATUS.json` to understand:
- What has been completed
- What is pending
- Critical findings documented
- Pending searches needed

---

## PROJECT OVERVIEW

**Case**: David Edward Jackson III v. 12 Defendants
**Cause No.**: 64D01-2512-MI-013832
**Court**: Porter County Superior Court
**Type**: APRA (Access to Public Records Act) violations

---

## DATABASE ACCESS

**SQLite Database**: `C:\APRA_Litigation\Memory\memories.db`
- 313 exhibits indexed
- 288 fully processed, 25 need OCR
- Total text: 4.3M+ characters

**Table Schema** (exhibits):
- id, hash, filename, filepath, content, content_preview
- file_type, size_kb, tags, created_date, ingested_date, page_count

---

## SEARCH TOOLS

### Option 1: Python Scripts (PowerShell)
```powershell
# Run all pending searches
python C:\APRA_Litigation\Scripts\search_all_pending.py

# Search for specific term
python C:\APRA_Litigation\Scripts\search_exhibits.py "immunity agreement"

# Read specific exhibit by ID
python C:\APRA_Litigation\Scripts\read_exhibit.py --id 42

# List all exhibits
python C:\APRA_Litigation\Scripts\read_exhibit.py --list
```

### Option 2: MCP Memory Service
```
Search memory for "immunity agreement Kastigar"
Search memory for "Nadia Wardrip transcript"
```

### Option 3: Direct SQL (via Desktop Commander)
```sql
SELECT filename, SUBSTR(content, 1, 500)
FROM exhibits
WHERE LOWER(content) LIKE '%kastigar%'
```

---

## CRITICAL FINDINGS ALREADY DOCUMENTED

### 1. Mandatory Reporting Violation ✅
- **Who**: Detective Robert Brazil + Victim Advocate Rochelle Ellis
- **What**: Concealed disclosure of abuse by cousin "Jaden"
- **When**: March 16, 2018
- **Evidence**: SRT transcript 10:20-11:07
- **Status**: DOCUMENTED in memory-service

### 2. Perpetrator Substitution ✅
- Detective Brazil asked if events were "amassed by what happened with Jayden"
- Shows detective considered confusion - never disclosed to defense
- **Status**: DOCUMENTED in memory-service

### 3. Racial Discrimination Pattern ✅
- Plaintiff is Latino/Puerto Rican
- NAACP investigation of Hobart PD (Oct 2022)
- Hobart officer racial remarks investigation (June 2020)
- **Status**: DOCUMENTED in memory-service

---

## PENDING INVESTIGATIONS

### HIGH PRIORITY:

1. **Jurisdictional Void**
   - Find: Plea Agreement (Nov 2021), Sentencing Order, Porter County docket
   - Issue: Porter County never accepted probation transfer
   - Significance: Revocation based on void jurisdiction

2. **Kastigar Immunity**
   - Find: Immunity agreement, court order prohibiting use
   - Issue: Use and derivative use protection violated?

3. **Family Case Interference**
   - Find: Nadia Wardrip transcripts/emails, Jacob Otto transcripts/emails
   - Issue: Prosecutor interference in civil custody case

### DEFENDANT VERIFICATION NEEDED:
- Office of Attorney General (Rachel Stark acknowledgment)
- Lake County Prosecutor
- Lake County Adult Probation
- Indiana Office of Judicial Admin
- Lake County Sheriff
- IDOC (specific denial letter)

---

## UPDATING PROJECT STATUS

After completing work, update `APRA_PROJECT_STATUS.json`:
1. Move completed items from `pending_tasks` to `completed_tasks`
2. Update `pending_searches` status
3. Add new findings to `critical_findings`
4. Update `last_updated` and `last_session`

---

## FILE LOCATIONS

| File | Path |
|------|------|
| Project Status | `C:\APRA_Litigation\APRA_PROJECT_STATUS.json` |
| Database | `C:\APRA_Litigation\Memory\memories.db` |
| Complaint (original) | `C:\APRA_Litigation\Filings\PLAINTIFF'S APRA COMPLAINT AND FILINGS.docx` |
| Complaint (text) | `C:\APRA_Litigation\Filings\complaint_lines.txt` |
| Search Scripts | `C:\APRA_Litigation\Scripts\` |
| Search Results | `C:\APRA_Litigation\Search_Results\` |
| Exhibit Inventory | `C:\APRA_Litigation\exhibit_inventory.csv` |

---

## SESSION HANDOFF PROTOCOL

Before ending a session:
1. Update `APRA_PROJECT_STATUS.json` with completed work
2. Save any new findings to memory-service
3. Document any blockers or issues encountered
4. List specific next actions needed

This ensures continuity across sessions with no lost context.
