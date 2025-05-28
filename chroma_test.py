import os
from chromadb.config import Settings
from chromadb import Client
from chromadb.utils import embedding_functions
from openai import OpenAI

# Load OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI client
client_openai = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Chroma client (local persistence folder: 'chroma_db')
chroma_client = Client(Settings(
    persist_directory="chroma_db",
    chroma_api_impl="local"
))

# Use OpenAI embeddings function via chromadb utils
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-ada-002"
)

# Create (or get) a collection to store newsletter embeddings
collection = chroma_client.get_or_create_collection(
    name="strategy_files_newsletter",
    embedding_function=openai_ef
)

# Sample newsletter content — you’d replace this with your real data
newsletter_texts = [
    {
        "id": "1",
        "text": (
            "Dapper Dan evolved from the underground world to luxury fashion by embracing change. "
            "He studied products in his industry carefully and built a strong team."
        )
    },
    {
        "id": "2",
        "text": (
            "Dan's frameworks help him save time by structuring idea validation and team building. "
            "He validates ideas by talking to potential customers."
        )
    },
]

# Insert data into collection (this stores vectors)
for item in newsletter_texts:
    # Avoid duplicates on rerun by deleting existing id if present
    try:
        collection.delete(ids=[item["id"]])
    except Exception:
        pass

    collection.add(
        documents=[item["text"]],
        ids=[item["id"]]
    )

# Persist collection to disk
chroma_client.persist()

# Simple query example
query = "How did Dapper Dan study products in his industry?"

# Search collection for relevant newsletter chunks
results = collection.query(
    query_texts=[query],
    n_results=2
)

# Extract matched texts from results
matched_texts = results['documents'][0]

# Create prompt for OpenAI GPT
prompt = (
    "You are an expert assistant. Use the following context from a newsletter to answer the question.\n\n"
    f"Context:\n{matched_texts[0]}\n\n"
    f"Question:\n{query}\n\n"
    "Answer:"
)

# Generate answer with GPT-4 (or GPT-3.5 if you prefer)
completion = client_openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)

answer = completion.choices[0].message.content
print("Question:", query)
print("Answer:", answer)

