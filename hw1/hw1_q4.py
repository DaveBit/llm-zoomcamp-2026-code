from gitsource import GithubRepositoryDataReader
import minsearch
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env
load_dotenv(".env")

# Create OpenAI client

print(os.getenv("OPENAI_API_KEY") is not None)  # should print True

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# Step 1: Load lesson documents
# -----------------------------
reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)

files = reader.read()

documents = []
for file in files:
    doc = file.parse()
    documents.append(doc)

print(f"Loaded {len(documents)} documents")

# -----------------------------
# Step 2: Build minsearch index
# -----------------------------
index = minsearch.Index(
    text_fields=["content"],
    keyword_fields=["filename"],
)

index.fit(documents)

# -----------------------------
# Step 3: Search helper
# -----------------------------
def search(question):
    return index.search(question, num_results=5)

# -----------------------------
# Step 4: Define the question
# -----------------------------
question = "How does the agentic loop keep calling the model until it stops?"

# -----------------------------
# Step 5: Retrieve documents
# -----------------------------
results = search(question)

print("\nTop result filenames:")
for doc in results:
    print(doc["filename"])

# -----------------------------
# Step 6: Build context
# -----------------------------
context = "\n\n".join([
    f"FILENAME: {doc['filename']}\n{doc['content']}"
    for doc in results
])

# -----------------------------
# Step 7: Build prompt
# -----------------------------
prompt = f"""
You are a course teaching assistant.
Answer the question based only on the context below.

Context:
{context}

Question:
{question}

Answer:
""".strip()

# Optional debug
# print(prompt[:2000])

# -----------------------------
# Step 8: Call the model
# -----------------------------
response = openai_client.responses.create(
    model="gpt-5.4-mini",
    input=prompt
)

# -----------------------------
# Step 9: Print outputs
# -----------------------------
print("\nMODEL ANSWER:\n")
print(response.output_text)

print("\nUSAGE:\n")
print(response.usage)

print("\nINPUT TOKENS:\n")
print(response.usage.input_tokens)