import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

books_data = []

# Loop through all 50 pages
for page in range(1, 51):
    print(f"Scraping page {page} of 50...")
    
    url = BASE_URL.format(page)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to load page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        # Book Title
        title = book.h3.a["title"]

        # Price
        price = book.find("p", class_="price_color").text.strip()

        # Rating (One, Two, Three, Four, Five)
        rating = book.find("p")["class"][1]

        # Availability
        availability = book.find("p", class_="instock availability").text.strip()

        books_data.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Availability": availability
        })

# Convert to DataFrame
df = pd.DataFrame(books_data)

# Save to JSON
df.to_json("books_all_50_pages.json", orient="records", indent=4)

print("✅ Scraping completed!")
print(f"📚 Total books scraped: {len(df)}")
print("📁 File saved as books_all_50_pages.json")
