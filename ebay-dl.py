import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv

'''
dictionary keys:
name
price
status
shipping
free_returns
items_sold
'''


def parse_name(text):
    name = ''
    if 'New Listing' in text:
        for char in text[11:]:
            name += char
    else:
        for char in text:
            name += char
    return name

def parse_price(text):
    price = ''
    if 'see price' in text.lower():
        return None
    else:
        for char in text:
            if char in '1234567890':
                price += char
            if char == 't':
                return int(price)
        return int(price)

def parse_ship_cost(text):
    ship_cost = ''
    if 'free' in text.lower():
        ship_cost = 0
        return ship_cost
    else:
        for char in text:
            if char in '1234567890':
                ship_cost += char
        return int(ship_cost)

def parse_items_sold(text):
    numitems = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numitems)
    else:
        return None

parser = argparse.ArgumentParser(description='Download information from eBay and convert to JSON.')
parser.add_argument('search_term')
parser.add_argument('--num_pages', default = 10)
parser.add_argument('--csv', default=False)
args = parser.parse_args()
print('args.search_term=', args.search_term)

items = []

for page_number in range(1, int(args.num_pages)+1):
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + args.search_term + '&_sacat=0&_pgn=' +str(page_number) + '&rt=nc'
    print('url=', url)

    r = requests.get(url)
    status = r.status_code
    print('status=', status)
    html =  r.text

    soup = BeautifulSoup(html, 'html.parser')

    tags_items = soup.select('.s-item')
    for tag_item in tags_items:
        name = None
        tags_name = tag_item.select('.s-item__title')
        for tag in tags_name:
            name = parse_name(tag.text)

        price = None
        tags_price = tag_item.select('.s-item__price')
        for tag in tags_price:
            price = parse_price(tag.text)

        status = None
        tags_status = tag_item.select('.SECONDARY_INFO')
        for tag in tags_status:
            status = tag.text

        shipping = None
        tags_shipping = tag_item.select('.s-item__shipping,.s-item__freeXDays')
        for tag in tags_shipping:
            shipping = parse_ship_cost(tag.text)

        freereturns = False
        tags_freereturns = tag_item.select('.s-item__free-returns')
        for tag in tags_freereturns:
            freereturns = True

        items_sold = None
        tags_itemssold = tag_item.select('.s-item__hotness')
        for tag in tags_itemssold:
            items_sold = parse_items_sold(tag.text)

        item = {
            'name': name,
            'price': price,
            'status': status,
            'shipping': shipping,
            'free_returns': freereturns,
            'items_sold': items_sold,
        }
        items.append(item)

    print('len(tags_items)=', len(tags_items))
    print('len(items)=', len(items))

if args.csv:
    field_names = list(items[0].keys())
    filename = args.search_term+'.csv'
    with open(filename, 'w', encoding='utf-8') as f:
        w = csv.DictWriter(f, field_names)
        w.writeheader()
        w.writerows(items)
else:
    filename = args.search_term+'.json'
    with open(filename, 'w', encoding = 'ascii') as f:
        f.write(json.dumps(items))