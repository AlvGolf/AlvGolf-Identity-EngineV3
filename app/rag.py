"""
AlvGolf Agentic Analytics Engine - RAG Core

Retrieval-Augmented Generation using Pinecone + Claude.

Since we're using Python 3.14, we use Pinecone's embeddings API
instead of local HuggingFace models (to avoid numpy/torch compilation issues).
"""

from typing import List
from pinecone import Pinecone, ServerlessSpec
from langchain_anthropic import ChatAnthropic
from app.config import settings
from app.models import ShotData
import time


# ============ Initialize Pinecone ============

pc = Pinecone(api_key=settings.pinecone_api_key)

# Check if index exists, create if not
index_name = settings.pinecone_index_name

if index_name not in pc.list_indexes().names():
    print(f"[INFO] Creating Pinecone index: {index_name}")
    pc.create_index(
        name=index_name,
        dimension=1024,  # multilingual-e5-large dimension
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
    # Wait for index to be ready
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
    print(f"[OK] Index {index_name} created and ready")
else:
    print(f"[OK] Using existing index: {index_name}")

index = pc.Index(index_name)


# ============ Initialize Claude ============

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    anthropic_api_key=settings.anthropic_api_key,
    temperature=0.1,
    max_tokens=2000
)


# ============ Helper Functions ============

def _shot_to_text(user_id: str, shot: ShotData) -> str:
    """
    Convert ShotData to text for vectorization.

    Format is optimized for semantic search.
    """
    return (
        f"User: {user_id} | Date: {shot.date} | Source: {shot.source} | "
        f"Club: {shot.club} | Hole: {shot.hole} | "
        f"BallSpeed: {shot.ball_speed} km/h | Carry: {shot.carry}m | "
        f"LaunchAngle: {shot.launch_angle} deg | FaceToPath: {shot.face_to_path} deg | "
        f"Score: {shot.score} | Notes: {shot.notes}"
    )


def _embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings using Pinecone's embeddings API.

    Batches requests in chunks of 96 (Pinecone API limit).

    Args:
        texts: List of texts to embed

    Returns:
        List of embedding vectors
    """
    BATCH_SIZE = 96
    all_embeddings = []

    # Process in batches
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        print(f"[INFO] Embedding batch {i//BATCH_SIZE + 1} ({len(batch)} texts)...")

        # Use Pinecone's embed API
        embeddings = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=batch,
            parameters={"input_type": "passage"}
        )

        all_embeddings.extend([e['values'] for e in embeddings])

    return all_embeddings


# ============ Public Functions ============

def ingest_shots(user_id: str, shots: List[ShotData]) -> int:
    """
    Ingest shots to Pinecone vector database.

    Args:
        user_id: User ID (used as namespace)
        shots: List of ShotData objects

    Returns:
        Number of chunks ingested
    """
    # Convert shots to texts
    texts = [_shot_to_text(user_id, s) for s in shots]

    # Generate embeddings
    print(f"[INFO] Generating embeddings for {len(texts)} shots...")
    embeddings = _embed_texts(texts)

    # Prepare vectors for Pinecone
    vectors = []
    for i, (text, embedding) in enumerate(zip(texts, embeddings)):
        shot = shots[i]
        vectors.append({
            "id": f"{user_id}_{shot.date}_{shot.club}_{i}",
            "values": embedding,
            "metadata": {
                "user_id": user_id,
                "date": shot.date,
                "source": shot.source,
                "club": shot.club,
                "text": text
            }
        })

    # Upsert to Pinecone with namespace
    print(f"[INFO] Upserting {len(vectors)} vectors to Pinecone...")
    index.upsert(
        vectors=vectors,
        namespace=user_id
    )

    print(f"[OK] Ingested {len(vectors)} shots for user {user_id}")
    return len(vectors)


def rag_answer(user_id: str, prompt: str, top_k: int = 5) -> str:
    """
    Answer question using RAG (Retrieval-Augmented Generation).

    Process:
    1. Embed the question
    2. Search similar vectors in Pinecone
    3. Retrieve top-k most relevant documents
    4. Send context + question to Claude
    5. Return answer

    Args:
        user_id: User ID (namespace)
        prompt: Question to answer
        top_k: Number of documents to retrieve

    Returns:
        Answer from Claude
    """
    # Embed the question
    question_embedding = _embed_texts([prompt])[0]

    # Search in Pinecone
    results = index.query(
        vector=question_embedding,
        top_k=top_k,
        namespace=user_id,
        include_metadata=True
    )

    # Extract context from results
    if not results['matches']:
        return "No data found for this user. Please ingest data first."

    context_docs = [match['metadata']['text'] for match in results['matches']]
    context = "\n".join(context_docs)

    # Build prompt for Claude
    full_prompt = f"""You are a professional golf analyst for AlvGolf.

Relevant data from the player's history:
{context}

Player's question:
{prompt}

Provide a technical analysis based on the data above. Be specific with numbers and patterns.
"""

    # Invoke Claude
    response = llm.invoke(full_prompt)

    return response.content


# ============ Testing ============

if __name__ == "__main__":
    print("Testing RAG Core...")
    print(f"Index: {index_name}")
    print(f"Index stats: {index.describe_index_stats()}")
    print("[OK] RAG Core ready")
