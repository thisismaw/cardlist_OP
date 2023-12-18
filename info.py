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

# MongoDB Atlas connection URI
atlas_connection_uri =  "mongodb+srv://admin:8883mb@onepiece.c2dddqy.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(atlas_connection_uri)

# Select your database
db = client['OnePiece']

# Select your collection
collection = db['op06']

# URL to scrape
url = 'https://asia-en.onepiece-cardgame.com/cardlist/?series=556106'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extracting data from 'infoCol' and 'cardName' classes
info_texts = [info.get_text(strip=True) for info in soup.find_all(class_='infoCol')]
card_names = [name.get_text(strip=True) for name in soup.find_all(class_='cardName')]

# Extracting data from 'frontCol' and 'backCol' classes
front_data = [{'text': front.get_text(strip=True), 'img_src': get_img_src(front)} for front in soup.find_all(class_='frontCol')]
back_data = [get_backcol_data(back) for back in soup.find_all(class_='backCol')]

# Combine or process the data as needed
data = {
    "infoCol": info_texts,
    "cardName": card_names,
    "frontCol": front_data,
    "backCol": back_data
}

# Inserting the data into MongoDB
collection.insert_one(data)

print("Data inserted into MongoDB")
