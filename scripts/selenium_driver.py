from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
