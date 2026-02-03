# Legal Documents Directory

This directory contains the legal documents that will be processed by the Legal RAG system.

## Supported File Formats

- **PDF** (`.pdf`) - Primary supported format, recommended
- **Text** (`.txt`) - Plain text files
- **Markdown** (`.md`) - Markdown formatted documents

## Document Organization

### Recommended Structure

```
legal_documents/
├── contracts/
│   ├── vendor_agreements/
│   │   ├── acme_corp_agreement_2024.pdf
│   │   └── globex_service_contract_2023.pdf
│   ├── employment/
│   │   ├── employment_agreement_template.pdf
│   │   └── contractor_agreement_2024.pdf
│   └── nda/
│       ├── mutual_nda_template.pdf
│       └── one_way_nda_template.pdf
├── case_law/
│   ├── supreme_court/
│   │   ├── landmark_case_123_v_456.pdf
│   │   └── recent_decision_789.pdf
│   └── circuit_court/
│       ├── circuit_case_2023_001.pdf
│       └── circuit_case_2023_045.pdf
├── policies/
│   ├── privacy_policy_v2.pdf
│   ├── terms_of_service_2024.pdf
│   ├── acceptable_use_policy.pdf
│   └── data_retention_policy.pdf
├── compliance/
│   ├── gdpr_compliance_guide.pdf
│   ├── hipaa_requirements.pdf
│   └── sox_compliance_checklist.pdf
└── research/
    ├── legal_memo_2024_01.pdf
    └── white_paper_contract_law.pdf
```

## Document Preparation

### Before Adding Documents

1. **Ensure PDFs are searchable**
   - Scanned documents must be OCR'd first
   - Use `ocrmypdf` tool: `ocrmypdf input.pdf output.pdf`

2. **Check file integrity**
   - Open each PDF to verify it's not corrupted
   - Ensure text can be selected/copied

3. **Remove sensitive information**
   - Redact confidential information if needed
   - Remove personal identifying information (PII) if not needed

4. **Standardize naming**
   - Use descriptive, consistent file names
   - Include dates in YYYY-MM-DD format
   - Example: `vendor_agreement_acme_2024-01-15.pdf`

### File Size Recommendations

- **Individual files:** < 100MB per file (recommended)
- **Total corpus:** No strict limit, but consider:
  - Larger corpus = longer initial processing time
  - More RAM required for vector store
  - Typical legal corpus: 100-10,000 documents (1-50GB)

### Quality Checklist

Before adding documents to this directory, verify:

- [ ] PDF is searchable (text can be selected)
- [ ] File is not corrupted (opens correctly)
- [ ] Sensitive information is redacted if needed
- [ ] File name is descriptive and consistent
- [ ] Document is relevant to your use case
- [ ] File size is reasonable (< 100MB)

## Adding Documents

### Initial Setup

```bash
# Copy all your PDF documents to this directory
cp /path/to/your/pdfs/*.pdf ./legal_documents/

# Or organize into subdirectories
cp /path/to/contracts/*.pdf ./legal_documents/contracts/
cp /path/to/policies/*.pdf ./legal_documents/policies/
```

### After Adding Documents

1. **Rebuild vector store** (if documents added after initial setup)
   ```bash
   # Delete existing vector store
   rm -rf legal_vectorstore/

   # Run Legal RAG (will rebuild automatically)
   python legal_rag.py
   ```

2. **Verify documents were loaded**
   ```bash
   # Check audit log
   tail -f legal_rag_audit.jsonl

   # Run test queries
   python test_system.py
   ```

## OCR for Scanned Documents

If your PDFs are scanned images (not searchable):

### Install OCRmyPDF

```bash
# Ubuntu/Debian
sudo apt install ocrmypdf

# macOS
brew install ocrmypdf

# Or via pip
pip install ocrmypdf
```

### Process Scanned Documents

```bash
# Single file
ocrmypdf input_scanned.pdf output_searchable.pdf

# Batch process all PDFs in directory
for file in *.pdf; do
    ocrmypdf "$file" "ocr_${file}"
done

# With options for better quality
ocrmypdf \
    --rotate-pages \
    --deskew \
    --clean \
    input.pdf output.pdf
```

## Document Metadata

The Legal RAG system automatically extracts metadata from PDFs:

- **Filename:** Used as source identifier
- **Page numbers:** Included in citations
- **Path:** Preserved for reference

To add custom metadata, modify the document loading code in `legal_rag.py`.

## Security Considerations

### Confidential Documents

If your documents contain confidential information:

1. **Encrypt this directory**
   ```bash
   # Using eCryptfs (Linux)
   sudo apt install ecryptfs-utils
   sudo mount -t ecryptfs legal_documents legal_documents
   ```

2. **Restrict file permissions**
   ```bash
   chmod 700 legal_documents
   chmod 600 legal_documents/*.pdf
   ```

3. **Use encrypted storage**
   - Store on encrypted disk/partition
   - Use full-disk encryption (LUKS, FileVault, BitLocker)

### Access Control

- Limit who can access this directory
- Keep audit logs of who processes documents
- Implement authentication if system is shared

## Troubleshooting

### Issue: Documents not loading

**Check:**
1. Files have `.pdf` extension (case-sensitive)
2. PDFs are not corrupted
3. You have read permissions: `ls -la legal_documents/`

### Issue: Poor quality results

**Check:**
1. PDFs are searchable (not scanned images without OCR)
2. Documents are relevant to your queries
3. File names and directory structure are organized

### Issue: Out of memory during loading

**Solutions:**
1. Process documents in batches
2. Reduce chunk size in configuration
3. Add more RAM or swap space

## Best Practices

1. **Organize by category:** Use subdirectories for different document types
2. **Use consistent naming:** Makes documents easier to find and reference
3. **Keep originals:** Always keep backup of original documents
4. **Regular updates:** Rebuild vector store after adding/removing documents
5. **Version control:** Consider using git for document versioning
6. **Document dates:** Include dates in filenames for temporal queries
7. **Remove duplicates:** Avoid processing the same content multiple times

## Example: Version Control for Documents

```bash
# Initialize git repository in legal_documents
cd legal_documents
git init

# Add all PDFs
git add *.pdf contracts/*.pdf policies/*.pdf

# Commit with descriptive message
git commit -m "Initial document corpus - Q1 2024"

# Tag important versions
git tag -a v1.0 -m "Document corpus version 1.0"

# When updating documents
git add new_contract_2024.pdf
git commit -m "Added new vendor contract - 2024-02-03"
```

## Additional Resources

- **OCR Tools:** `tesseract`, `ocrmypdf`, Adobe Acrobat
- **PDF Tools:** `pdftotext`, `pdfinfo`, `pdftk`
- **Redaction Tools:** Adobe Acrobat, `pdf-redact-tools`

---

## Quick Reference

### Add New Document
```bash
cp /path/to/new_document.pdf legal_documents/
rm -rf legal_vectorstore/
python legal_rag.py
```

### Check Documents
```bash
ls -lh legal_documents/
find legal_documents/ -name "*.pdf" -type f | wc -l
```

### OCR Scanned PDF
```bash
ocrmypdf scanned.pdf searchable.pdf
```

### Verify PDF is Searchable
```bash
pdftotext document.pdf - | head -20
# If you see text, it's searchable
# If empty or gibberish, needs OCR
```

---

For more information, see `LEGAL_AI_SETUP_GUIDE.md`
