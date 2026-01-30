import requests
from bs4 import BeautifulSoup
import config

def get_yandex_product_data(product_id):
    """
    Collect product data from Yandex Market.
    Basic scraping.
    """
    try:
        url = f"https://market.yandex.ru/product/{product_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Simplified
        name = soup.find('h1').text.strip() if soup.find('h1') else 'Unknown'
        price = soup.find('span', class_='price').text.strip() if soup.find('span', class_='price') else 'Unknown'

        return {
            'name': name,
            'price': price,
            'source': 'Yandex Market'
        }
    except Exception as e:
        print(f"Error collecting Yandex data: {e}")
        return None