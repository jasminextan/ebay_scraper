# [Project 3](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03) for CM-CSCI 40: Ebay Scraper

*Introduction*

**Project Goal:**

The goal of this project was to create code that could create a JSON/CSV file based on eBay search results. The file includes the following data:

1. Name
1. Price
1. Status
1. Shipping Cost
1. Free Return Status
1. Number of Items Sold

**Learning objectives:**

1. understand how web scraping works
1. complete a python project entirely on your own (no starter code!)
1. integrate python knowledge with HTML knowledge+JSON knowledge

*How to Run the Code*

Use the following code to run my code if you have an item you'd like to search for:

```
$ python3 ebay-dl.py 'putyoursearchhere'
```
If you want the the return in a .csv format:
```
$ python3 ebay-dl.py 'putyoursearchhere' --csv=True
```
The default code will return 10 pages of results, but if you want less, use the following code:
```
$ python3 ebay-dl.py 'putyoursearchhere' --num_pages=integer
```

Thanks for checking out my code!