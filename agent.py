from pdf_to_markdown_tool import convert_pdf_to_markdown

class PDFMarkdownAgent:

    def run(self, file_bytes):
        result = convert_pdf_to_markdown(file_bytes)
        return result
