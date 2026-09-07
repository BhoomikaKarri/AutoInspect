from pypdf import PdfReader

PDF_PATH = "data/BridgeInspRpt-PUTNEY-00001/BridgeInspRpt-PUTNEY-00001.pdf"

reader = PdfReader(PDF_PATH)

print(f"Total pages: {len(reader.pages)}")

for i, page in enumerate(reader.pages[:3]):
    text = page.extract_text() or ""

    print(f"\n--- PAGE {i + 1} ---\n")
    print(text[:2000])