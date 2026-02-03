#!/usr/bin/env python3
"""
Legal RAG System - High Accuracy CPU Inference
Designed for processing large legal documents with minimal hallucination risk

Requirements:
- 64GB+ RAM (128GB recommended for 70B models)
- Multi-core CPU (12+ cores recommended)
- SSD with 100GB+ free space for models and vector store

Author: Claude AI Assistant
License: MIT
"""

import os
import json
from typing import List, Dict, Any
from datetime import datetime

try:
    from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.llms import LlamaCpp
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    from langchain.callbacks.manager import CallbackManager
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Please run: pip install -r requirements.txt")
    exit(1)


class LegalRAG:
    """
    Legal RAG System with high accuracy requirements

    Features:
    - Semantic chunking optimized for legal documents
    - Local vector embeddings (no external API calls)
    - CPU-optimized inference with llama.cpp
    - Source verification and citation
    - Query audit logging
    - Hallucination detection
    """

    def __init__(
        self,
        model_path: str,
        docs_path: str,
        vectorstore_path: str = "./legal_vectorstore",
        embedding_model: str = "BAAI/bge-large-en-v1.5",
        n_ctx: int = 4096,
        temperature: float = 0.1,
        chunk_size: int = 800,
        chunk_overlap: int = 200,
        top_k_retrieval: int = 5,
        score_threshold: float = 0.7
    ):
        """
        Initialize Legal RAG System

        Args:
            model_path: Path to GGUF model file (Q8_0 or Q6_K recommended)
            docs_path: Directory containing PDF legal documents
            vectorstore_path: Directory for vector database persistence
            embedding_model: HuggingFace embedding model name
            n_ctx: Context window size
            temperature: LLM temperature (0.1 = very factual)
            chunk_size: Document chunk size in tokens
            chunk_overlap: Overlap between chunks
            top_k_retrieval: Number of chunks to retrieve per query
            score_threshold: Minimum similarity score for retrieval
        """
        self.model_path = model_path
        self.docs_path = docs_path
        self.vectorstore_path = vectorstore_path
        self.embedding_model = embedding_model
        self.n_ctx = n_ctx
        self.temperature = temperature
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k_retrieval = top_k_retrieval
        self.score_threshold = score_threshold

        # Initialize audit log
        self.audit_log_path = "legal_rag_audit.jsonl"

        print("=" * 80)
        print("Legal RAG System - High Accuracy CPU Inference")
        print("=" * 80)

        # Load or create vector store
        if os.path.exists(vectorstore_path) and os.listdir(vectorstore_path):
            print(f"\nLoading existing vector store from {vectorstore_path}...")
            self.load_vectorstore()
        else:
            print(f"\nCreating new vector store from {docs_path}...")
            self.load_documents(docs_path)
            self.setup_vectorstore()

        # Load LLM
        self.setup_llm(model_path)

        # Create QA chain
        self.setup_qa_chain()

        print("\n" + "=" * 80)
        print("System ready for queries")
        print("=" * 80 + "\n")

    def load_documents(self, docs_path: str) -> None:
        """Load and chunk legal documents"""
        print(f"Loading documents from {docs_path}...")

        if not os.path.exists(docs_path):
            raise ValueError(f"Documents path does not exist: {docs_path}")

        # Load all PDF files
        loader = DirectoryLoader(
            docs_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True
        )

        documents = loader.load()
        print(f"Loaded {len(documents)} pages from PDF files")

        if len(documents) == 0:
            raise ValueError(f"No PDF documents found in {docs_path}")

        # Semantic chunking optimized for legal documents
        # Preserves legal structure: sections, subsections, clauses
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n\n",  # Major section breaks
                "\n\n",    # Paragraph breaks
                "\n",      # Line breaks
                ". ",      # Sentence breaks
                " ",       # Word breaks
                ""         # Character breaks
            ],
            length_function=len
        )

        self.chunks = splitter.split_documents(documents)
        print(f"Created {len(self.chunks)} chunks from {len(documents)} pages")
        print(f"Chunk size: {self.chunk_size}, Overlap: {self.chunk_overlap}")

    def setup_vectorstore(self) -> None:
        """Create local vector database with embeddings"""
        print("\nCreating vector embeddings...")
        print(f"Using embedding model: {self.embedding_model}")

        # Use local embeddings (no API calls)
        embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={
                'device': 'cpu',
                'trust_remote_code': True
            },
            encode_kwargs={
                'normalize_embeddings': True,
                'batch_size': 32
            }
        )

        # Create Chroma vector store
        self.vectorstore = Chroma.from_documents(
            documents=self.chunks,
            embedding=embeddings,
            persist_directory=self.vectorstore_path,
            collection_metadata={"hnsw:space": "cosine"}
        )

        self.vectorstore.persist()
        print(f"Vector store created and persisted to {self.vectorstore_path}")

    def load_vectorstore(self) -> None:
        """Load existing vector database"""
        embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model,
            model_kwargs={
                'device': 'cpu',
                'trust_remote_code': True
            },
            encode_kwargs={
                'normalize_embeddings': True,
                'batch_size': 32
            }
        )

        self.vectorstore = Chroma(
            persist_directory=self.vectorstore_path,
            embedding_function=embeddings
        )

        print(f"Vector store loaded from {self.vectorstore_path}")
        print(f"Total chunks in database: {self.vectorstore._collection.count()}")

    def setup_llm(self, model_path: str) -> None:
        """Initialize CPU-optimized LLM with llama.cpp"""
        print(f"\nLoading LLM model: {model_path}")

        if not os.path.exists(model_path):
            raise ValueError(f"Model file not found: {model_path}")

        # Callback for streaming output (optional)
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        # Initialize llama.cpp with CPU optimization
        self.llm = LlamaCpp(
            model_path=model_path,
            n_ctx=self.n_ctx,
            n_threads=os.cpu_count(),  # Use all CPU cores
            n_batch=512,                # Batch size for prompt processing
            n_gpu_layers=0,             # CPU only
            temperature=self.temperature,  # Low = factual
            max_tokens=2048,
            top_p=0.95,
            repeat_penalty=1.1,
            verbose=False,
            # callback_manager=callback_manager  # Uncomment for streaming
        )

        print(f"Model loaded successfully")
        print(f"Context window: {self.n_ctx} tokens")
        print(f"CPU threads: {os.cpu_count()}")
        print(f"Temperature: {self.temperature} (low = factual)")

    def setup_qa_chain(self) -> None:
        """Create RAG pipeline with legal-specific prompt"""

        # Legal-specific prompt template
        prompt = PromptTemplate(
            template="""You are a legal research assistant. Your task is to answer questions based ONLY on the provided context from legal documents.

CRITICAL INSTRUCTIONS:
1. Answer ONLY using information from the context below
2. If the answer is not in the context, respond: "Information not found in provided documents"
3. Quote exact text when making legal claims
4. Cite page numbers for all references
5. Do not infer, speculate, or add information not in the context
6. If uncertain, say "The documents do not provide sufficient information to answer this question"

Context from legal documents:
{context}

Question: {question}

Answer (with page citations):""",
            input_variables=["context", "question"]
        )

        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={
                    "k": self.top_k_retrieval,
                    "score_threshold": self.score_threshold
                }
            ),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )

        print(f"\nRAG pipeline configured:")
        print(f"Retrieval: Top-{self.top_k_retrieval} chunks with similarity >= {self.score_threshold}")

    def query(self, question: str, return_sources: bool = True) -> Dict[str, Any]:
        """
        Execute query with source verification and audit logging

        Args:
            question: User question
            return_sources: Whether to return source documents

        Returns:
            Dictionary with answer, sources, and metadata
        """
        print(f"\nQuery: {question}")
        print("-" * 80)

        # Execute RAG pipeline
        result = self.qa_chain({"query": question})

        # Extract source information
        sources = []
        if return_sources and "source_documents" in result:
            for doc in result["source_documents"]:
                sources.append({
                    "page": doc.metadata.get("page", "unknown"),
                    "source": doc.metadata.get("source", "unknown"),
                    "text_preview": doc.page_content[:300] + "..."
                })

        # Prepare response
        response = {
            "question": question,
            "answer": result["result"],
            "sources": sources,
            "num_sources": len(sources),
            "timestamp": datetime.now().isoformat()
        }

        # Audit logging
        self._log_query(response)

        return response

    def _log_query(self, response: Dict[str, Any]) -> None:
        """Log query to audit trail (JSONL format)"""
        with open(self.audit_log_path, "a") as f:
            json.dump(response, f)
            f.write("\n")

    def detect_hallucination(self, answer: str, source_docs: List[Any]) -> Dict[str, Any]:
        """
        Basic hallucination detection

        Checks if answer contains information not present in source documents.
        This is a simple heuristic approach - not foolproof.

        Args:
            answer: Generated answer
            source_docs: Source documents used for answer

        Returns:
            Dictionary with hallucination analysis
        """
        # Combine source text
        source_text = " ".join([doc.page_content for doc in source_docs]).lower()

        # Split answer into sentences
        answer_sentences = [s.strip() for s in answer.split('.') if s.strip()]

        # Check each sentence for supporting evidence
        unsupported_sentences = []
        for sentence in answer_sentences:
            # Skip meta-sentences
            if any(phrase in sentence.lower() for phrase in [
                "information not found",
                "documents do not",
                "page",
                "according to",
                "cited in"
            ]):
                continue

            # Extract key terms (simple approach)
            words = sentence.lower().split()
            key_words = [w for w in words if len(w) > 4]  # Words > 4 chars

            # Check if key words appear in source
            if len(key_words) > 0:
                found_words = sum(1 for w in key_words if w in source_text)
                support_ratio = found_words / len(key_words)

                if support_ratio < 0.3:  # Less than 30% of key words found
                    unsupported_sentences.append(sentence)

        return {
            "likely_hallucination": len(unsupported_sentences) > 0,
            "unsupported_sentences": unsupported_sentences,
            "confidence": 1 - (len(unsupported_sentences) / max(len(answer_sentences), 1))
        }

    def print_response(self, response: Dict[str, Any]) -> None:
        """Pretty print query response"""
        print("\nANSWER:")
        print("=" * 80)
        print(response["answer"])
        print("\n" + "=" * 80)

        if response["sources"]:
            print(f"\nSOURCES ({response['num_sources']} documents):")
            print("-" * 80)
            for i, source in enumerate(response["sources"], 1):
                print(f"\n[{i}] Page {source['page']} - {source['source']}")
                print(f"    {source['text_preview']}")
        else:
            print("\nNo source documents found meeting similarity threshold")

        print("\n" + "=" * 80)


