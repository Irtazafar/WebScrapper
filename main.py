import requests
from bs4 import BeautifulSoup
import os
import re
import base64
from urllib.parse import urlparse
import string

def sanitize_filename(filename):
    # Remove invalid characters from the filename
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    return filename

def scrape_website(url, folder_path):
    # Send a GET request to the provided URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all image elements
        images = soup.find_all('img')

        # Create a folder if it doesn't exist to store images
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Download and save images
        for img in images:
            # Get the 'src' attribute of the image tag
            img_url = img.get('src')
            # Check if img_url is not None
            if img_url:
                # Check if the URL is valid and not a base64 encoded SVG image
                if img_url.startswith("http") and not img_url.startswith("data:image/svg+xml;base64"):
                    # Extract the image name from the URL
                    img_name = os.path.basename(urlparse(img_url).path)
                    img_name = sanitize_filename(img_name)
                    # Download the image content
                    img_data = requests.get(img_url).content
                    # Write the image content to a file
                    with open(os.path.join(folder_path, img_name), 'wb') as img_file:
                        img_file.write(img_data)
                        print(f"Image '{img_name}' downloaded successfully.")
                else:
                    print("Skipping invalid image URL:", img_url)
            else:
                print("Skipping image with no 'src' attribute.")

        # Find the elements containing the text content
        paragraphs = soup.find_all('p')

        # Print out the text content of each paragraph
        for paragraph in paragraphs:
            print(paragraph.get_text())
    else:
        print("Failed to retrieve data. Status code:", response.status_code)


# Prompt the user to input the website URL
website_name = input("Enter the website URL you want to scrape: ")
folder_path = "images"  # Path to the folder where images will be saved
scrape_website(website_name, folder_path)
