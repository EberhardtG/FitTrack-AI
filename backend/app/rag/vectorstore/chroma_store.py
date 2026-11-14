import chromadb
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from app.rag.config.rag_settings import RAGSettings

# Instantiate settings once 
settings = RAGSettings()




class ChromaStore:
    def __init__(self):
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

        # NEW ChromaDB client 
        self.client = PersistentClient(path=settings.CHROMA_PATH)

        # Create or load collection
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )


    def embed(self, text: str):
        return self.embedding_model.encode(text).tolist()

    def add_chunk(self, text: str, source: str, metadata: dict = None):
        """
        Add a chunk to ChromaDB.
        """
        if metadata is None:
            metadata = {"source": source}

        chunk_id = f"{source}-{hash(text)}"
        embedding = self.embed(text)

        self.collection.add(
            ids=[chunk_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata]
        )


    def query(self, query_text: str, top_k: int = None):
        if top_k is None:
            top_k = settings.MAX_CONTEXT_CHUNKS

        query_embedding = self.embed(query_text)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        formatted = []
        for doc, meta, score in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            formatted.append({
                "text": doc,
                "metadata": meta,
                "score": score
            })

        return formatted


# Singleton instance
chroma_store = ChromaStore()
