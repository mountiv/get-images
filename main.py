import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib.parse


def download_images(url):
    response = requests.get(url)
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
            if img_url.startswith('http'):
                img_response = requests.get(img_url)
            else:
                img_response = requests.get(urllib.parse.urljoin(url, img_url))

            # Extract the filename from the URL
            parsed_url = urllib.parse.urlparse(img_url)
            filename = os.path.basename(parsed_url.path)
            filename = filename.split('?')[0]  # Remove the query string

            # Save the image to the 'images' directory
            with open(os.path.join('images', filename), 'wb') as f:
                f.write(img_response.content)

            print(f'Downloaded {filename}')
        else:
            print('Image source URL not found.')


url = sys.argv[1]
print("URL:", url)

download_images(url)
