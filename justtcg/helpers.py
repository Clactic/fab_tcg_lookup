import config
import requests

def chunk_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# API request helper with error handling
def api_request(endpoint, method="GET", params=None, json_data=None):
    headers = {"X-API-Key": config.API_KEY}
    url = f"{config.BASE_URL}/{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        else:  # POST
            response = requests.post(url, headers=headers, json=json_data)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        if hasattr(e, "response") and e.response:
            try:
                error_data = e.response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error status code: {e.response.status_code}")
                print(f"Error text: {e.response.text}")
        return None


# Track price history for your collection
def track_collection_prices(collection):
    # print("Tracking prices for your collection...")

    # We'll store our results here
    results = []

    # Make batch request for all cards in collection
    response_data = api_request("cards", method="POST", json_data=collection)

    if not response_data:
        return []

    # Process the results
    for item in response_data["data"]:
        card_data = {
            "tcgplayerid": item["tcgplayerId"],
            "name": item["name"],
            "set": item["set"],
            "cardid": item["number"],
            "rarity": item["rarity"],
            "condition": item["variants"][0]["condition"],
            "printing": item["variants"][0]["printing"],
            "current_price": item["variants"][0]["price"],
            "price_delta_7d(%)": item["variants"][0]["priceChange7d"],
            "last_updated": item["variants"][0]["lastUpdated"],
        }
        results.append(card_data)

        # Print the details
        # print(
        #     f"{card_data['name']} ({card_data['condition']}, {card_data['printing']})"
        # )
        # print(f"  Current price: ${card_data['current_price']:.2f}")

    return results

