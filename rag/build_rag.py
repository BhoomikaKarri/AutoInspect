from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


PDF_PATH = Path(
    "data/BridgeInspRpt-PUTNEY-00001/BridgeInspRpt-PUTNEY-00001.pdf"
)


def load_pdf():
    reader = PdfReader(str(PDF_PATH))

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": str(PDF_PATH),
                        "page": page_number,
                        "bridge": "PUTNEY-00001",
                    },
                )
            )

    return documents


documents = load_pdf()

print(f"Pages with text: {len(documents)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
)

chunks = splitter.split_documents(documents)

print(f"Total chunks created: {len(chunks)}")

print("\n--- FIRST CHUNK ---\n")
print(chunks[0].page_content)

print("\n--- METADATA ---")
print(chunks[0].metadata)