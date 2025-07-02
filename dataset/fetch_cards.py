import json

import requests
from ratelimit import limits
from tenacity import retry, wait_random

@limits(calls=5, period=60)
def get_bulk_cards()-> list[str] | None:
    """
    Gets bulk rulings data from Scryfall's public API and returns rules text as an array of sentences. Method is rate limited on client side
    to avoid exceeding Scryfall API rates.
    :return: the embeddings.
    """
    url = "https://api.scryfall.com/bulk-data/default-cards"
    result = requests.get(url)
    if result.status_code == 200:
        result = result.json()
        print("Getting file from " + result['download_uri'])
        file_response = requests.get(result['download_uri'])
        if file_response.status_code == 200:
            content = json.loads(file_response.content)
            file = open("cards.json","w")
            json.dump(content,file)
            return content
        else:
            raise RuntimeError("Request returned code " + str(file_response.status_code))
