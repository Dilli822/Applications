import fitz  # PyMuPDF
from docx import Document
from docx.shared import Inches
import os

def convert_pdf_to_docx(pdf_path):
    # Open the PDF
    pdf_document = fitz.open(pdf_path)
    
    # Create a new Word document
    doc = Document()

    # Iterate through each page in the PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Extract text from the page
        text = page.get_text()
        
        # Add the text to the Word document
        doc.add_paragraph(text)
        
        # Add a page break (except for the last page)
        if page_num < len(pdf_document) - 1:
            doc.add_page_break()

    # Generate output filename
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = f'{base_name}_output.docx'
    
    # Save the document
    doc.save(output_path)
    print(f"Conversion complete. Output saved as {output_path}")

# Usage
pdf_file_path = 'Calculus - Wikipedia.pdf'  # Replace with your PDF file path
convert_pdf_to_docx(pdf_file_path)