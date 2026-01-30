import requests
from bs4 import BeautifulSoup
import config

def get_wb_product_data(product_id):
    """
    Collect product data from Wildberries.
    For MVP, basic scraping of product page.
    """
    try:
        url = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract basic info - this is simplified, actual selectors may vary
        name = soup.find('h1', class_='product-title').text.strip() if soup.find('h1', class_='product-title') else 'Unknown'
        price = soup.find('span', class_='price').text.strip() if soup.find('span', class_='price') else 'Unknown'

        return {
            'name': name,
            'price': price,
            'source': 'Wildberries'
        }
    except Exception as e:
        print(f"Error collecting WB data: {e}")
        return None