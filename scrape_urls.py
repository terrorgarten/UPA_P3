import requests
from bs4 import BeautifulSoup
import sys
import time

def scrape_links(prod_list_url: str, base_url: str, max_links: int, print_out: bool = False) -> list:
    """
    Scrapes product links from the given URL until it reaches max_links.

    :param print_out: Whether to print the links to stdout
    :param prod_list_url: Base URL to scrape content from.
    :param max_links: Maximum number of product links to fetch.
    """
    product_links = []
    page_number = 1

    while len(product_links) < max_links:
        # Construct the URL for the current page
        url = f"{prod_list_url}&page={page_number}"

        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all links with the specified class
            links = soup.find_all(class_="product-item__title")

            for link in links:
                link_string = base_url + link['href']

                # Print to stdout if requested
                if print_out:
                    print(link_string, file=sys.stdout)

                # Break if we have enough links
                if len(product_links) >= max_links:
                    return product_links

                product_links.append(link_string)

            page_number += 1

            # Add a delay to avoid overwhelming the server with requests
            time.sleep(2)
        else:
            print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
            break

    return product_links

def save_to_file(links: list, filename: str) -> None:
    """
    Saves the given list of links to a file.

    :param links: List of links to save.
    :param filename: Name of the file to save to.
    """
    try:
        with open(filename, "w") as f:
            for link in links:
                f.write(link + '\n')
    except OSError as e:
        print(f"Error when attempting to write to a file {filename}: <{e}>")

if __name__ == "__main__":
    base_url = "https://thecamerastore.com"
    prod_list_url = "https://thecamerastore.com/collections/cameras?sort_by=best-selling&filter.p.m.search_filters.category=Mirrorless+System+Cameras&filter.v.price.gte=&filter.v.price.lte="
    max_links = 100

    links = scrape_links(prod_list_url, base_url, max_links, True)

    # Uncomment the line below to save links to a file
    # save_to_file(links, "../data/urls.txt")
