"""
Legal RAG Configuration Example

Copy this file to config.py and adjust settings for your specific setup.
"""

# ==============================================================================
# MODEL CONFIGURATION
# ==============================================================================

# Path to your GGUF model file
# Recommended: Q8_0 or Q6_K quantization for legal work
MODEL_PATH = "./models/llama-2-70b.Q8_0.gguf"

# Directory containing your PDF legal documents
DOCS_PATH = "./legal_documents"

# Directory for vector database persistence
VECTORSTORE_PATH = "./legal_vectorstore"

# ==============================================================================
# EMBEDDING CONFIGURATION
# ==============================================================================

# HuggingFace embedding model
# Options:
#   - "BAAI/bge-large-en-v1.5" (recommended, 1.3GB)
#   - "thenlper/gte-large" (alternative, 1.4GB)
#   - "sentence-transformers/all-mpnet-base-v2" (smaller, 420MB)
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"

# ==============================================================================
# LLM PARAMETERS
# ==============================================================================

# Context window size (tokens)
# Larger = more context, but slower and more RAM
# Options: 2048, 4096, 8192 (if model supports)
N_CTX = 4096

# Temperature (0.0 = deterministic, 1.0 = creative)
# For legal work: use 0.1 or lower for maximum factuality
TEMPERATURE = 0.1

# Maximum tokens in response
# Typical legal answers: 200-500 tokens
# Longer documents: 1000-2000 tokens
MAX_TOKENS = 2048

# Top-p sampling (nucleus sampling)
# Keep at 0.95 for balanced outputs
TOP_P = 0.95

# Repeat penalty (1.0 = no penalty, 1.1 = slight penalty)
# Reduces repetitive text
REPEAT_PENALTY = 1.1

# ==============================================================================
# DOCUMENT CHUNKING PARAMETERS
# ==============================================================================

# Chunk size in characters
# Optimal for legal documents: 600-1000
# Smaller chunks = more precise retrieval but may lose context
# Larger chunks = better context but less precise
CHUNK_SIZE = 800

# Overlap between chunks in characters
# Recommended: 20-30% of chunk size
# Ensures legal context isn't split across boundaries
CHUNK_OVERLAP = 200

# ==============================================================================
# RETRIEVAL PARAMETERS
# ==============================================================================

# Number of document chunks to retrieve per query
# More chunks = better context but slower
# Legal work: 5-8 recommended
TOP_K_RETRIEVAL = 5

# Minimum similarity score threshold (0.0-1.0)
# Higher = more strict, only highly relevant chunks
# Lower = more permissive, may include less relevant chunks
# Legal work: 0.7-0.8 recommended
SCORE_THRESHOLD = 0.7

# ==============================================================================
# PERFORMANCE TUNING
# ==============================================================================

# Number of CPU threads to use
# Set to None to use all available cores (recommended)
# Or specify: N_THREADS = 16
N_THREADS = None

# Batch size for prompt processing
# Larger = faster processing but more RAM
# Typical: 256-512 for most systems, 1024 for high-end
N_BATCH = 512

# GPU layers (0 = CPU only)
# Keep at 0 for CPU-only inference
N_GPU_LAYERS = 0

# ==============================================================================
# MEMORY OPTIMIZATION
# ==============================================================================

# Use memory mapping for model file
# Recommended: True (faster startup, less RAM usage)
USE_MMAP = True

# Lock model in RAM (prevents swapping)
# Set to True if you have enough RAM and want maximum speed
# Set to False if RAM limited
USE_MLOCK = False

# ==============================================================================
# AUDIT AND LOGGING
# ==============================================================================

# Path to audit log (JSONL format)
# All queries and responses are logged here
AUDIT_LOG_PATH = "./legal_rag_audit.jsonl"

# Enable verbose logging
# Set to True for debugging
VERBOSE = False

# ==============================================================================
# CONFIGURATION PRESETS
# ==============================================================================

# Uncomment one of these presets or customize above

# ---- MAXIMUM ACCURACY (Slow, High RAM) ----
# MODEL_PATH = "./models/llama-2-70b.Q8_0.gguf"
# N_CTX = 8192
# TEMPERATURE = 0.05
# CHUNK_SIZE = 1000
# CHUNK_OVERLAP = 300
# TOP_K_RETRIEVAL = 8
# SCORE_THRESHOLD = 0.8

# ---- BALANCED (Recommended for most users) ----
# MODEL_PATH = "./models/llama-2-70b.Q8_0.gguf"
# N_CTX = 4096
# TEMPERATURE = 0.1
# CHUNK_SIZE = 800
# CHUNK_OVERLAP = 200
# TOP_K_RETRIEVAL = 5
# SCORE_THRESHOLD = 0.7

# ---- FAST (Lower accuracy, less RAM) ----
# MODEL_PATH = "./models/llama-2-13b.Q6_K.gguf"
# N_CTX = 2048
# TEMPERATURE = 0.15
# CHUNK_SIZE = 600
# CHUNK_OVERLAP = 150
# TOP_K_RETRIEVAL = 3
# SCORE_THRESHOLD = 0.6

# ---- MINIMUM SYSTEM (32GB RAM) ----
# MODEL_PATH = "./models/mistral-7b.Q8_0.gguf"
# N_CTX = 2048
# TEMPERATURE = 0.1
# CHUNK_SIZE = 600
# CHUNK_OVERLAP = 150
# TOP_K_RETRIEVAL = 3
# SCORE_THRESHOLD = 0.7

# ==============================================================================
# USAGE EXAMPLE
# ==============================================================================

"""
To use this configuration:

1. Copy this file:
   cp config_example.py config.py

2. Edit config.py with your settings

3. Import in your code:
   from config import *

   rag = LegalRAG(
       model_path=MODEL_PATH,
       docs_path=DOCS_PATH,
       n_ctx=N_CTX,
       temperature=TEMPERATURE,
       # ... other parameters
   )
"""
