"""
File: scrape_urls.py
Description: Scrapes product links from the B&H Photo Video website.
Author: Matěj Konopík, FIT BUT, matejkonopik@gmail.com
Date: December 2023
Python version: 3.11
"""
from selenium_driver import get_driver
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def scrape_links(driver, base_url, max_links) -> list[str]:
    """
    Uses Selenium WebDriver to scrape links from the given URL until it gets max_links.

    :param driver: Selenium WebDriver.
    :param base_url: Base URL to scrape content from.
    :param max_links: Maximum number of product links to fetch.
    """
    product_links = []

    # Visit the first page
    driver.get(base_url)
    print("Loading page 1 ...")
    time.sleep(3)  # Wait for JavaScript to load
    page_number = 2
    while len(product_links) < max_links:
        # Scrape all links from the current page
        links = driver.find_elements(By.CLASS_NAME, "product-item__title")
        for link in links:
            link_string = link.get_attribute("href")
            product_links.append(link_string)

        # Visit next page
        driver.get(f"https://thecamerastore.com/collections/mirrorless-system-cameras?page={page_number}")
        print(f"Loading page {page_number} ...")
        page_number += 1
        print(len(product_links))

    return product_links


def save_to_file(links: list[str], filename: str) -> None:
    """
    Saves the given list of links to a file.

    :param links: List of links to save.
    :param filename: Name of the file to save to.
    """
    try:
        with open(filename, "w") as f:
            for link in links:
                f.write(link + '\n')
    except IOError as e:
        print(f"Error when attempting to write to a file {filename}: <{e}>")


if __name__ == "__main__":
    driver: webdriver = get_driver()

    links: list[str] = scrape_links(
        driver,
        "https://thecamerastore.com/collections/mirrorless-system-cameras",
        100)
    save_to_file(links, "../data/urls.txt")

    print(f"Scraped {len(links)} links.")

    driver.quit()
