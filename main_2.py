import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib.parse
import base64
from requests.exceptions import Timeout

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

def save_image(img_url, url):
    try:
        if img_url.startswith('http'):
            img_response = requests.get(img_url, timeout=3)
        else:
            if img_url.startswith('data:image'):
                # Decode the Base64 string
                image_data = base64.b64decode(img_url.split(',')[1])
                img_response = requests.Response()
                img_response._content = image_data
            else:
                img_response = requests.get(urllib.parse.urljoin(url, img_url))

        if not img_response.ok:
            print(f'Error downloading image from {img_url}')
            return None

        # Extract the filename from the URL
        parsed_url = urllib.parse.urlparse(img_url)
        filename = os.path.basename(parsed_url.path)
        filename = filename.split('?')[0]  # Remove the query string

        # Save the image to the 'images' directory
        if not os.path.exists('images'):
            os.makedirs('images')

        with open(os.path.join('images', filename), 'wb') as f:
            f.write(img_response.content)

        print(f'..........Downloaded {filename}')
        return filename
    
    except Timeout:
        print(f'Timeout exceeded for {img_url}. Moving to next request...')
        return None

def download_images(urls):
    try:
        for url in urls:
            print("URL:", url)
            try:
                response = requests.get(url, timeout=3)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Create a directory to store the images
                if not os.path.exists('images'):
                    os.makedirs('images')

                # Find all image tags on the page
                img_tags = soup.find_all('img')

                # Download each image
                for img in img_tags:
                    img_url = img.get('src')
                    if img_url:
                        save_image(img_url, url)
                    else:
                        print('..........Image source URL not found.')

            except Timeout:
                print(f'Timeout exceeded for {url}. Moving to next request...')

    except KeyboardInterrupt:
        print('\nProcess interrupted by user. Exiting...')
        
# Usage
urls = read_urls_from_file('URLs.txt')
download_images(urls)
