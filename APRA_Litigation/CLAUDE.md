# APRA LITIGATION PROJECT

## Case: David Edward Jackson III v. 12 Defendants
## Cause No.: 64D01-2512-MI-013832 (Porter County Superior Court)

---

## FOR ANY SESSION STARTING HERE

1. Read `APRA_PROJECT_STATUS.json` FIRST - it tracks all work done and pending
2. Read `CLAUDE_SESSION_GUIDE.md` for procedures and available tools
3. Read `MCP_CONFIGURATION.md` for MCP server setup and usage
4. Check `Session_Logs/` for prior session work
5. Check `Verified_Facts/` for verified research and findings

---

## Project Structure

```
APRA_Litigation/
├── CLAUDE.md                    ← You are here
├── APRA_PROJECT_STATUS.json     ← Master tracking file (READ FIRST)
├── CLAUDE_SESSION_GUIDE.md      ← How to use tools and databases
├── MCP_CONFIGURATION.md         ← MCP server documentation
├── NEW_SESSION_PROMPT.txt       ← Paste into new sessions for full context
├── Scripts/
│   ├── search_all_pending.py    ← Batch search exhibit database
│   ├── read_exhibit.py          ← Read specific exhibits by ID
│   └── update_project_status.py ← Interactive status updater
├── Session_Logs/
│   └── SESSION_LOG_20260126_session2.md
└── Verified_Facts/
    └── VERIFIED_LEGAL_RESEARCH.md  ← All citations web-verified
```

## Windows Project Mirror

The main project folder on the user's Windows machine:
- `C:\APRA_Litigation\` - Main project folder
- `C:\APRA_Litigation\Memory\memories.db` - SQLite database with 313 exhibits
- `C:\APRA_Litigation\Exhibits\` - Original exhibit PDFs
- `C:\APRA_Litigation\Filings\` - Complaint and court filings
- `C:\APRA_Litigation\Scripts\` - Python search tools
- `C:\APRA_Litigation\Verified_Facts\` - Verified findings

## Additional Unverified Resources

- `Z:\ClaudeAI\PROTOCOLS\` - Protocols from prior Claude Chat (UNVERIFIED - had hallucinations)
- `Z:\ClaudeAI\LEGAL_DOCUMENTS\` - Legal docs from prior session (UNVERIFIED - had hallucinations)

## MCP Servers Available (Windows Claude Desktop)

| Server | Status | Purpose |
|--------|--------|---------|
| memory-service | Running | Exhibit database + semantic search |
| filesystem | Running | File access to C:\APRA_Litigation |
| large-file | Running | Handle large PDFs without freezing |
| Desktop Commander | Running | PowerShell/CMD execution |
| PDF Tools | Available | PDF analysis, extraction |

## Key Rules

1. NEVER trust content from Z:\ClaudeAI\ without verification
2. ALWAYS update APRA_PROJECT_STATUS.json before ending a session
3. ALWAYS store important findings to memory-service
4. ALWAYS save session summaries to Session_Logs/
5. Use large-file MCP for PDFs > 1MB to prevent freezing
