#!/bin/bash
# Legal RAG System - Automated Setup Script
# This script automates the installation and configuration of the Legal RAG system

set -e  # Exit on error

echo "=========================================="
echo "Legal RAG System - Setup"
echo "=========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
print_status "Found Python $PYTHON_VERSION"

if [ "$(echo "$PYTHON_VERSION < 3.8" | bc)" -eq 1 ]; then
    print_error "Python 3.8 or higher is required"
    exit 1
fi

# Check system resources
echo ""
echo "Checking system resources..."
TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
print_status "Total RAM: ${TOTAL_RAM}GB"

if [ "$TOTAL_RAM" -lt 32 ]; then
    print_warning "Less than 32GB RAM detected. Legal RAG requires at least 64GB for optimal performance."
    print_warning "You may experience slowdowns or out-of-memory errors with large models."
fi

CPU_CORES=$(nproc)
print_status "CPU cores: $CPU_CORES"

# Create directories
echo ""
echo "Creating directories..."
mkdir -p models
mkdir -p legal_documents
mkdir -p legal_vectorstore
print_status "Directories created"

# Check if virtual environment exists
echo ""
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        print_status "Removed existing virtual environment"
    else
        print_status "Using existing virtual environment"
    fi
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel
print_status "pip upgraded"

# Detect CPU architecture for optimized llama.cpp
echo ""
echo "Detecting CPU architecture for optimization..."
if [[ $(uname -m) == "arm64" ]] || [[ $(uname -m) == "aarch64" ]]; then
    print_status "ARM64 architecture detected (Apple Silicon or ARM)"
    export CMAKE_ARGS="-DLLAMA_METAL=on"
    print_status "Will build llama-cpp-python with Metal support"
elif grep -q avx512 /proc/cpuinfo 2>/dev/null; then
    print_status "Intel CPU with AVX-512 detected"
    export CMAKE_ARGS="-DLLAMA_AVX512=on"
    print_status "Will build llama-cpp-python with AVX-512 support"
elif grep -q avx2 /proc/cpuinfo 2>/dev/null; then
    print_status "CPU with AVX2 detected"
    export CMAKE_ARGS="-DLLAMA_AVX2=on"
    print_status "Will build llama-cpp-python with AVX2 support"
else
    print_warning "No advanced CPU features detected, using default build"
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
echo "This may take several minutes..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_status "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Download embedding model (optional but recommended)
echo ""
read -p "Do you want to download the embedding model now? (~1.3GB) (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Downloading BAAI/bge-large-en-v1.5 embedding model..."
    python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-large-en-v1.5')"
    print_status "Embedding model downloaded"
else
    print_warning "Skipping embedding model download. It will be downloaded on first use."
fi

