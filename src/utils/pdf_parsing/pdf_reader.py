import pdfplumber


def extract_text_from_pdf(path_to_pdf_file):
    full_text = ""
    with pdfplumber.open(path_to_pdf_file) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        if text:
            full_text = text
    return full_text
