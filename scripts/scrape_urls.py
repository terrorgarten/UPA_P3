# selenium_scrape_headless.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def get_driver():
    """
    Initializes and returns a Selenium WebDriver in headless mode with a custom user agent.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Set a user agent - without this, the cloudflare antibot will block the request (responds with the waiting page)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def print_html(driver, url):
    """
    Prints the HTML content of the given URL.

    :param driver: Selenium WebDriver.
    :param url: URL to scrape content from.
    """
    driver.get(url)
    time.sleep(15)  # Wait for JavaScript to load
    print(driver.page_source)

def scrape_links(driver, base_url, max_links):
    """
    Uses Selenium WebDriver to scrape links from the given URL until it gets max_links.

    :param driver: Selenium WebDriver.
    :param base_url: Base URL to scrape content from.
    :param max_links: Maximum number of product links to fetch.
    """
    product_links = []
    page_number = 2  # Starting from page 2 since the first page is already visited

    # Visit the first page
    driver.get(base_url)
    time.sleep(15)  # Wait for JavaScript to load
    links = driver.find_elements(By.CLASS_NAME, 'title_UCJ1nUFwhh')
    for link in links:
        product_links.append(link.get_attribute('href'))
        print("Addindg initial")
    print(f"afterfirst {len(product_links)} links scraped so far")

    # Visit subsequent pages
    while len(product_links) < max_links:
        page_url = f"{base_url}/pn/{page_number}"
        print(page_url)
        time.sleep(60)  # Wait for JavaScript to load
        driver.get(page_url)
        time.sleep(60)  # Wait for JavaScript to load
        print(f"{len(product_links)} links scraped so far")
        links = driver.find_elements(By.CLASS_NAME, 'title_UCJ1nUFwhh')

        for link in links:
            if len(product_links) < max_links:
                product_links.append(link.get_attribute('href'))
            else:
                break

        page_number += 1

    for link in product_links:
        print(link)


if __name__ == "__main__":
    driver = get_driver()
    scrape_links(driver, 'https://www.bhphotovideo.com/c/buy/Digital-Cameras/ci/9811/N/4288586282', 100)
    driver.quit()
