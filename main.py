from docling.document_converter import DocumentConverter


def main():
    converter = DocumentConverter()
    result = converter.convert("data/fertil_catalog.pdf")
    document = result.document
    text = document.export_to_markdown()
    print(text)


if __name__ == "__main__":
    main()
