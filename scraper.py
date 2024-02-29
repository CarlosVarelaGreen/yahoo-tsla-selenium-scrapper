from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

def scrape_news_headlines():
    # Set up Selenium WebDriver with Chrome:
    options = Options()
    options.add_argument("--headless=new") #comment this is you wish to see the chrome window...
    driver = webdriver.Chrome(options=options)
    url = 'https://finance.yahoo.com/quote/tsla/news'
    driver.get(url)
    print('Opening URL')
    print()
    # Wait for page to load:
    time.sleep(3)

    # Scroll to accept cookies:
    scroll_down_button = driver.find_element(By.ID, "scroll-down-btn")
    scroll_down_button.click()
    print('Getting rid of cookies')
    print()
    # Wait to go down:
    time.sleep(1)

    # Click the accept all button:
    accept_all_button = driver.find_element(By.CLASS_NAME, "accept-all")
    accept_all_button.click()

    time.sleep(2)

    # scroll down to load news content:
    max_scrolls = 35
    scroll_count = 0
    print('Please wait while I read the news...')
    print()
    while scroll_count < max_scrolls:
        # Send spacebar key to scroll down:
        ActionChains(driver).send_keys(Keys.SPACE).perform()

        # Wait for a short duration to allow content to load:
        time.sleep(1)

        scroll_count += 1

    # Find all <li> elements with the specified class to get content:
    content_elements = driver.find_elements(By.XPATH, '//li[@class="js-stream-content Pos(r)"]')

    # Create a list to store the titles:
    titles = []

    print('Scrapping content now')
    print()
    # Loop over each content element to get each title:
    for content_element in content_elements:
        title_element = content_element.find_element(By.TAG_NAME, 'h3')
        # Extract the text from the title element:
        title_text = title_element.text
        titles.append(title_text)

    # Convert to DataFrame:
    df = pd.DataFrame(titles, columns=['news_statement'])
    df.to_csv('news_headlines.csv', index=False, header=['news_statements'])
    print('Finished scrapping, your news got saved as "news_headlines.csv"')

    # Close the WebDriver:
    driver.quit()

if __name__ == "__main__":
    scrape_news_headlines()
