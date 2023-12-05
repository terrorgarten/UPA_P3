"""
File: scrape_details.py
Description: Scrapes product details from camera detail pages listed in urls.txt.
Author: Matěj Konopík, FIT BUT, matejkonopik@gmail.com
Date: December 2023
Python version: 3.11
"""
import csv
import sys

from selenium_driver import get_driver
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd


def read_urls(filename: str) -> list[str]:
    """
    Reads URLs from a file and returns them as a list.

    :param filename: Name of the file to read from.
    """
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


def scrape_details(driver: webdriver, url: str) -> dict:
    """
    Scrapes the 'Specifications' card details from a given URL.

    :param driver: Selenium WebDriver.
    :param url: URL to scrape details from.
    """
    wanted_specs = ["Video Resolution", "Dimensions", "Weight", "Recording Media", "Power Source", "ISO Sensitivity",
                    "Lens Mount", "Shutter Speed", "Continuous Shooting Speed", "Sensor Resolution", "Resolution"]
    product_details = {'url': url}

    driver.get(url)

    # get name, price and stock status
    product_details["price"] = driver.find_element(By.CLASS_NAME, "price").text.removeprefix("Sale price\n")
    product_details["stock_status"] = driver.find_element(By.CLASS_NAME, "product-form__inventory").text
    product_details["product_name"] = driver.find_element(By.CLASS_NAME, "product-meta__title").text

    # handle product details from the 'Specifications' card
    cards = driver.find_elements(By.CLASS_NAME, "card")

    for card in cards:
        headers = card.find_elements(By.CLASS_NAME, "card__header")
        for header in headers:
            if "Specifications" in header.text:
                card_body = card.find_element(By.CLASS_NAME, "card__section")
                card_text = card_body.text

                lines = card_text.split('\n')
                for line in lines:
                    if ': ' in line:
                        key, value = line.split(': ', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in wanted_specs:
                            product_details[key] = value
                if "Sensor Resolution" not in product_details and "Resolution" in product_details:
                    product_details["Sensor Resolution"] = product_details["Resolution"]
                if "Resolution" in product_details:
                    del product_details["Resolution"]

                return product_details

    return product_details  # Return even if no 'Specifications' found


def export_to_tsv(data: [dict], filename: str) -> None:
    """
    Exports a pandas DataFrame to a TSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, sep='\t', index=False)


def print_data(data: [dict]) -> None:
    """
    Prints scraped data to stdout in a tab-separated format.
    :param data: List of dictionaries containing scraped data from product websites.
    :return: Nothing
    """

    # Define the desired order for specific keys
    desired_order = ['url', 'product_name', 'price', 'stock_status']

    # Extend the order with other keys found in the data, sorted alphabetically
    # and not already in the desired_order
    additional_keys = sorted({k for d in data for k in d if k not in desired_order})
    sorted_keys = desired_order + additional_keys

    # Print each row in the specified order
    for d in data:
        # Extract values in the order of sorted_keys, use empty string for missing keys
        row = [str(d.get(key, '')) for key in sorted_keys]
        print('\t'.join(row))


if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
        open(input_file, 'r')
    except IndexError:
        print("Please provide a file with URLs to scrape.")
        exit(1)
    except OSError:
        print(f"File {sys.argv[1]} not found.")
        exit(1)

    driver = get_driver()
    urls: [str] = read_urls(input_file)

    scraped_data: [dict] = []
    for url in urls:
        details = scrape_details(driver, url)
        if details:
            scraped_data.append(details)

    driver.quit()
    # export_to_tsv(scraped_data, 'data.tsv')
    print_data(scraped_data)
