# Product scraper - UPA course project
This is the solution to the third project of the UPA course on FIT BUT.
The goal of this project is to create a web scraper that will get the links to products and additional product information.

## Creators: Vidím ostře team
- Matěj Konopík (matejkonopik@gmail.com)
- Jakub Ryšánek ()
- Krištof Šiška


## Scraped website
We have decided to scrape digital camera products form the eshop [thecamerastore.com](https://www.thecamerastore.com/).
The exact base link is [here](https://thecamerastore.com/collections/cameras?sort_by=best-selling&filter.p.m.search_filters.category=Compact+Cameras&filter.p.m.search_filters.category=Mirrorless+System+Cameras&filter.v.price.gte=&filter.v.price.lte=). This link applies filters for **Compact cameras** and **Mirrorless system cameras** and sorts the products by **best selling**.

## Resulting TSV data file column description

According to the assignment, the resulting tsv contains URL, product name and current price, plus additional product data.
It was also requested to save the data in a TSV file without headers, which should have been described here.

- `C1`: URL
- `C2`: Product name
- `C3`: Price
- `C4`: Stock status (available, out of stock, etc.)
- `C5`: Continuous shooting speed
- `C6`: Dimensions
- `C7`: ISO range
- `C8`: Lens mount
- `C9`: Power source (battery)
- `C10`: Data card slot(s)
- `C11`: Resolution
- `C12`: Shutter speed
- `C13`: Video resolution
- `C14`: Weight

## Running the scraper
*Expecting linux machine with python 3.8+ environment with pip installed.*

Run the following command for build:
```
./build.sh
```

To extract links:
```
python scrape_urls.py > urls.txt
```

Then to extract data:
```
python scrape_data.py urls.txt > data.tsv
```

The assignment also requires a testing run to print out details for first 10 links.
To see these results, use `run.sh`:
```
./run.sh
```

## Details
The scrape_details saves all the data in memory and then prints it out in the end. This is because we have also implemented a function that saves it directly to a file, using pandas dataframe. This could be potentially useful if we need to further work with a dataframe, but could be a downside, as the program could quite memory-hungry. This is a feature, not a bug ;).
