# MCP (Model Context Protocol) CONFIGURATION

## FOR ALL CLAUDE SESSIONS

This document tracks all MCP servers, extensions, and memory systems configured for this project.

---

## CONFIGURED MCP SERVERS

### 1. filesystem (Custom)
**Purpose**: Direct access to project files
**Status**: RUNNING
**Config Location**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\APRA_Litigation", "C:\\Users\\Avatar\\Desktop"]
  }
}
```

**Capabilities**:
- Read files from C:\APRA_Litigation and Desktop
- List directories
- Get file info
- Write files (if permitted)

**Usage**:
```
Use filesystem tool to read C:\APRA_Litigation\APRA_PROJECT_STATUS.json
Use filesystem tool to list C:\APRA_Litigation\Exhibits
```

---

### 2. memory-service (Custom)
**Purpose**: Persistent memory across sessions, semantic search
**Status**: RUNNING
**Database**: `C:\APRA_Litigation\Memory\memories.db`

```json
{
  "memory-service": {
    "command": "C:\\Python314\\python.exe",
    "args": ["-m", "mcp_memory_service.server"],
    "env": {
      "MCP_MEMORY_DIR": "C:\\APRA_Litigation\\Memory"
    }
  }
}
```

**Capabilities**:
- Store memories (facts, findings, analysis)
- Search memories (semantic + keyword)
- Dream-inspired consolidation ("REM Sleep")
- Recall across sessions

**Usage**:
```
Search memory for "mandatory reporting violation Brazil"
Store memory: "Key finding: Porter County never accepted transfer"
```

---

## AVAILABLE EXTENSIONS (Claude Code Desktop Commander)

Based on Developer settings screenshot, these extensions are available:

| Extension | Purpose | Status |
|-----------|---------|--------|
| **Filesystem** (capital F) | Built-in file access | Running |
| **Desktop Commander** | PowerShell/CMD execution, file operations | Running |
| **PDF Tools - Analyze** | PDF reading, analysis | Available |
| **PopHIVE Public Health** | Health data | Available |
| **Kubernetes MCP Server** | K8s operations | Available |
| **Enrichr MCP Server** | Data enrichment | Available |
| **ToolUniverse** | Multi-tool access | Available |
| **Context7** | Context management | Available |
| **B12 Website Generator** | Web generation | Available |
| **filesystem** (lowercase) | Custom - APRA project | Running |
| **memory-service** | Custom - Exhibit database | Running |

---

## KEY EXTENSION USAGE FOR THIS PROJECT

### Desktop Commander
```
Desktop Commander: Start Terminal Process
powershell -Command "Get-Content file.txt"

Desktop Commander: Read File or URL
C:\path\to\file.txt

Desktop Commander: Get File Information
C:\path\to\file
```

### PDF Tools
Use for the 25 scanned PDFs that need OCR:
```
PDF Tools: Analyze PDF
C:\APRA_Litigation\Exhibits\scanned_document.pdf
```

### Memory Service
```
memory-service: Search Memories (Unified)
query terms here

memory-service: Store Memory
Content to store with tags
```

---

## CONFIGURATION FILE LOCATION

**Claude Desktop Config**:
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Full path**:
```
C:\Users\Avatar\AppData\Roaming\Claude\claude_desktop_config.json
```

**Current Configuration**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\APRA_Litigation", "C:\\Users\\Avatar\\Desktop"]
    },
    "memory-service": {
      "command": "C:\\Python314\\python.exe",
      "args": ["-m", "mcp_memory_service.server"],
      "env": {
        "MCP_MEMORY_DIR": "C:\\APRA_Litigation\\Memory"
      }
    }
  }
}
```

---

## EXTENDING MCP CAPABILITIES

### To Add New MCP Servers:
1. Install the server package (npm or pip)
2. Add configuration to `claude_desktop_config.json`
3. Restart Claude Desktop
4. Verify in Settings > Developer > MCP Servers

### Useful MCP Servers to Consider:
- **@anthropic/mcp-server-sqlite** - Direct SQL access
- **@anthropic/mcp-server-puppeteer** - Web automation
- **@anthropic/mcp-server-brave-search** - Web search
- **mcp-server-fetch** - URL fetching

### Adding SQLite Direct Access (Recommended):
```json
{
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@anthropic/mcp-server-sqlite", "C:\\APRA_Litigation\\Memory\\memories.db"]
  }
}
```

---

## MEMORY SYSTEM FEATURES

The `mcp-memory-service` provides:

1. **Memory Skill**: Store and retrieve facts/findings
2. **REM Sleep**: Dream-inspired consolidation (automatic)
3. **Recall**: Semantic search across all stored memories

### What Gets Stored:
- Exhibit content (313 records)
- Critical findings (mandatory reporting, perpetrator substitution, etc.)
- Analysis results
- Cross-reference verifications

### Persistence:
All data persists in SQLite at `C:\APRA_Litigation\Memory\memories.db`
Any future session can access this data via memory-service or direct SQL.

---

## TROUBLESHOOTING

### MCP Server Not Appearing:
1. Check JSON syntax in config file
2. Ensure full paths (no environment variables)
3. Restart Claude Desktop completely
4. Check Developer > MCP Servers for status

### Memory Service Errors:
1. Verify Python path: `C:\Python314\python.exe`
2. Verify package installed: `pip show mcp-memory-service`
3. Check MCP_MEMORY_DIR path exists

### Filesystem Access Denied:
1. Verify path in config matches actual directory
2. Check Windows permissions on folder
3. Try running Claude Desktop as Administrator

---

## SESSION CONTINUITY CHECKLIST

When starting a new session:
- [ ] Read `APRA_PROJECT_STATUS.json` for current state
- [ ] Read `MCP_CONFIGURATION.md` for available tools
- [ ] Read `CLAUDE_SESSION_GUIDE.md` for procedures
- [ ] Check memory-service for stored findings
- [ ] Review pending searches and tasks

When ending a session:
- [ ] Update `APRA_PROJECT_STATUS.json`
- [ ] Store new findings to memory-service
- [ ] Document any new MCP configurations
- [ ] List next actions for future sessions
