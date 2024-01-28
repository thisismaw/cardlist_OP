import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def get_img_src(element):
    """ Function to get image source """
    img_tag = element.find('img')
    return img_tag['src'] if img_tag else None

def get_backcol_data(element):
    """ Function to get data from each subclass in backCol """
    subclass_data = {}
    for subclass in element.find_all(class_=True):
        # Exclude 'backCol' class and avoid duplicates
        classes = set(subclass.get('class')) - {'backCol'}
        for cls in classes:
            subclass_data[cls] = subclass.get_text(strip=True)
    return subclass_data

def scrape_data(url):
    """ Function to scrape data from a single URL """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    info_texts = [info.get_text(strip=True) for info in soup.find_all(class_='infoCol')]
    card_names = [name.get_text(strip=True) for name in soup.find_all(class_='cardName')]
    front_data = [{'text': front.get_text(strip=True), 'img_src': get_img_src(front)} for front in soup.find_all(class_='frontCol')]
    back_data = [get_backcol_data(back) for back in soup.find_all(class_='backCol')]

    return {
        "infoCol": info_texts,
        "cardName": card_names,
        "frontCol": front_data,
        "backCol": back_data
    }

def card_exists(collection, card_name):
    """ Check if a card with the given name already exists in the database """
    return collection.count_documents({"cardName": card_name}) > 0

# MongoDB setup
client = MongoClient("mongodb+srv://admin:8883mb@onepiece.c2dddqy.mongodb.net/?retryWrites=true&w=majority")
db = client["OnePiece"]
collection = db["OPdb"]

# List of URLs to scrape
urls = [
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556201',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556106',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556105',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556104',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556103',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556102',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556101',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556013',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556012',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556011',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556010',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556009',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556008',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556007',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556006',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556005',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556004',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556003',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556002',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556001',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556701',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556901',
    'https://asia-en.onepiece-cardgame.com/cardlist/?series=556801'
]

# Dictionary to hold aggregated data
aggregated_data = {
    "infoCol": [],
    "cardName": [],
    "frontCol": [],
    "backCol": []
}

# Scrape data and aggregate
for url in urls:
    scraped_data = scrape_data(url)
    for i, card_name in enumerate(scraped_data['cardName']):
        if not card_exists(collection, card_name):
            aggregated_data['infoCol'].append(scraped_data['infoCol'][i] if i < len(scraped_data['infoCol']) else None)
            aggregated_data['cardName'].append(card_name)
            aggregated_data['frontCol'].append(scraped_data['frontCol'][i] if i < len(scraped_data['frontCol']) else None)
            aggregated_data['backCol'].append(scraped_data['backCol'][i] if i < len(scraped_data['backCol']) else None)

# Insert aggregated data into MongoDB as a single document
if aggregated_data['cardName']:  # Check if there is any new data
    collection.insert_one(aggregated_data)
    print("New unique data inserted into MongoDB.")
else:
    print("No new data to insert.")
