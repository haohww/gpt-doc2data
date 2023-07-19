import os
import magic
from PyPDF2 import PdfReader

def get_file_string(context):
    file_strings = []

    for root, dirs, files in os.walk(context['data_dir']):
        for file in files:
            file_path = os.path.join(root, file)
            file_type = magic.from_file(file_path, mime=True)

            if file_type in ['text/plain', 'text/markdown']:
                with open(file_path, 'r') as f:
                    file_strings.append(f.read().strip() + ' ')
            elif file_type == 'application/pdf':
                with open(file_path, 'rb') as f:
                    pdf_reader = PdfReader(f)
                    num_pages = len(pdf_reader.pages)
                    file_text = ""
                    for page_num in range(num_pages):
                        file_text += pdf_reader.pages[page_num].extract_text().strip() + ' '
                    file_strings.append(file_text)

    return ' '.join(file_strings)