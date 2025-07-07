from docling.document_converter import DocumentConverter

converter = DocumentConverter()

link = 'https://silvestrecode.shop/'
result = converter.convert(link)
print(result.document.export_to_markdown())



