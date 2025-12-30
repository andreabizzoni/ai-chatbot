from app.services.document_parser import DocumentParser

if __name__ == "__main__":
    parser = DocumentParser()
    chunks = parser.process_document("data/fertil_catalog.pdf")

    print(f"Total chunks created: {len(chunks)}")
    print("First chunk preview:")
    print(f"Content length: {len(chunks[0]['content'])} chars")
    print(f"Metadata: {chunks[0]['metadata']}")
    print(f"\nContent preview: {chunks[0]['content'][:200]}...")
