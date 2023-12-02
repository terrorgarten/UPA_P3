"""
File: scrape_urls.py
Description: Scrapes product links from the B&H Photo Video website.
Author: Matěj Konopík, FIT BUT, matejkonopik@gmail.com
Date: December 2023
Python version: 3.11
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def get_driver():
    """
    Initializes and returns a Selenium WebDriver in headless mode with a custom user agent.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set a user agent - without this, the cloudflare antibot will block the request (responds with the waiting page)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')

    return webdriver.Chrome(options=chrome_options)


def print_html(driver, url):
    """
    Prints the HTML content of the given URL.

    :param driver: Selenium WebDriver.
    :param url: URL to scrape content from.
    """
    driver.get(url)
    time.sleep(15)  # Wait for JavaScript to load
    print(driver.page_source)


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
    time.sleep(5)  # Wait for JavaScript to load
    while len(product_links) < max_links:
        # Scrape all links from the current page
        links = driver.find_elements(By.CLASS_NAME, "title_UCJ1nUFwhh")
        for link in links:
            product_links.append(link.get_attribute("href"))

        # Click the next page button
        next_page_button = driver.find_element(By.CLASS_NAME, "arrowLink_Mq9n1iP4rq")
        driver.execute_script("arguments[0].click();", next_page_button)

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
        "https://www.bhphotovideo.com/c/buy/Digital-Cameras/ci/9811/N/4288586282",
        100)
    save_to_file(links, "../data/urls.txt")

    print(f"Scraped {len(links)} links.")

    driver.quit()
