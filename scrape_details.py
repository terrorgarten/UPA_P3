import sys
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


def read_urls(filename: str) -> list:
    """
    Reads URLs from a file and returns them as a list.

    :param filename: Name of the file to read from.
    """
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except OSError:
        print(f"File '{filename}' not found.")
        exit(1)


def scrape_details(url: str) -> dict:
    """
    Scrapes the 'Specifications' card details from a given URL.

    :param url: URL to scrape details from.
    """
    wanted_specs = ["Video Resolution", "Dimensions", "Weight", "Recording Media", "Power Source", "ISO Sensitivity",
                    "Lens Mount", "Shutter Speed", "Continuous Shooting Speed", "Sensor Resolution", "Resolution"]
    product_details = {'url': url}

    # Send an HTTP GET request to the URL
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Error when attempting to send an HTTP request: <{e}>", file=sys.stderr)
        return product_details

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get product name, price, and stock status
        product_details["product_name"] = soup.find("h1", class_="product-meta__title").text
        product_details["price"] = soup.find("span", class_="price").text.replace("Sale price", "").replace("\n", "")
        product_details["stock_status"] = soup.find("span", class_="product-form__inventory").text

        # Find and parse the 'Specifications' card
        card_elements = soup.find_all("div", class_="card")
        for card in card_elements:
            header = card.find("div", class_="card__header")
            if header and "Specifications" in header.text:
                card_text = card.find_next("div", class_="card__section").find("div", class_="rte text--pull")
                if card_text:
                    spec_items = card_text.find_all("p")

                    # Special case - weird formatting
                    if len(spec_items) == 1:
                        specs = spec_items[0].decode_contents().split('<br/>')
                        for spec in specs:
                            if ':' in spec:
                                key, value = spec.split(':', 1)
                                key = key.strip().replace("<strong>", "")
                                value = value.strip().replace("</strong>", "")
                                if key in wanted_specs:

                                    product_details[key] = value

                    elif len(spec_items) == 0:
                        specs = card_text.decode_contents().split('<br/>')
                        for spec in specs:
                            if ':' in spec:
                                key, value = spec.split(':', 1)
                                key = key.strip().replace("<strong>", "")
                                value = value.strip().replace("</strong>", "")
                                if key in wanted_specs:
                                    product_details[key] = value

                    # "Normal" case
                    else:
                        for item in spec_items:
                            text = item.get_text(strip=True)
                            key, value = text.split(':', 1)
                            key = key.strip()
                            value = value.strip()
                            if key in wanted_specs:
                                product_details[key] = value

                    # Handle special case - "Resolution" and "Sensor Resolution" are the same thing
                    if "Resolution" in product_details:
                        if "Sensor Resolution" not in product_details:
                            product_details["Sensor Resolution"] = product_details["Resolution"]
                        del product_details["Resolution"]

                return product_details

    return product_details


def export_to_tsv(data: [dict], filename: str) -> None:
    """
    Exports a pandas DataFrame to a TSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, sep='\t', index=False)

def print_data(data: list) -> None:
    """
    Prints scraped data to stdout in a tab-separated format.

    :param data: List of dictionaries containing scraped data from product websites.
    """
    desired_order = ['url', 'product_name', 'price', 'stock_status']

    additional_keys = sorted({k for d in data for k in d if k not in desired_order})
    sorted_keys = desired_order + additional_keys

    # Print each row in the specified order
    for d in data:
        row = [str(d.get(key, '')) for key in sorted_keys]
        print('\t'.join(row), file=sys.stdout)


if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except IndexError:
        print("Please provide a file with URLs to scrape.")
        exit(1)

    # Read URLs from file
    urls = read_urls(input_file)

    # Scrape details from each URL
    scraped_data = []
    for url in urls:
        details = scrape_details(url)
        if details:
            scraped_data.append(details)

        # Add a delay to avoid overwhelming the server with requests
        time.sleep(1)

    # Print scraped data to stdout
    print_data(scraped_data)