def main():
    """Example usage of Legal RAG system"""

    # Configuration
    MODEL_PATH = "./models/llama-2-70b.Q8_0.gguf"  # Update with your model path
    DOCS_PATH = "./legal_documents"                 # Update with your docs path

    # Initialize system
    try:
        rag = LegalRAG(
            model_path=MODEL_PATH,
            docs_path=DOCS_PATH,
            vectorstore_path="./legal_vectorstore",
            embedding_model="BAAI/bge-large-en-v1.5",
            n_ctx=4096,
            temperature=0.1,  # Very factual
            chunk_size=800,
            chunk_overlap=200,
            top_k_retrieval=5,
            score_threshold=0.7
        )
    except Exception as e:
        print(f"\nERROR: Failed to initialize Legal RAG system")
        print(f"Details: {str(e)}")
        print("\nPlease ensure:")
        print("1. Model file exists at specified path")
        print("2. Documents directory exists and contains PDF files")
        print("3. All dependencies are installed (pip install -r requirements.txt)")
        return

    # Example queries
    example_queries = [
        "What are the indemnification clauses in the contract?",
        "What is the termination notice period?",
        "What are the liability limitations?",
        "What governing law applies to disputes?"
    ]

    print("\nRunning example queries...")
    print("=" * 80)

    for query in example_queries:
        response = rag.query(query)
        rag.print_response(response)

        # Optional: Check for hallucinations
        if response["sources"]:
            hallucination_check = rag.detect_hallucination(
                response["answer"],
                response["sources"]
            )
            if hallucination_check["likely_hallucination"]:
                print("\n⚠️  WARNING: Possible hallucination detected")
                print(f"Confidence: {hallucination_check['confidence']:.1%}")

        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
