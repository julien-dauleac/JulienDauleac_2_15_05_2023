import requests
from bs4 import BeautifulSoup
import csv

# URL de la page à extraire
url = 'http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html'

# Envoi de la requête HTTP
response = requests.get(url)

# Vérification du statut de la requête
if response.status_code == 200:
    # Création de l'objet BeautifulSoup pour l'analyse HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraction des données nécessaires
    product_page_url = url
    upc = soup.find('td', text='UPC').find_next_sibling('td').text
    title = soup.find('h1').text
    price_including_tax = soup.find('td', text='Price (incl. tax)').find_next_sibling('td').text[1:]
    price_excluding_tax = soup.find('td', text='Price (excl. tax)').find_next_sibling('td').text[1:]
    number_available = soup.find('td', text='Availability').find_next_sibling('td').text.strip()
    product_description = soup.find('div', {'id': 'product_description'}).find_next('p').text
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    review_rating = soup.find('p', class_='star-rating')['class'][1]
    image_url = soup.find('div', class_='item active').find('img')['src']

    # Création de la liste des données extraites
    data = [product_page_url, upc, title, price_including_tax, price_excluding_tax,
            number_available, product_description, category, review_rating, image_url]

    # Enregistrement des données dans un fichier CSV
    with open('data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['product_page_url', 'upc', 'title', 'price_including_tax',
                         'price_excluding_tax', 'number_available', 'product_description',
                         'category', 'review_rating', 'image_url'])
        writer.writerow(data)

    print("Les données ont été extraites et enregistrées dans le fichier 'data.csv'.")
else:
    print("La requête HTTP a échoué.")