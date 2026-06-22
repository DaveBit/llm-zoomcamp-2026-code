from gitsource import GithubRepositoryDataReader
import minsearch


#Exercise 1
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
    

print(len(documents))

#Exercise 2
index = minsearch.Index(
    text_fields=["content"],  # Specify the text fields to index
    keyword_fields=["filename"],  # Specify the keyword fields to index
)

index.fit(documents)

results = index.search(
    "How does the agentic loop keep calling the model until it stops?", 
    num_results=5)

print(results[0]["filename"])

#Exercise3

