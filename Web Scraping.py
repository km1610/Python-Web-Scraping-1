import requests
import csv
from bs4 import BeautifulSoup

def scrape_products(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []

    for product_container in soup.find_all('div', {'class': 's-result-item'}):
        product = {}

        product_url = product_container.find('a', {'class': 'a-link-normal'})
        if product_url:
            product['url'] = product_url['href']
            product['name'] = product_url.text.strip()
        else:
            product['url'] = ''
            product['name'] = ''

        product_price = product_container.find('span', {'class': 'a-offscreen'})
        if product_price:
            product['price'] = product_price.text.strip()
        else:
            product['price'] = ''

        product_rating = product_container.find('span', {'class': 'a-icon-alt'})
        if product_rating:
            product['rating'] = product_rating.text.strip()
        else:
            product['rating'] = ''

        product_reviews = product_container.find('div', {'class': 'a-section a-text-center'})
        if product_reviews:
            product['reviews'] = product_reviews.text.strip()
        else:
            product['reviews'] = ''

        product_description = product_container.find('div', {'class': 'a-section a-spacing-none a-spacing-top-micro'})
        if product_description:
            product['description'] = product_description.text.strip()
        else:
            product['description'] = ''

        product_asin = product_container.find('div', {'data-index': True})
        if product_asin:
            product['asin'] = product_asin['data-asin']
        else:
            product['asin'] = ''

        product_manufacturer = product_container.find('div', {'class': 'a-section a-spacing-none'})
        if product_manufacturer:
            product['manufacturer'] = product_manufacturer.text.strip()
        else:
            product['manufacturer'] = ''

        products.append(product)

    return products

def scrape_pages(pages=20):
    url = "https://www.amazon.in/s?k=bags&page={}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    products = []
    for page in range(1, pages + 1):
        products.extend(scrape_products(url.format(page)))

    return products

def export_to_csv(products):
    fieldnames = ['url', 'name', 'price', 'rating', 'reviews', 'description', 'asin', 'manufacturer']
    filename = 'products.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow(product)


products = scrape_pages()
export_to_csv(products)