# Check for model file
echo ""
echo "Checking for LLM model..."
if ls models/*.gguf 1> /dev/null 2>&1; then
    MODEL_FILE=$(ls models/*.gguf | head -n 1)
    print_status "Found model: $MODEL_FILE"
else
    print_warning "No GGUF model found in ./models/ directory"
    echo ""
    echo "You need to download a quantized GGUF model."
    echo "Recommended models for legal work (Q8_0 or Q6_K quantization):"
    echo ""
    echo "  • LLaMA 2 70B Q8_0 (~70GB) - Best accuracy"
    echo "    https://huggingface.co/TheBloke/Llama-2-70B-GGUF"
    echo ""
    echo "  • LLaMA 2 13B Q8_0 (~14GB) - Good for 64GB RAM systems"
    echo "    https://huggingface.co/TheBloke/Llama-2-13B-GGUF"
    echo ""
    echo "  • Mistral 7B Q8_0 (~8GB) - Minimum recommended"
    echo "    https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF"
    echo ""
    echo "Download instructions:"
    echo "  1. Visit the HuggingFace link above"
    echo "  2. Download a *Q8_0.gguf or *Q6_K.gguf file"
    echo "  3. Place it in the ./models/ directory"
    echo ""
fi

# Check for legal documents
echo ""
echo "Checking for legal documents..."
if ls legal_documents/*.pdf 1> /dev/null 2>&1; then
    DOC_COUNT=$(ls legal_documents/*.pdf | wc -l)
    print_status "Found $DOC_COUNT PDF documents"
else
    print_warning "No PDF documents found in ./legal_documents/ directory"
    echo ""
    echo "Please add your legal PDF documents to the ./legal_documents/ directory"
    echo ""
fi

# Create example configuration
echo ""
echo "Creating example configuration..."
cat > config_example.py << 'EOF'
# Legal RAG Configuration Example
# Copy this to config.py and adjust for your setup

# Model Configuration
MODEL_PATH = "./models/llama-2-70b.Q8_0.gguf"  # Update with your model
DOCS_PATH = "./legal_documents"
VECTORSTORE_PATH = "./legal_vectorstore"

# Embedding Configuration
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"

# LLM Parameters
N_CTX = 4096          # Context window size
TEMPERATURE = 0.1     # Low = factual (0.0-0.3 for legal work)
MAX_TOKENS = 2048     # Maximum response length

# Chunking Parameters
CHUNK_SIZE = 800      # Tokens per chunk (optimized for legal docs)
CHUNK_OVERLAP = 200   # Overlap between chunks

# Retrieval Parameters
TOP_K_RETRIEVAL = 5        # Number of chunks to retrieve
SCORE_THRESHOLD = 0.7      # Minimum similarity score (0.0-1.0)

# Hardware Optimization
# These are auto-detected, but you can override:
# N_THREADS = 16      # CPU threads (default: all cores)
# N_BATCH = 512       # Batch size for prompt processing
EOF
print_status "Created config_example.py"

# Create simple test script
echo ""
echo "Creating test script..."
cat > test_system.py << 'EOF'
#!/usr/bin/env python3
"""Quick system test for Legal RAG"""
import os
import sys

print("Testing Legal RAG System Dependencies...\n")

# Test imports
try:
    import langchain
    print("✓ LangChain imported")
except ImportError as e:
    print(f"✗ LangChain import failed: {e}")
    sys.exit(1)

try:
    from langchain_community.llms import LlamaCpp
    print("✓ LlamaCpp imported")
except ImportError as e:
    print(f"✗ LlamaCpp import failed: {e}")
    sys.exit(1)

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    print("✓ HuggingFaceEmbeddings imported")
except ImportError as e:
    print(f"✗ HuggingFaceEmbeddings import failed: {e}")
    sys.exit(1)

try:
    from langchain_community.vectorstores import Chroma
    print("✓ Chroma imported")
except ImportError as e:
    print(f"✗ Chroma import failed: {e}")
    sys.exit(1)

try:
    from langchain_community.document_loaders import PyPDFLoader
    print("✓ PyPDFLoader imported")
except ImportError as e:
    print(f"✗ PyPDFLoader import failed: {e}")
    sys.exit(1)

print("\n✓ All dependencies OK")

# Check directories
print("\nChecking directories...")
for dir_path in ["models", "legal_documents", "legal_vectorstore"]:
    if os.path.exists(dir_path):
        print(f"✓ {dir_path}/ exists")
    else:
        print(f"✗ {dir_path}/ missing")

# Check for model
print("\nChecking for GGUF model...")
if os.path.exists("models") and any(f.endswith('.gguf') for f in os.listdir("models")):
    models = [f for f in os.listdir("models") if f.endswith('.gguf')]
    print(f"✓ Found {len(models)} GGUF model(s):")
    for m in models:
        size_gb = os.path.getsize(f"models/{m}") / (1024**3)
        print(f"  - {m} ({size_gb:.1f} GB)")
else:
    print("✗ No GGUF models found in models/")

# Check for documents
print("\nChecking for PDF documents...")
if os.path.exists("legal_documents") and any(f.endswith('.pdf') for f in os.listdir("legal_documents")):
    pdfs = [f for f in os.listdir("legal_documents") if f.endswith('.pdf')]
    print(f"✓ Found {len(pdfs)} PDF document(s)")
else:
    print("✗ No PDF documents found in legal_documents/")

print("\n" + "="*50)
print("System check complete!")
print("="*50)
EOF

chmod +x test_system.py
print_status "Created test_system.py"

# Final summary
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Download a GGUF model (Q8_0 or Q6_K recommended):"
echo "   - LLaMA 2 70B Q8_0 for best accuracy"
echo "   - LLaMA 2 13B Q8_0 for 64GB RAM systems"
echo "   - Place in ./models/ directory"
echo ""
echo "2. Add your PDF documents to ./legal_documents/"
echo ""
echo "3. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "4. Test the system:"
echo "   python test_system.py"
echo ""
echo "5. Run the Legal RAG system:"
echo "   python legal_rag.py"
echo ""
echo "For detailed instructions, see LEGAL_AI_SETUP_GUIDE.md"
echo ""
