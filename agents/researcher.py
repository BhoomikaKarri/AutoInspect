from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "bridge_inspections"


def get_retriever(bridge_name=None):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )

    search_kwargs = {"k": 5}

    if bridge_name:
        search_kwargs["filter"] = {"bridge": bridge_name}

    return vectorstore.as_retriever(
        search_kwargs=search_kwargs
    )


def research(question: str, bridge_name=None):
    retriever = get_retriever(bridge_name)

    documents = retriever.invoke(question)

    results = []

    for doc in documents:
        results.append(
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "bridge": doc.metadata.get("bridge"),
            }
        )

    return results


if __name__ == "__main__":
    question = input("Enter inspection question: ")
    bridge = input("Enter bridge name (or press Enter for all bridges): ").strip()

    bridge = bridge if bridge else None

    results = research(question, bridge)

    print("\n==============================")
    print("RESEARCHER AGENT RESULTS")
    print("==============================")

    for i, result in enumerate(results, start=1):
        print(f"\n--- Evidence {i} ---")
        print(f"Bridge: {result['bridge']}")
        print(f"Page: {result['page']}")
        print(f"Source: {result['source']}")
        print("\n" + result["content"])