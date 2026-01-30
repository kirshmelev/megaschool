import requests
from bs4 import BeautifulSoup
import config

def get_ozon_product_data(product_id):
    """
    Collect product data from Ozon.
    Basic scraping.
    """
    try:
        url = f"https://www.ozon.ru/product/{product_id}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Simplified extraction
        name = soup.find('h1').text.strip() if soup.find('h1') else 'Unknown'
        price = soup.find('span', class_='price').text.strip() if soup.find('span', class_='price') else 'Unknown'

        return {
            'name': name,
            'price': price,
            'source': 'Ozon'
        }
    except Exception as e:
        print(f"Error collecting Ozon data: {e}")
        return None