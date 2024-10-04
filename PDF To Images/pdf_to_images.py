import os
import requests
from pdf2image import convert_from_path
from urllib.parse import urlparse

def is_valid_local_file(pdf_path):
    """Check if the given path is a valid local file."""
    return os.path.isfile(pdf_path)

def download_pdf_from_url(pdf_url, output_folder):
    """Download PDF from the URL to a specified folder."""
    try:
        # Extract PDF name from the URL
        file_name = os.path.basename(urlparse(pdf_url).path)
        output_pdf_path = os.path.join(output_folder, file_name)

        # Download the PDF file
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open(output_pdf_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded PDF from URL: {output_pdf_path}")
            return output_pdf_path
        else:
            raise Exception(f"Failed to download PDF. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading PDF from URL: {e}")
        return None

def convert_pdf_to_images(pdf_path, output_folder):
    """Convert PDF pages to images and save them."""
    try:
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Convert PDF to images
        images = convert_from_path(pdf_path)

        # Save each page as an image
        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f'page_{i + 1}.png')
            image.save(image_path, 'PNG')
            print(f"Saved {image_path}")

        print("All pages converted to images successfully!")
    except Exception as e:
        print(f"Error occurred while converting PDF to images: {e}")

def process_pdf_input(pdf_input, output_folder):
    """Handle the PDF input, whether it's a local path or a URL."""
    if is_valid_local_file(pdf_input):
        print("Processing local PDF file...")
        convert_pdf_to_images(pdf_input, output_folder)
    else:
        print("Assuming input is a URL. Attempting to download...")
        downloaded_pdf = download_pdf_from_url(pdf_input, output_folder)
        if downloaded_pdf:
            convert_pdf_to_images(downloaded_pdf, output_folder)

# Example usage
pdf_input = 'https://github.com/Dilli822/Learning-Utsav-AI_ML-/blob/main/30Days%20Self%20Learning%20Challenge/Day2/Quick%20Notefina%3Bl.pdf' 
# pdf_input = "./AI Talk Show Session.pdf"
output_folder = '~/Output'  # Folder to save images

process_pdf_input(pdf_input, output_folder)
