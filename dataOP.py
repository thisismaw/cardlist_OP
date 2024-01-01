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

    # Extracting data from 'infoCol' and 'cardName' classes
    info_texts = [info.get_text(strip=True) for info in soup.find_all(class_='infoCol')]
    card_names = [name.get_text(strip=True) for name in soup.find_all(class_='cardName')]

    # Extracting data from 'frontCol' and 'backCol' classes
    front_data = [{'text': front.get_text(strip=True), 'img_src': get_img_src(front)} for front in soup.find_all(class_='frontCol')]
    back_data = [get_backcol_data(back) for back in soup.find_all(class_='backCol')]

    return {
        "infoCol": info_texts,
        "cardName": card_names,
        "frontCol": front_data,
        "backCol": back_data
    }

# MongoDB setup
client = MongoClient("mongodb+srv://admin:8883mb@onepiece.c2dddqy.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB URI
db = client["OnePiece"]  # Replace with your database name
collection = db["OPdb"]  # Replace with your collection name

# List of URLs to scrape
urls = [
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
    aggregated_data['infoCol'].extend(scraped_data['infoCol'])
    aggregated_data['cardName'].extend(scraped_data['cardName'])
    aggregated_data['frontCol'].extend(scraped_data['frontCol'])
    aggregated_data['backCol'].extend(scraped_data['backCol'])

# Insert aggregated data into MongoDB
collection.insert_one(aggregated_data)

print("Aggregated data has been successfully inserted into MongoDB.")