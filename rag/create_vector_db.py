from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings



DATA_DIR = Path("data")
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "bridge_inspections"


def load_all_pdfs():
    documents = []

    pdf_files = list(DATA_DIR.glob("*/**/*.pdf"))

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_path in pdf_files:
        bridge_id = pdf_path.parent.name

        print(f"Reading: {pdf_path}")

        try:
            reader = PdfReader(str(pdf_path))

            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""

                if text.strip():
                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": str(pdf_path),
                                "page": page_number,
                                "bridge": bridge_id,
                            },
                        )
                    )

        except Exception as e:
            print(f"ERROR reading {pdf_path}: {e}")

    return documents, pdf_files



documents, pdf_files = load_all_pdfs()

print(f"Pages with text: {len(documents)}")



splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)

chunks = splitter.split_documents(documents)

print(f"Total chunks created: {len(chunks)}")



print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



print("Creating Chroma database...")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_PATH,
    collection_name=COLLECTION_NAME,
)


print("\n========================================")
print("Chroma database created successfully.")
print("========================================")
print(f"PDF files processed : {len(pdf_files)}")
print(f"Pages with text     : {len(documents)}")
print(f"Chunks stored       : {len(chunks)}")
print(f"Database location   : {CHROMA_PATH}")
print("========================================")