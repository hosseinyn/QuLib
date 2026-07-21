from questions.tasks import extract_text_from_uploaded_pdf, extract_image_text

def process_uploaded_pdf(pdf_file):
    if pdf_file.size > 5 * 1024 * 1024:
        return False, "حداکثر حجم مجاز فایل 5 مگابایت است."

    file_start = pdf_file.read(5)
    if file_start != b"%PDF-":
        return False, "فایل شما معتبر نیست."
    
    pdf_file.seek(0)
    
    if pdf_file.content_type != "application/pdf":
        return False, "فایل شما معتبر نیست."
    
    pdf_text = extract_text_from_uploaded_pdf(pdf_file)

    if pdf_text != False:
        return True, pdf_text
    else:
        return False, "پردازش فایل موفقیت آمیز نبود."

def process_uploaded_image(image_file):
    if image_file.size > 5 * 1024 * 1024:
        return False, "حداکثر حجم مجاز فایل 5 مگابایت است."

    file_start = image_file.read(8)

    valid = False
    if file_start.startswith(b'\x89PNG\r\n\x1a\n'):
        valid = True
    elif file_start.startswith(b'\xff\xd8\xff'):
        valid = True
    else:
        return False, "فایل شما معتبر نیست."

    image_file.seek(0)

    if image_file.content_type not in ["image/png", "image/jpeg"]:
        return False, "فرمت فایل باید PNG یا JPEG باشد."
    
    image_text = extract_image_text(image_file)

    if image_text != False:
        return True, image_text
    else:
        return False, "پردازش فایل موفقیت آمیز نبود."
