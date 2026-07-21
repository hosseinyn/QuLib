import os
import tempfile
from pdf2docx import Converter
import io

import pdfplumber

from bidi.algorithm import get_display

import easyocr
from PIL import Image
import numpy as np
from celery import shared_task
from .repositories.question_repository import get_question_by_id

@shared_task
def convert_pdf(question_id : int) -> io.BytesIO:
    """
    Convert a PDF file to a Word document format in memory.

    Args:
        pdf_file (UploadedFile): The uploaded PDF file to convert.

    Returns:
        io.BytesIO: In-memory stream containing the converted Word document.

    document by AI
    """
    question = get_question_by_id(question_id)
    pdf_file = question.file
    name = question.title

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        for chunk in pdf_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    word_io = io.BytesIO()

    try:
        cv = Converter(tmp_path)
        cv.convert(word_io , layout=True)
        cv.close()
    finally:
        os.remove(tmp_path) 

    word_io.seek(0)

    return {"word_io" : word_io.read() , "name" : name}

@shared_task
def extract_text_from_uploaded_pdf(temp_path: str):
    try:
        full_text = ""

        with pdfplumber.open(temp_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

        full_text = get_display(full_text)

        return {
            "status": True,
            "text": full_text,
        }

    except Exception:
        return {
            "status": False,
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    

def compress_text_whitespace(text: str) -> str:
    """
    Compress whitespace in text by joining lines with single spaces.

    Args:
        text (str): The input text to process.

    Returns:
        str: Compressed text.

    document by AI
    """
    lines = [line.strip() for line in text.splitlines() if line.strip() != ""]
    return " ".join(lines)

@shared_task
def extract_image_text(temp_path: str):
    """
        Extract text content from an uploaded image using easyocr.
    
        Args:
            uploaded_file (UploadedFile): The uploaded image file.
    
        Returns:
            str: Extracted text from the image.
    
        document by AI
        """
    try:
        image = Image.open(temp_path)
        image_np = np.array(image)

        reader = easyocr.Reader(['fa', 'en'], gpu=False)

        results = reader.readtext(image_np)
        text_result = "\n".join(text for _, text, _ in results)

        return {
            "status": True,
            "text": text_result,
        }

    except Exception:
        return {
            "status": False,
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

