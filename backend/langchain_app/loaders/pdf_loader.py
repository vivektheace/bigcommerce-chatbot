import os
import fitz  # PyMuPDF
import json
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_and_images(pdf_path: str, output_dir: str) -> None:
    """
    Extracts text and images from a PDF, saves them to structured output.

    Args:
        pdf_path (str): Path to the PDF file.
        output_dir (str): Folder to save processed chunks and images.
    """
    doc = fitz.open(pdf_path)
    product_name = os.path.splitext(os.path.basename(pdf_path))[0]
    product_dir = os.path.join(output_dir, product_name)
    images_dir = os.path.join(product_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    chunks: List[Dict] = []
    img_count = 0
    chunk_index = 0

    logger.info(f"📄 Processing {product_name}...")

    for page_num, page in enumerate(doc):
        text_blocks = page.get_text("blocks")

        # Extract text blocks
        for block in text_blocks:
            text = block[4].strip()
            if text:
                chunks.append({
                    "chunk_id": f"{product_name}_chunk_{chunk_index}",
                    "chunk_type": "text",
                    "page_number": page_num + 1,
                    "content": text,
                    "metadata": {
                        "source": product_name,
                        "type": "manual"
                    }
                })
                chunk_index += 1

        # Extract images
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"img_{img_count}.{image_ext}"
            image_path = os.path.join(images_dir, image_filename)

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            chunks.append({
                "chunk_id": f"{product_name}_image_caption_{img_count}",
                "chunk_type": "image_caption",
                "page_number": page_num + 1,
                "content": f"Image extracted from page {page_num + 1}",
                "image_path": image_path,
                "metadata": {
                    "source": product_name,
                    "type": "image"
                }
            })

            img_count += 1

    # Save chunks to JSON
    chunks_path = os.path.join(product_dir, "chunks.json")
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    logger.info(f" Finished: {product_name} → {len(chunks)} chunks, {img_count} images extracted.")

def batch_process_pdfs(input_folder: str, output_folder: str) -> None:
    """
    Processes all PDFs in a folder and extracts content to structured format.

    Args:
        input_folder (str): Folder containing raw PDF manuals.
        output_folder (str): Folder to store processed data.
    """
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
    if not pdf_files:
        logger.warning(" No PDF files found.")
        return

    for pdf in pdf_files:
        extract_text_and_images(os.path.join(input_folder, pdf), output_folder)


if __name__ == "__main__":
    # Example usage
    input_path = "D:/bigcommerce-chatbot/data/manuals"
    output_path = "D:/bigcommerce-chatbot/data/processed_manuals"

    batch_process_pdfs(input_path, output_path)

