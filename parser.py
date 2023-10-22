import os
import random
import string
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote


def check_response(url, proxies=None, headers=None):
    if proxies is None:
        proxies = None
    else:
        proxies = proxies
    response = requests.get(url, proxies=proxies, headers=headers)
    return response


def download_images(url, path=None, default_format="png", tags=None, proxies=None, headers=None):

    if proxies is None:
        proxies = None
    else:
        proxies = proxies

    if proxies is None:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url, proxies=proxies, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")

    if path is None:
        path = "parsed_images"

    if not os.path.exists(path):
        os.makedirs(path)

    if tags is None:
        images = soup.find_all("img")
    else:
        images = soup.find_all("img", f'{tags}')

    for img in images:
        if "data-original" in img.attrs:
            img_url = img["data-original"]
        elif "data-src" in img.attrs:
            img_url = img["data-src"]
        else:
            img_url = img["src"]

        if not urlparse(img_url).netloc:
            img_url = url + img_url

        random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

        parsed_url = urlparse(img_url)
        image_path = unquote(parsed_url.path)
        _, image_ext = os.path.splitext(image_path)
        if image_ext:
            format_save = image_ext[1:]
        else:
            format_save = default_format

        file_name = f"{path}/{random_name}.{format_save}"

        try:
            if proxies is None:
                image_data = requests.get(img_url, headers=headers).content
            else:
                image_data = requests.get(img_url, headers=headers, proxies=proxies, timeout=10).content

        except:
            image_data = None

        if image_data:
            with open(file_name, "wb") as f:
                f.write(image_data)

    return 'Done'