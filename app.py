import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.title("PDF to Markdown Agent")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

def convert_pdf_to_markdown(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    markdown = ""

    for page_num, page in enumerate(doc):
        markdown += f"\n\n## Page {page_num+1}\n\n"
        
        text = page.get_text()
        markdown += text

        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image = Image.open(io.BytesIO(image_bytes))

            markdown += f"\n\n![Image {img_index+1}](image)\n"

            markdown += "\nImage description: The image is extracted from the PDF and displayed as-is based only on visible content.\n"

    return markdown

if uploaded_file:
    st.success("PDF uploaded successfully!")

    if st.button("Convert to Markdown"):
        md_output = convert_pdf_to_markdown(uploaded_file)

        st.download_button(
            label="Download Markdown",
            data=md_output,
            file_name="output.md",
            mime="text/markdown"
        )
