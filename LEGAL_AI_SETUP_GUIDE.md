# Legal RAG System - Complete Setup Guide

## Overview

This guide provides complete instructions for setting up a high-accuracy, CPU-based Legal RAG (Retrieval-Augmented Generation) system for processing legal documents with minimal hallucination risk.

**Key Features:**
- 98-99% accuracy retention with Q8_0/Q6_K quantization
- CPU-only inference (no GPU required)
- Local processing (no external API calls)
- Source verification and citation
- Hallucination detection
- Query audit logging
- Optimized for large legal documents (100K+ tokens)

**Target Use Cases:**
- Legal document analysis
- Contract review
- Case law research
- Compliance document processing
- Legal discovery

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start](#quick-start)
3. [Detailed Installation](#detailed-installation)
4. [Model Selection](#model-selection)
5. [Document Preparation](#document-preparation)
6. [Configuration](#configuration)
7. [Usage Examples](#usage-examples)
8. [Performance Optimization](#performance-optimization)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## System Requirements

### Minimum Requirements

**For 13B Models (Q8_0):**
- CPU: 8+ cores (Intel Core i7/i9, AMD Ryzen 7/9, or equivalent)
- RAM: 64GB
- Storage: 100GB free SSD space
- OS: Linux (Ubuntu 20.04+), macOS (12+), or Windows 10/11 with WSL2

**For 70B Models (Q8_0):**
- CPU: 12+ cores (Intel Xeon, AMD Threadripper, or EPYC)
- RAM: 128GB (256GB recommended)
- Storage: 200GB free SSD space (NVMe recommended)
- OS: Linux (Ubuntu 20.04+) or macOS (12+)

### Recommended Configurations

#### Budget Setup ($1,500-$2,000)
- CPU: AMD Ryzen 9 7950X (16 cores)
- RAM: 64GB DDR5-4800
- Storage: 1TB NVMe SSD
- **Best Model:** LLaMA 2 13B Q8_0 (~14GB)
- **Performance:** 3-5 tokens/sec

#### Professional Setup ($2,500-$3,500)
- CPU: AMD Threadripper 7960X (24 cores)
- RAM: 128GB DDR5-4800
- Storage: 2TB NVMe SSD
- **Best Model:** LLaMA 2 70B Q8_0 (~70GB)
- **Performance:** 5-8 tokens/sec

#### Enterprise Setup ($5,000-$8,000)
- CPU: AMD Threadripper PRO 7995WX (96 cores) or Dual Intel Xeon
- RAM: 256GB+ DDR5-4800
- Storage: 4TB NVMe SSD (RAID 0)
- **Best Model:** LLaMA 2 70B Q6_K (~55GB) with multi-instance
- **Performance:** 10-15 tokens/sec with parallel processing

---

## Quick Start

### Automated Installation (Recommended)

```bash
# 1. Clone or download the Legal RAG system
cd /path/to/legal-rag

# 2. Run automated setup
chmod +x setup.sh
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Download a model (see Model Selection section)
# Place .gguf file in ./models/

# 5. Add PDF documents to ./legal_documents/

# 6. Test the system
python test_system.py

# 7. Run Legal RAG
python legal_rag.py
```

---

## Detailed Installation

### Step 1: Install System Dependencies

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3-pip
sudo apt install -y build-essential cmake git
```

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and dependencies
brew install python@3.10 cmake
```

#### Windows (WSL2)
```powershell
# Install WSL2 and Ubuntu
wsl --install -d Ubuntu-22.04

# Then follow Ubuntu instructions inside WSL2
```

### Step 2: Set Up Python Environment

```bash
# Create project directory
mkdir -p ~/legal-rag
cd ~/legal-rag

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Step 3: Install Python Dependencies

```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt
```

**For CPU-specific optimization:**

```bash
# Intel CPU with AVX-512
CMAKE_ARGS="-DLLAMA_AVX512=on" pip install llama-cpp-python

# AMD CPU with AVX2
CMAKE_ARGS="-DLLAMA_AVX2=on" pip install llama-cpp-python

# Apple Silicon (M1/M2/M3)
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
```

### Step 4: Create Directory Structure

```bash
mkdir -p models
mkdir -p legal_documents
mkdir -p legal_vectorstore
```

---

## Model Selection

### Recommended Models for Legal Work

**Critical:** Legal work requires Q8_0 or Q6_K quantization. DO NOT use Q4 or lower for legal documents due to accuracy loss.

#### Best Accuracy: Q8_0 Quantization (99% accuracy retention)

| Model | Size | RAM Required | Speed | Download Link |
|-------|------|--------------|-------|---------------|
| LLaMA 2 70B Q8_0 | ~70GB | 128GB+ | 5-8 tok/sec | [HuggingFace](https://huggingface.co/TheBloke/Llama-2-70B-GGUF) |
| LLaMA 2 13B Q8_0 | ~14GB | 64GB+ | 8-12 tok/sec | [HuggingFace](https://huggingface.co/TheBloke/Llama-2-13B-GGUF) |
| Mistral 7B Q8_0 | ~8GB | 32GB+ | 12-18 tok/sec | [HuggingFace](https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF) |

#### Good Accuracy: Q6_K Quantization (98% accuracy retention)

| Model | Size | RAM Required | Speed | Download Link |
|-------|------|--------------|-------|---------------|
| LLaMA 2 70B Q6_K | ~55GB | 96GB+ | 6-10 tok/sec | [HuggingFace](https://huggingface.co/TheBloke/Llama-2-70B-GGUF) |
| LLaMA 2 13B Q6_K | ~11GB | 48GB+ | 10-15 tok/sec | [HuggingFace](https://huggingface.co/TheBloke/Llama-2-13B-GGUF) |

### How to Download Models

#### Method 1: Direct Download (Recommended)

```bash
# 1. Visit HuggingFace link
# 2. Find file named *Q8_0.gguf or *Q6_K.gguf
# 3. Click to download (may take 10-60 minutes depending on size)
# 4. Move to models directory

mv ~/Downloads/llama-2-70b.Q8_0.gguf ./models/
```

#### Method 2: Using huggingface-cli

```bash
# Install huggingface-cli
pip install huggingface_hub[cli]

# Download specific file
huggingface-cli download TheBloke/Llama-2-70B-GGUF llama-2-70b.Q8_0.gguf --local-dir ./models
```

### Quantization Quality Comparison

| Quantization | Accuracy | Use Case | Legal Work? |
|--------------|----------|----------|-------------|
| Q8_0 | 99% | Maximum accuracy | ✅ YES |
| Q6_K | 98% | High accuracy | ✅ YES |
| Q5_K_M | 97% | Balanced | ⚠️ Risky |
| Q4_K_M | 95% | Fast inference | ❌ NO |
| Q3_K_M | 90% | Very fast | ❌ NO |

**For legal work:** Use Q8_0 for maximum accuracy. Q6_K is acceptable if RAM is limited.

---

## Document Preparation

### Supported Formats

- **PDF:** Fully supported (recommended)
- **Word (.docx):** Requires `python-docx` (uncomment in requirements.txt)
- **Text (.txt):** Supported
- **Markdown (.md):** Supported
- **HTML:** Requires `beautifulsoup4` (uncomment in requirements.txt)

### Best Practices for Legal Documents

#### 1. File Organization

```
legal_documents/
├── contracts/
│   ├── vendor_agreement_2024.pdf
│   └── service_contract_2023.pdf
├── case_law/
│   ├── supreme_court_case_123.pdf
│   └── circuit_case_456.pdf
└── policies/
    ├── privacy_policy_v2.pdf
    └── terms_of_service.pdf
```

#### 2. Document Quality

- **Resolution:** Ensure PDFs are searchable (OCR if needed)
- **Size:** No strict limit, but <100MB per file recommended
- **Pages:** System handles 1-1000+ pages
- **Scanned Documents:** Use OCR software first (e.g., Adobe Acrobat, Tesseract)

#### 3. OCR for Scanned Documents

```bash
# Install Tesseract OCR
sudo apt install tesseract-ocr

# Install OCRmyPDF
pip install ocrmypdf

# Process scanned PDF
ocrmypdf input_scanned.pdf output_searchable.pdf
```

### Initial Document Load

```bash
# Place all PDFs in legal_documents/
cp /path/to/your/pdfs/*.pdf ./legal_documents/

# Verify documents
ls -lh legal_documents/

# Run Legal RAG (will automatically create vector store)
python legal_rag.py
```

### Adding Documents Later

When adding new documents after initial setup:

```bash
# Option 1: Delete vector store and rebuild
rm -rf legal_vectorstore/
python legal_rag.py

# Option 2: Incremental update (modify legal_rag.py to add update method)
```

---

## Configuration

### Basic Configuration

Edit the configuration at the top of `legal_rag.py`:

```python
# Model Configuration
MODEL_PATH = "./models/llama-2-70b.Q8_0.gguf"
DOCS_PATH = "./legal_documents"
VECTORSTORE_PATH = "./legal_vectorstore"

# LLM Parameters
N_CTX = 4096              # Context window
TEMPERATURE = 0.1         # Low = factual
MAX_TOKENS = 2048         # Max response length

# Chunking Parameters
CHUNK_SIZE = 800          # Optimal for legal docs
CHUNK_OVERLAP = 200       # Preserve context

# Retrieval Parameters
TOP_K_RETRIEVAL = 5       # Chunks to retrieve
SCORE_THRESHOLD = 0.7     # Similarity threshold
```

### Advanced Configuration

#### For Large Documents (500+ pages)

```python
# Increase chunk size for better context
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 300

# Retrieve more chunks
TOP_K_RETRIEVAL = 8
```

#### For Maximum Accuracy

```python
# More conservative retrieval
SCORE_THRESHOLD = 0.8

# Lower temperature (more factual)
TEMPERATURE = 0.05

# Larger context window
N_CTX = 8192  # If model supports
```

#### For Faster Responses

```python
# Smaller context window
N_CTX = 2048

# Fewer chunks
TOP_K_RETRIEVAL = 3

# Lower score threshold (more permissive)
SCORE_THRESHOLD = 0.6
```

---

## Usage Examples

### Example 1: Basic Query

```python
from legal_rag import LegalRAG

# Initialize system
rag = LegalRAG(
    model_path="./models/llama-2-70b.Q8_0.gguf",
    docs_path="./legal_documents"
)

# Ask question
response = rag.query("What are the indemnification clauses?")

# Print results
rag.print_response(response)
```

**Output:**
```
Query: What are the indemnification clauses?
--------------------------------------------------------------------------------

ANSWER:
================================================================================
According to Section 12.3 on page 45, the indemnification clause states:

"Each party shall indemnify, defend, and hold harmless the other party from
and against any and all claims, damages, losses, and expenses arising out of
or resulting from the indemnifying party's breach of this Agreement."

The indemnification obligations survive termination for a period of three (3)
years as specified in Section 15.7.

================================================================================

SOURCES (2 documents):
--------------------------------------------------------------------------------

[1] Page 45 - contract_agreement_2024.pdf
    Section 12.3 INDEMNIFICATION Each party shall indemnify, defend, and
    hold harmless the other party from and against any and all claims...

[2] Page 67 - contract_agreement_2024.pdf
    Section 15.7 SURVIVAL The following provisions shall survive termination:
    representations, warranties, indemnification obligations...

================================================================================
```

### Example 2: Multiple Queries

```python
queries = [
    "What is the termination notice period?",
    "What are the liability limitations?",
    "What governing law applies?",
    "What are the payment terms?"
]

for query in queries:
    print(f"\n{'='*80}")
    print(f"Q: {query}")
    print('='*80)

    response = rag.query(query)
    print(response["answer"])

    if response["sources"]:
        print(f"\nSources: {len(response['sources'])} documents")
        for i, src in enumerate(response["sources"][:2], 1):
            print(f"  [{i}] Page {src['page']}")
```

### Example 3: With Hallucination Detection

```python
response = rag.query("What are the warranty provisions?")

# Check for hallucinations
hallucination_check = rag.detect_hallucination(
    response["answer"],
    response["sources"]
)

if hallucination_check["likely_hallucination"]:
    print("\n⚠️  WARNING: Possible hallucination detected")
    print(f"Confidence: {hallucination_check['confidence']:.1%}")
    print("\nUnsupported claims:")
    for claim in hallucination_check["unsupported_sentences"]:
        print(f"  - {claim}")
    print("\n⚠️  HUMAN REVIEW REQUIRED")
else:
    print("\n✓ Answer appears well-supported by source documents")
```

### Example 4: Batch Processing

```python
import json

# Load questions from file
with open("legal_questions.json", "r") as f:
    questions = json.load(f)

results = []

for q in questions:
    response = rag.query(q["question"])
    results.append({
        "question": q["question"],
        "answer": response["answer"],
        "sources": response["sources"],
        "case_id": q.get("case_id")
    })

# Save results
with open("legal_answers.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Example 5: Interactive Session

```python
#!/usr/bin/env python3
from legal_rag import LegalRAG

def interactive_session():
    rag = LegalRAG(
        model_path="./models/llama-2-70b.Q8_0.gguf",
        docs_path="./legal_documents"
    )

    print("\nLegal RAG Interactive Session")
    print("Type 'quit' or 'exit' to end session\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() in ['quit', 'exit']:
            break

        if not question:
            continue

        try:
            response = rag.query(question)
            rag.print_response(response)
        except Exception as e:
            print(f"Error: {e}")

        print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    interactive_session()
```

---

## Performance Optimization

### CPU Optimization

#### 1. Thread Configuration

```python
# Use all CPU cores
import os
n_threads = os.cpu_count()

llm = LlamaCpp(
    model_path=model_path,
    n_threads=n_threads,
    n_batch=512  # Larger batch = faster processing
)
```

#### 2. Intel-Specific Optimization

```bash
# Enable Intel MKL
pip install intel-extension-for-pytorch

# Set environment variables
export OMP_NUM_THREADS=16
export MKL_NUM_THREADS=16
```

#### 3. AMD-Specific Optimization

```bash
# Enable AMD optimizations
export BLIS_NUM_THREADS=24
export OMP_NUM_THREADS=24
```

### Memory Optimization

#### 1. Reduce Context Window

```python
# Trade context for speed
N_CTX = 2048  # Instead of 4096
```

#### 2. Limit Concurrent Queries

```python
# Process one query at a time
# Avoid parallel processing if RAM limited
```

#### 3. Use Memory-Mapped Files

```python
# Enable in llama.cpp
llm = LlamaCpp(
    model_path=model_path,
    use_mmap=True,  # Memory-map model file
    use_mlock=False  # Don't lock in RAM
)
```

### Storage Optimization

#### 1. Use NVMe SSD

- 5-10× faster than SATA SSD for model loading
- Recommended for vector store persistence

#### 2. RAM Disk for Vector Store (Advanced)

```bash
# Create 10GB RAM disk
sudo mkdir -p /mnt/ramdisk
sudo mount -t tmpfs -o size=10G tmpfs /mnt/ramdisk

# Use for vector store
VECTORSTORE_PATH = "/mnt/ramdisk/legal_vectorstore"
```

### Benchmark Your System

```python
import time

def benchmark():
    rag = LegalRAG(
        model_path="./models/llama-2-70b.Q8_0.gguf",
        docs_path="./legal_documents"
    )

    test_query = "What are the main terms of the agreement?"

    # Warm-up
    _ = rag.query(test_query)

    # Benchmark
    start = time.time()
    response = rag.query(test_query)
    elapsed = time.time() - start

    # Calculate tokens/sec (estimate)
    words = len(response["answer"].split())
    tokens_estimate = words * 1.3  # Rough estimate
    tokens_per_sec = tokens_estimate / elapsed

    print(f"Query time: {elapsed:.2f}s")
    print(f"Response: {words} words (~{tokens_estimate:.0f} tokens)")
    print(f"Speed: {tokens_per_sec:.1f} tokens/sec")

benchmark()
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Out of Memory Error

**Symptoms:**
```
RuntimeError: [Errno 12] Cannot allocate memory
```

**Solutions:**
1. Use a smaller model (13B instead of 70B)
2. Use more aggressive quantization (Q6_K instead of Q8_0)
3. Reduce context window: `N_CTX = 2048`
4. Close other applications
5. Add swap space:

```bash
# Create 32GB swap file
sudo fallocate -l 32G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### Issue 2: Slow Performance

**Symptoms:**
- <1 token/sec
- Long query response times

**Solutions:**
1. Enable CPU optimizations (AVX2/AVX-512)
2. Reduce chunk retrieval: `TOP_K_RETRIEVAL = 3`
3. Use smaller context: `N_CTX = 2048`
4. Increase batch size: `N_BATCH = 1024`
5. Check CPU throttling:

```bash
# Linux: Check CPU frequency
watch -n 1 "cat /proc/cpuinfo | grep MHz"

# Disable CPU throttling (if appropriate)
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

#### Issue 3: Hallucinations

**Symptoms:**
- Answers not supported by documents
- Fabricated citations
- Invented information

**Solutions:**
1. Use Q8_0 quantization (not Q4 or lower)
2. Increase score threshold: `SCORE_THRESHOLD = 0.8`
3. Lower temperature: `TEMPERATURE = 0.05`
4. Enable hallucination detection (see examples)
5. Always verify with source documents
6. Implement human review workflow

#### Issue 4: Poor Retrieval Quality

**Symptoms:**
- Irrelevant chunks retrieved
- Missing relevant information
- Low similarity scores

**Solutions:**
1. Adjust chunk size: Try 600 or 1000
2. Lower score threshold: `SCORE_THRESHOLD = 0.6`
3. Increase retrieval count: `TOP_K_RETRIEVAL = 8`
4. Use better embedding model: `thenlper/gte-large`
5. Rebuild vector store with different chunking

#### Issue 5: Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'langchain'
```

**Solutions:**
1. Activate virtual environment: `source venv/bin/activate`
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python version: `python --version` (need 3.8+)

#### Issue 6: PDF Loading Errors

**Symptoms:**
```
PDFSyntaxError: Invalid PDF
```

**Solutions:**
1. Verify PDF is not corrupted: Open in PDF reader
2. Use OCR if scanned: `ocrmypdf input.pdf output.pdf`
3. Try alternative loader: `pdfplumber` instead of `pypdf`
4. Convert to text first: `pdftotext input.pdf output.txt`

---

## Best Practices

### Legal-Specific Recommendations

#### 1. Accuracy Requirements

- **ALWAYS use Q8_0 or Q6_K quantization**
- **NEVER use Q4 or lower for legal work**
- **ALWAYS verify answers against source documents**
- **ALWAYS implement human review**

#### 2. Source Citation

```python
# Always return and verify sources
response = rag.query(question, return_sources=True)

# Check number of sources
if response["num_sources"] == 0:
    print("⚠️  WARNING: No source documents found")
    print("Answer may not be reliable")
```

#### 3. Audit Trail

```python
# All queries are automatically logged to legal_rag_audit.jsonl
# Review audit log regularly

import json

with open("legal_rag_audit.jsonl", "r") as f:
    for line in f:
        query_record = json.loads(line)
        print(f"[{query_record['timestamp']}] {query_record['question']}")
```

#### 4. Human Review Workflow

```
1. RAG generates answer with sources
   ↓
2. Hallucination detection runs
   ↓
3. If risk detected → Flag for immediate review
   ↓
4. Lawyer reviews answer and sources
   ↓
5. Lawyer approves or corrects answer
   ↓
6. Final answer used in legal work
```

#### 5. Version Control

- Keep audit logs for all queries
- Version control your document corpus
- Track which model version was used
- Maintain document change history

```bash
# Git-based document versioning
git init legal_documents
cd legal_documents
git add *.pdf
git commit -m "Initial document corpus - 2024-02-03"
```

#### 6. Confidentiality

- All processing is local (no external API calls)
- Audit who has access to the system
- Encrypt audit logs if needed
- Consider disk encryption for sensitive documents

```bash
# Encrypt audit log
gpg --symmetric --cipher-algo AES256 legal_rag_audit.jsonl

# Decrypt when needed
gpg --decrypt legal_rag_audit.jsonl.gpg > legal_rag_audit.jsonl
```

### General Best Practices

#### 1. Regular Testing

```python
# Create test suite
test_queries = [
    ("What is the indemnification clause?", "expected_answer_snippet"),
    ("What is the termination period?", "30 days"),
    # Add more test cases
]

for query, expected in test_queries:
    response = rag.query(query)
    if expected.lower() in response["answer"].lower():
        print(f"✓ PASS: {query}")
    else:
        print(f"✗ FAIL: {query}")
```

#### 2. Monitor Performance

```bash
# Log response times
echo "$(date),query_time,5.2s" >> performance_log.csv

# Analyze periodically
python -c "
import pandas as pd
df = pd.read_csv('performance_log.csv', names=['timestamp', 'metric', 'value'])
print(f'Average query time: {df[df.metric==\"query_time\"].value.mean()}')
"
```

#### 3. Document Updates

- Rebuild vector store when documents change
- Keep old vector stores for comparison
- Test with sample queries after updates

#### 4. Model Updates

```bash
# Keep old models for reproducibility
mv models/llama-2-70b.Q8_0.gguf models/archive/llama-2-70b.Q8_0_v1.gguf

# Download new model
# Test thoroughly before deploying

# Rollback if needed
cp models/archive/llama-2-70b.Q8_0_v1.gguf models/llama-2-70b.Q8_0.gguf
```

---

## Additional Resources

### Documentation
- [LangChain Documentation](https://python.langchain.com/)
- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [ChromaDB Documentation](https://docs.trychroma.com/)

### Model Sources
- [TheBloke GGUF Models](https://huggingface.co/TheBloke)
- [HuggingFace Model Hub](https://huggingface.co/models)

### Research Papers
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [Improving Language Models by Retrieving from Trillions of Tokens](https://arxiv.org/abs/2112.04426)

### Legal AI Research
- Stanford CodeX: Legal AI Research
- MIT Computational Law Report

---

## Support and Contributions

This is an open-source project. For issues, improvements, or questions:

1. Check this guide first
2. Review the troubleshooting section
3. Check the audit log for errors
4. Test with a simpler configuration

**Remember:** Legal work requires human oversight. This system is a tool to assist legal professionals, not replace them.

---

## License

MIT License - See LICENSE file for details

---

**Document Version:** 1.0
**Last Updated:** 2024-02-03
**Maintained By:** Claude AI Assistant
