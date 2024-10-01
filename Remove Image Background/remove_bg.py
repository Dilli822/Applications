import requests
from rembg import remove
from PIL import Image
import io
import os

def remove_background_from_url(image_url):
    try:
        # Fetch the image from the URL
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Open the image from the response content
        input_image = Image.open(io.BytesIO(response.content)).convert("RGBA")
        
        # Remove the background
        output_image = remove(input_image)
        
        # Extract the file name from the URL
        output_image_name = os.path.basename(image_url).split('?')[0]  # Remove query parameters if any
        output_image_path = f"{output_image_name}_no_background.png"  # Append suffix to indicate background removal
        
        # Save the output image
        output_image.save(output_image_path)
        print(f"Background removed. Output saved to: {output_image_path}")

    except requests.RequestException as e:
        print(f"Failed to fetch image. Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR82bx-Cg82mONaVNXV78s_lMt48Lk0vr31wA&s'  # Replace with your image URL
remove_background_from_url(image_url)
