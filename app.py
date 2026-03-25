import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

# Page title
st.title("PDF to Markdown Agent")

st.write(
    "Upload a PDF file and this agent will convert the content into Markdown format."
)

# File uploader (this ensures upload UI is always visible)
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])


def convert_pdf_to_markdown(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    markdown = "# Converted PDF Document\n\n"

    for page_num, page in enumerate(doc):
        markdown += f"\n\n## Page {page_num + 1}\n\n"

        # Extract text
        text = page.get_text()
        markdown += text + "\n"

        # Extract images
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # Load image
            image = Image.open(io.BytesIO(image_bytes))

            markdown += f"\n\n### Image {img_index + 1}\n"
            markdown += f"![Image](image_{page_num}_{img_index}.png)\n"

            markdown += (
                "\nDescription: The image extracted from the PDF is shown here. "
                "The description is limited to visible elements without adding external information.\n"
            )

    return markdown


# When a file is uploaded
if uploaded_file is not None:

    st.success("PDF uploaded successfully!")

    if st.button("Convert to Markdown"):

        with st.spinner("Processing PDF..."):
            md_output = convert_pdf_to_markdown(uploaded_file)

        st.success("Conversion complete!")

        # Show preview
        st.subheader("Markdown Preview")
        st.text(md_output[:2000])  # preview first part

        # Download button
        st.download_button(
            label="Download Markdown File",
            data=md_output,
            file_name="converted_document.md",
            mime="text/markdown",
        )

else:
    st.info("Please upload a PDF file to begin.")
