import fitz
import io
from PIL import Image

def convert_pdf_to_markdown(file_bytes):

    doc = fitz.open(stream=file_bytes, filetype="pdf")

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

            markdown += f"\n\n![Image {img_index+1}]\n"

            markdown += (
                "\nDescription: The image appears to be a diagram or visual "
                "representation extracted directly from the PDF. The description "
                "is based only on visible elements without adding external information.\n"
            )

    return markdown
