import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import WebDriverWait
import requests
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

# Set the path to your Chrome WebDriver executable
webdriver_path = 'C:\path\to\chromedriver.exe'

# Create Chrome options
options = Options()
options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'

# Create a new instance of the Chrome WebDriver with options
driver = webdriver.Chrome(options=options)

# Set page load strategy to eager
driver.set_page_load_timeout(10)  # Set a reasonable page load timeout

# Open the desired link
# //*[@id="__next"]/div[3]/div/div[2]/div[5]/div[1]/div/a/div/button/div/span
link = 'https://www.meesho.com/kobra-fancy-nutrition-weight-gain/p/13vdcn'
driver.get(link)


# Maximize the browser window
driver.maximize_window()


view_button1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[3]/div/div[2]/div[5]/div[1]/div/a/div/button/div/span'))
    )
view_button1.click()
    


while True:
        try:
            view_button2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/button/div/span'))
            )
            view_button2.click()
            time.sleep(1)  # Wait for the content to load
        except:
            break


page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')

def cus_rev(soup):
    reviews = []
    review_blocks = soup.find_all('div', {'class': 'sc-ezOQGI iOvaTb'})
    for block in review_blocks:
        class1_elements = block.find_all(class_='sc-gKPRtg kJYMan')
        class2_elements = block.find_all(class_='sc-gKPRtg kuvnkX')
        class3_elements = block.find_all(class_='sc-gKPRtg dgeEur Comment__CommentText-sc-1ju5q0e-3 cfdxfJ Comment__CommentText-sc-1ju5q0e-3 cfdxfJ')
        class4_elements = block.find_all(class_='sc-gKPRtg jdrvQI')

        # Extract data from each element
        ratings = [element.text for element in class1_elements]
        reviews_text = [element.text for element in class2_elements]
        names = [element.text for element in class3_elements]
        dates = [element.text for element in class4_elements]

        # Create a dictionary for each review
        for rating, review_text, name, date in zip(ratings, reviews_text, names, dates):
            review = {
                'Name': rating,
                'Rating': review_text,
                'Review': name,
                'Date': date,
            }
            reviews.append(review)

    return reviews
reviews = cus_rev(soup)

print(f"Total reviews scraped: {len(reviews)}")
print(reviews)

# Authenticate with Google Sheets API using service account credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('C:\\Users\\faroo\Downloads\\youtube0011-391306-e2aaaf87f3f1.json', scope)


# Authenticate and access the Google Sheets API
client = gspread.authorize(credentials)

# Open the existing Google Sheets spreadsheet
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/14S7YUe1x24jqoFwjQkej6lh7zJrHMr6ImJ8eDErS3PU/edit?pli=1#gid=0')
reviews = cus_rev(soup)

# Set the sheet name as the current date
today = date.today()
new_sheet_name = today.strftime("%d-%m-%Y")

# Create a new sheet
spreadsheet.add_worksheet(title=new_sheet_name, rows="100", cols="20")

# Select the new sheet
sheet = spreadsheet.worksheet(new_sheet_name)

# Create a new list with the header row included
header_row = ['Name', 'Review', 'Rating', 'Date']
values = [[review['Name'], review['Review'], review['Rating'], review['Date']] for review in reviews]

# Clear the existing values in the sheet
sheet.clear()
sheet.append_row(header_row)
# Append the data list to the Google Sheets
sheet.append_rows(values)

print("Reviews saved to Google Sheets.")