"""
File: scrape_details.py
Description: Scrapes product details from camera detail pages listed in urls.txt.
Author: Matěj Konopík, FIT BUT, matejkonopik@gmail.com
Date: December 2023
Python version: 3.11
"""

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
    product_details = {'URL': url}

    driver.get(url)
    print(f"Scraping {url} ...")
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
                        product_details[key.strip()] = value.strip()

                return product_details

    return product_details  # Return even if no 'Specifications' found


def parse_to_dataframe(specs_list: list) -> pd.DataFrame:
    """
    Parses a list of dictionaries into a pandas DataFrame, keeping only common keys.
    """
    common_keys = set.intersection(*[set(spec.keys()) for spec in specs_list])
    filtered_specs = [{k: spec[k] for k in common_keys} for spec in specs_list]
    return pd.DataFrame(filtered_specs)


def export_to_tsv(df: pd.DataFrame, filename: str) -> None:
    """
    Exports a pandas DataFrame to a TSV file.
    """
    df.to_csv(filename, sep='\t', index=False)


if __name__ == "__main__":
    driver = get_driver()
    urls = read_urls('../data/urls.txt')
    scraped_data = []

    for url in urls:
        details = scrape_details(driver, url)
        if details:
            scraped_data.append(details)

    driver.quit()

    if scraped_data:
        df = parse_to_dataframe(scraped_data)
        export_to_tsv(df, '../data/data.tsv')
        print("Data exported to data/data.tsv")
    else:
        print("No data scraped.")
