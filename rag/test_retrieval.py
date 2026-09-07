from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


CHROMA_PATH = "chroma_db"


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
    collection_name="bridge_inspections",
)

query = "What is the condition of the bridge deck?"

results = vectorstore.similarity_search_with_score(
    query,
    k=3
)

print("\nQUERY:")
print(query)

print("\nTOP RETRIEVED EVIDENCE:\n")

for i, (doc, score) in enumerate(results, start=1):

    print(f"========== RESULT {i} ==========")
    print(f"Similarity score: {score}")
    print(f"Page: {doc.metadata.get('page')}")
    print(f"Bridge: {doc.metadata.get('bridge')}")
    print("\nText:")
    print(doc.page_content[:1500])
    print()