import os
from openpyxl import load_workbook
import re
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import fitz  # PyMuPDF
import re
import docx2txt
from docx import Document



def extract_text_from_image(file_path):
    """Extract text from image using Tesseract OCR"""
    try:
        with Image.open(file_path) as img:
            text = pytesseract.image_to_string(img, lang='fra')
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def is_pdf_scanned(file_path):
    """Check if a PDF file is scanned or not by checking if the first page is empty or not"""
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        if len(pdf_reader.pages) > 0:
            # Traitement de la première page seulement
            page = pdf_reader.pages[0]
            page_text = page.extract_text()
            return not page_text.strip()
    return False

def extract_text_from_pdf(file_path):
    """Extract text from PDF using PyMuPDF library"""
    text = ''
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            text += page_text
            text = re.sub(r'\s+', ' ', text)

    return text

def extract_text_from_pdf_ocr(file_path):
    """Extract text from scanned PDF using Tesseract OCR"""
    document = fitz.open(file_path)
    text = []

    # Process the first 6 pages only
    for page_num in range(min(6, document.page_count)):
        current_page = document.load_page(page_num)
        resolution = 300
        image = current_page.get_pixmap(matrix=fitz.Matrix(resolution / 72, resolution / 72))

        temp_image_path = f"Images\\temp_image_page_{page_num}.png"
        image_pil = Image.frombytes("RGB", [image.width, image.height], image.samples)
        image_pil.save(temp_image_path)

        page_text = pytesseract.image_to_string(Image.open(temp_image_path))
        page_text = re.sub(r'\s+', ' ', page_text)
        text.append(page_text)

    document.close()
    text = ' '.join(text)
    return text


def read_docx(docx_path):
    """Read text from a DOCX file"""
    text = docx2txt.process(docx_path)
    text = re.sub(r'\s+', ' ', text)
    return text

def text_from_any_documents(file_path):
    """Extract text from any type of document (PDF, DOCX, Image)"""

    extension = os.path.splitext(file_path)[-1].lower()

    if extension == '.pdf':
        if is_pdf_scanned(file_path):
            return extract_text_from_pdf_ocr(file_path)
        else:
            return extract_text_from_pdf(file_path)

    elif extension == '.doc' or extension == '.docx':
        return read_docx(file_path)

    elif extension == '.jpg' or extension == '.png':
      return extract_text_from_image(file_path)
    elif file_path is None:
      return None

    else:
        print(f"Unsupported file type: {extension}. Unable to extract text.")
        return None

def split_text(text, words_per_subtext, word_overlap):
    """Split the text into subtexts with a certain number of words and overlap"""
    words = text.split()
    subtexts = []

    for i in range(0, len(words), words_per_subtext - word_overlap):
        subtext = ' '.join(words[i:i + words_per_subtext])
        subtexts.append(subtext)

    return subtexts