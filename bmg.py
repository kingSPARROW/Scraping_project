import time
import csv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Web scraping functions
def initialize_driver():
    driver = webdriver.Firefox()
    return driver

def get_html_soup_selenium(driver, url, max_retries=3):
    for _ in range(max_retries):
        try:
            driver.get(url)
            time.sleep(1)  # Adjust this sleep time as needed
            page_source = driver.page_source
            break  # If successful, break out of the loop
        except TimeoutException as e:
            print(f"Timeout Exception: {e}")
            page_source = None
            if _ == max_retries - 1:
                print(f"Max retries reached. Unable to fetch page: {url}")
                break
            else:
                print(f"Retrying... Attempt {_ + 1}")

    if page_source:
        soup = BeautifulSoup(page_source, "html.parser")
        return soup
    else:
        return None

# Scrape reviews using Selenium
def scrape_reviews_selenium(driver, url, page_number, filename, max_retries=3):
    reviews = []

    for _ in range(max_retries):
        # Load the webpage using Selenium
        soup = get_html_soup_selenium(driver, url)

        if soup:
            review_blocks = soup.find_all('div', {'class': '_2zlSTn'})

            for block in review_blocks:
                rating_elem = block.find('div', {'class': '_3LWZlK'})
                review_elem = block.find('div', {'class': '_2Xz2nt'})
                sum_elem = block.find('div', {'class': 'wdVh9J'})
                name_elem = block.find('div', {'class': '_3G7LJF'}).find('div', {'class': '_1sk9Vt'})
                date_elem = block.find('div', {'class': '_3G7LJF'}).find_all('div', {'class': '_1sk9Vt'})[-1]
                location_elem = block.find('div', {'class': 'row Ljko-4'}).find('div', {'class': '_1LmwT9'}).text

                if rating_elem and review_elem and name_elem and date_elem and name_elem.text:
                    review = {
                        'Rating': rating_elem.text.strip(),
                        'Review': review_elem.text.strip(),
                        'Name': name_elem.text.strip(),
                        'Date': date_elem.text.strip(),
                        'Review Description': sum_elem.text.strip(),
                        'Location': location_elem.strip(),
                        'Link': url,
                        'Page Number': page_number
                    }
                    reviews.append(review)
            break  # Break out of retry loop if successful
        else:
            if _ == max_retries - 1:
                print(f"Max retries reached. Unable to fetch page: {url}")
                break
            else:
                print(f"Retrying... Attempt {_ + 1}")

    return reviews

def save_reviews_to_csv(reviews, filename):
    fields = ['Rating', 'Review', 'Name', 'Date', 'Review Description', 'Location', 'Link', 'Page Number']
    
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fields)

        # Write the data
        csvwriter.writerows(reviews)

    print(f"Reviews appended to {filename} from page {reviews[0]['Page Number']}")

def main_with_selenium():
    base_url = "https://www.flipkart.com/reviews/PSLG4XSHNBXBHZY3:{}?"
    filename = 'reviews14830.csv'

    # Initialize the driver outside the loop
    driver = initialize_driver()

    for page in range(14830, 19500):  # Scraping reviews up to page 18020
        current_url = base_url.format(page)
        page_reviews = scrape_reviews_selenium(driver, current_url, page, filename)

        if not page_reviews:
            print(f"No reviews found on page {page}")
        else:
            save_reviews_to_csv(page_reviews, filename)

    # Quit the driver after scraping all pages
    driver.quit()

if __name__ == '__main__':
    main_with_selenium()
