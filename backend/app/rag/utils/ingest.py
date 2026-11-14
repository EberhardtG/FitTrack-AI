import os
import json

from app.rag.config.rag_settings import RAGSettings
from app.rag.utils.file_loader import load_raw_documents
from app.rag.utils.chunker import hybrid_chunk
from app.rag.vectorstore.chroma_store import chroma_store
from app.rag.utils.chunk_quality import ChunkQualityEvaluator

# Instantiate settings once (required for Pydantic v2)
settings = RAGSettings()

# Chunk quality evaluator now uses instance settings
evaluator = ChunkQualityEvaluator()



def ingest():
    print("📥 Starting ingestion...")
    print(f"RAW_DOCS_DIR = {settings.RAW_DOCS_DIR}")

    # Load raw documents using instance settings
    docs = load_raw_documents(settings.RAW_DOCS_DIR)
    

    total_docs = len(docs)
    total_chunks = 0
    all_chunks = []

    print(f"📄 Found {total_docs} documents to ingest.\n")

    for idx, doc in enumerate(docs, start=1):
        print(f"🔎 [{idx}/{total_docs}] Processing: {doc['source']}")

        # Chunk the document
        chunks = hybrid_chunk(doc["text"])
        chunk_count = len(chunks)

        print(f"   ➤ Generated {chunk_count} chunks")

        # Store chunks
        for c in chunks:
            score = evaluator.evaluate(c["text"])

            if score <= 0:
                print(f"   ✖ Filtered low-quality chunk (score={score:.2f})")
                continue

            print(f"   ✔ Accepted chunk (score={score:.2f})")

            chroma_store.add_chunk(c["text"], doc["source"])
            total_chunks += 1

            all_chunks.append({
                "source": doc["source"],
                "text": c["text"],
                "score": score
            })

        # Progress percentage
        percent = round((idx / total_docs) * 100, 1)
        print(f"   ➤ Progress: {percent}% complete\n")

    # Save chunks.json using instance settings
    os.makedirs(settings.PROCESSED_DOCS_DIR, exist_ok=True)

    with open(settings.CHUNKS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print("✅ Ingestion complete!")
    print(f"📦 Total documents processed: {total_docs}")
    print(f"🧩 Total chunks stored: {total_chunks}")
    print(f"📄 chunks.json written to: {settings.CHUNKS_JSON_PATH}")


if __name__ == "__main__":
    ingest()
