import chromadb
from chromadb.config import Settings
from rag.loader import load_forecast_data
import os

_client = None

def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path="./chroma_db"
        )
    return _client

def store_to_chroma():
    client = get_client()
    collection = client.get_or_create_collection(name="weather")
    docs = load_forecast_data()

    collection.add(
        documents=[doc["text"] for doc in docs],
        metadatas=[{"province": doc["province"], "region": doc["region"]} for doc in docs],
        ids=[doc["id"] for doc in docs]
    )

    print(f"📦 เก็บ {len(docs)} เอกสารแล้วใน ChromaDB")
    print("Path chroma_db exists?", os.path.exists("./chroma_db"))