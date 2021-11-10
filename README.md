# eBay Scraper Homework 3

## Description of Code
My ebay-dl.py file is programmed with python to download 6 key pieces of information - name, if there are free returns, number of items sold, shipping prices (in cents), condition status, and item price (in cents) - for any eBay item and combine the information into a JSON file.

## How to Run the Code
To run the code for any item on ebay, use the following command in the ebay-dl.py terminal to get a JSON file of information for the chosen item:

```
python3 ebay-dl.py 'item_name' --num_pages=10
```
The code I used to download `kettle.json` :

```
python3 ebay-dl.py 'kettle' --num_pages=10
```

The code I used to download `sunglasses.json` :

```
python3 ebay-dl.py 'sunglasses' --num_pages=10
```

The code I used to download `golf balls.json` :

```
python3 ebay-dl.py 'golf balls' --num_pages=10
```

Last but not least, here is the [link](https://github.com/mikeizbicki/cmc-csci040/tree/2021fall/hw_03) to the course project. 
Thank you for checking out my work :)
