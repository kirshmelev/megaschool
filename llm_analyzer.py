import openai
import config

openai.api_key = config.OPENAI_API_KEY

def analyze_product_data(products):
    """
    Use LLM to analyze collected product data.
    Simple analysis: compare prices, suggest best deals.
    """
    if not products:
        return "No data to analyze."

    try:
        prompt = "Analyze the following product data from different marketplaces and provide insights:\n"
        for product in products:
            prompt += f"- {product['source']}: {product['name']} - {product['price']}\n"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in LLM analysis: {e}")
        return "Analysis failed."