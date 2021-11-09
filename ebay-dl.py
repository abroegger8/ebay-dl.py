import argparse
from typing import Text
import requests
from bs4 import BeautifulSoup
import json
import csv

# Only show 'Sold' items and nothing else
def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.

    >>> parse_itemssold ('38 sold')
    38
    >>> parse_itemssold ('14 watchers')
    0
    >>> parse_itemssold ('Almost gone')
    0
    >>> parse_itemssold ('Last one')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

# Convert shipping cost into cents
def parse_shipping(text):
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if '$' in text:
        numbers = int(numbers)
        return numbers
    elif 'Free' in text:
        numbers = int(0)
        return numbers

# Convert price into cents
def parse_price(text):
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if '$' in text:
        numbers = int(numbers)
        return numbers
    elif 'Free' in text:
        numbers = int(0)
        return numbers

# this if statement says only run the code when the python file is run "normally" (not in doctest)
if __name__ == '__main__':

    # Getting command line arguments
    parser = argparse.ArgumentParser(description='Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    args = parser.parse_args()
    print('args.search_term=', args.search_term)

    # List of all items found in all ebay webpages
    items = []

    # Loop over the ebay webpages
    for page_number in range(1,int(args.num_pages)+1):
        # Build the URL
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=' 
        url += args.search_term 
        url += '&_sacat=0&_pgn'
        url += str(page_number)
        url += '&rt=nc'
        print('url=',url)

        # Download the HTML
        r = requests.get(url)
        status = r.status_code
        print('status=', status)
        html = r.text

        # Process the HTML
        soup = BeautifulSoup(html,  'html.parser')

        # Loop over the items in the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:

            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text

            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns = True

            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)
                print('tag=', tag)

            shipping = None
            tags_shipping = tag_item.select('.s-item__shipping')
            for tag in tags_shipping:
                shipping = parse_shipping(tag.text)

            status = None
            tags_status = tag_item.select('.s-item__subtitle')
            for tag in tags_status:
                status = tag.text

            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)

            item = {
                'name' : name,
                'free_returns' : freereturns,
                'items_sold' : items_sold,
                'shipping' : shipping,
                'status' : status,
                'price' : price,
            }
            items.append(item)

        print('len(tag_items)=', len(tags_items))
        print('len(items)=',len(items)) 

    # Create new file
    filename = args.search_term+'.json'
    with open(filename, 'w', encoding='ascii') as f:
        f.write(json.dumps(items))
    