"""
Script para eliminar y recrear el índice de Pinecone con la dimensión correcta.
"""

from pinecone import Pinecone
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME", "alvgolf-rag")

print("="*60)
print("Pinecone Index Reset")
print("="*60)

# List existing indexes
existing_indexes = pc.list_indexes().names()
print(f"Existing indexes: {existing_indexes}")

# Delete if exists
if index_name in existing_indexes:
    print(f"[INFO] Deleting index: {index_name}")
    pc.delete_index(index_name)
    print(f"[OK] Index deleted: {index_name}")
else:
    print(f"[INFO] Index does not exist: {index_name}")

print("="*60)
print("[OK] Ready to recreate index with correct dimension")
print("     Start backend to create index with dimension=1024")
print("="*60)
