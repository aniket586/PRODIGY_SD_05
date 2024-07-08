import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    # Add more user agents if needed
]

def scrape_amazon(url):
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }
    
    # Send a GET request to the URL
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find product information
    products = []
    for item in soup.select('.s-result-item'):
        name_elem = item.select_one('.a-size-medium')
        price_elem = item.select_one('.a-price .a-offscreen')
        rating_elem = item.select_one('.a-icon-alt')
        
        name = name_elem.text.strip() if name_elem else None
        price = price_elem.text.strip() if price_elem else None
        rating = rating_elem.text.strip() if rating_elem else None
        
        if name and price and rating:
            products.append({
                'Name': name,
                'Price': price,
                'Rating': rating
            })

    return products

def save_to_csv(products, filename):
    df = pd.DataFrame(products)
    save_path = os.path.join(os.getcwd(), filename)  # Get the full path to the CSV file
    df.to_csv(save_path, index=False)
    print(f"Data saved to {save_path}")

if __name__ == "__main__":
    url = input("Please enter the URL to scrape: ")
    products = scrape_amazon(url)
    if products:
        filename = input("Please enter the filename to save the data (with .csv extension): ")
        save_to_csv(products, filename)
    else:
        print("No products found.")
