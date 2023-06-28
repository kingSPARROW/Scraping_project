import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

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
# Create a new workbook and select the active sheet
workbook = Workbook()
sheet = workbook.active

# Write the headers to the sheet
headers = ['Rating', 'Review', 'Name', 'Date', 'Review Description', 'Location']
sheet.append(headers)

# Write the reviews to the sheet
for review in reviews:
    row_data = [review['Rating'], review['Review'], review['Name'], review['Date'], review['Review Description'], review['Location']]
    sheet.append(row_data)

# Save the workbook to an Excel file
workbook.save('youtube.xlsx')

print("Reviews saved to youtube.xlsx")
