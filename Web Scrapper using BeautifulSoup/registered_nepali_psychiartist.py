import requests
from bs4 import BeautifulSoup
import json

# URL of the page to scrape (input can vary)
url = "https://psychiatrynepal.org.np/register-psychiatrist/"

# Derive the base name for output files based on input
base_filename = "registered_nepali_psychiatrist"

# Send a GET request to fetch the content of the page
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the specific <h1> with "Registered Psychiatrist" and related data
heading = soup.find('h1', text="Registered Psychiatrist")

# Extract the related content after the heading
if heading:
    content = heading.find_next('div').get_text()
else:
    content = "No data found."

# Save the data in JSON format using the base filename
data = {"Registered_Psychiatrist": content}
with open(f'{base_filename}.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

# Save the data in .txt format using the base filename
with open(f'{base_filename}.txt', 'w') as text_file:
    text_file.write(content)

print(f"Data saved in {base_filename}.json and {base_filename}.txt")
