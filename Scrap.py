import requests
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import date

def html_code(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def cus_rev(soup):
    reviews = []
    review_blocks = soup.find_all('div', {'class': '_27M-vq'})
    for block in review_blocks:
        rating_elem = block.find('div', {'class': '_3LWZlK'})
        review_elem = block.find('p', {'class': '_2-N8zT'})
        sum_elem = block.find('div', {'class': 't-ZTKy'})
        name_elem = block.find_all('p', {'class': '_2sc7ZR'})[0]
        date_elem = block.find_all('p', {'class': '_2sc7ZR'})[1]
        location_elem = block.find('p', {'class': '_2mcZGG'})
        
        if rating_elem and review_elem and name_elem and date_elem:
            review = {
                'Rating': rating_elem.text,
                'Review': review_elem.text,
                'Name': name_elem.text.strip(),
                'Date': date_elem.text.strip(),
                'Review Description': sum_elem.text.strip(),
                'Location': location_elem.text
            }
            reviews.append(review)
    return reviews

# URL of the page to scrape
url = "https://www.flipkart.com/sony-zv-e10l-mirrorless-camera-body-1650-mm-power-zoom-lens-vlog/product-reviews/itmed07cbb694444?pid=DLLG6G8U8P2NGEHG&lid=LSTDLLG6G8U8P2NGEHGGVZNLB&marketplace=FLIPKART"

reviews = []
page = 1

while True:
    page_url = url + "&page=" + str(page)
    print(page, "st page is scraping")
    soup = html_code(page_url)
    page_reviews = cus_rev(soup)
    if not page_reviews:
        break
    reviews.extend(page_reviews)
    page += 1


print(reviews)
# Define the scope and credentials for Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\faroo\Downloads\youtube0011-391306-e2aaaf87f3f1.json', scope)

# Authenticate and access the Google Sheets API
client = gspread.authorize(credentials)

# Open the existing Google Sheets spreadsheet
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/14S7YUe1x24jqoFwjQkej6lh7zJrHMr6ImJ8eDErS3PU/edit#gid=0')

# Set the sheet name as the current date
today = date.today()
new_sheet_name = today.strftime("%d-%m-%Y")

# Create a new sheet
new_worksheet = spreadsheet.add_worksheet(title=new_sheet_name, rows="100", cols="20")

# Select the new sheet
sheet = spreadsheet.worksheet(new_sheet_name)

# Create a new list with the header row included
header_row = ['Rating', 'Review', 'Name', 'Date', 'Review Description', 'Location']
data_list = [header_row] + [[review[col] for col in header_row] for review in reviews]

# Clear the existing values in the sheet
sheet.clear()

# Append the data list to the Google Sheets
sheet.append_rows(data_list)

print("Reviews saved to Google Sheets.")
