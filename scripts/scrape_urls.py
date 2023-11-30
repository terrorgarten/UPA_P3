import requests
from bs4 import BeautifulSoup
import time


def fetch_html(url):
    """
    Fetches the HTML content of a given URL.

    :param url: URL to fetch content from.
    :return: HTML content.
    """
    response = requests.get(url)
    return response.text


def parse_product_links(html_content, max_links):
    """
    Parses the HTML content to extract product links.

    :param html_content: HTML content to parse.
    :param max_links: Maximum number of product links to extract.
    :return: List of product URLs.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    product_links = []

    for link in soup.find_all('a', href=True):
        if len(product_links) < max_links and '/c/product/' in link['href']:
            full_link = f"https://www.bhphotovideo.com{link['href']}"
            if full_link not in product_links:
                product_links.append(full_link)

    return product_links


if __name__ == "__main__":
    url = 'https://www.bhphotovideo.com/c/buy/Digital-Cameras/ci/9811/N/4288586282'
    html_content = fetch_html(url)
    product_links = parse_product_links(html_content, 100)

    for link in product_links:
        print(link)

    # Optionally, write the links to a file
    with open('data/urls.txt', 'w') as file:
        for link in product_links:
            file.write(link + '\n')
