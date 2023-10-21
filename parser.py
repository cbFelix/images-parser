import os
import random
import string
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0"
}

proxies = {
    'http': '34.142.51.21P:443',
    'https': '161.117.81.228:483'
}


def check_response(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response


def download_images(url, path=None, format_save="png"):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    if path is None:
        path = "parsed_images"

    if not os.path.exists(path):
        os.makedirs(path)

    images = soup.find_all("img")

    for img in images:
        img_url = img["src"]

        if not urlparse(img_url).netloc:
            img_url = url + img_url

        random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        file_name = f"{path}/{random_name}.{format_save}"
        try:
            image_data = requests.get(img_url, headers=headers).content

        except:
            try:
                image_data = requests.get(img_url, headers=headers).content

            except:
                image_data = requests.get(f"https:{img_url}", headers=headers, timeout=10).content


        with open(file_name, "wb") as f:
            f.write(image_data)
