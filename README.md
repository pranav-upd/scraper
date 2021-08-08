#    README
scarper.py is a simple scraper that scrapes the data from books.toscrape.com and stores the data
in a csv file for each category. The csv file is of the following format:

product_page_url
universal_ product_code (upc)
title 
price_including_tax
price_excluding_tax
number_available
product_description
category
review_rating
image_url

The scraper also downloads the image fie and stores in the local directory. The name of the file is same as the original name
of the image file.

## REQUIREMENTS 
To run the file, the libraries in the requirements.txt must be installed on the local system. This can ne installed via pip
e.g. pip install beautifulsoup4

You must also have python 3.0 or above installed in your system. If you do not have it installed, you can install it from 
https://www.python.org/downloads/. Instructions are given on installing for each operating system.

## RUNNING

Once you have python and the libraries set up, you can run it using 'python scraper.py'. This will automatically retrieve
the category list and start building the csv files and downloading the images. Make sure to run scaper,py in a subdirectory of
your choice since it retrieves/generates 1000+ files (including images and csv files). It would clutter the desktop very fast, so
please avoid running it on the desktop.

For any queries or feedback, feel free to contact me on pranavupadhyaya51@gmail.com
 
 
