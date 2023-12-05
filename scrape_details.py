"""
File: scrape_details.py
Description: Scrapes product details from camera detail pages listed in urls.txt.
Author: Matěj Konopik, FIT BUT, matejkonopik@gmail.com
Date: December 2023
Python version: 3.11
"""
import csv
import sys

from selenium_driver import get_driver
from selenium.webdriver.common.by import By
from selenium import webdriver


def read_urls(filename: str) -> list[str]:
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

    # Return even if no 'Specifications' card found on the site.
    return product_details


def print_data(data: [dict]) -> None:
    """
    Prints scraped data to stdout in a tab-separated format.
    :param data: List of dictionaries containing scraped data from product websites.
    :return: None.
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

    # Create driver and read URLs from file
    driver = get_driver()
    urls: [str] = read_urls(input_file)

    # Scrape details from each URL
    scraped_data: [dict] = []
    for url in urls:
        details = scrape_details(driver, url)
        if details:
            scraped_data.append(details)

    driver.quit()

    # Print scraped data to stdout
    print_data(scraped_data)
