import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Other configs if needed
WB_API_KEY = os.getenv('WB_API_KEY')  # If needed
OZON_API_KEY = os.getenv('OZON_API_KEY')