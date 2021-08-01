import re
from bs4 import BeautifulSoup
import mechanicalsoup
import csv


#book_data = {}
def book_categories():
   # First we get the data using MechanicalSoup by creating a browser instance and then using the browser.get() function to
   # retrieve the data
   browser = mechanicalsoup.Browser()
   browser_instance = browser.get("https://books.toscrape.com/index.html")
   browser_output = browser_instance.soup.find_all('div',{'class':'side_categories'})
   # we have to iterate over the browser_output since the data is contained in a list and we change the data type to
   # string since it is easier to apply regex on a striing object.
   for i in browser_output:
      input_data = str(i)
   """
   totext is a function that takes input with both html and non html string and outputs only the non html strings in a list
   totext uses regex in order filter the non html data from html. The regex we use here is defined by two parts. The first
   part is \s\s which selects the double space region since \s the the regex code for space. Then we simultaneously use another
   regex code which we seperate from our first (\s\s) regex code by an or function (|). The second regex uses the positive lookahead
   and negative lookahead. Positive lookahead and negative lookahead can be referenced at "https://www.regular-expressions.info/lookaround.html"
   We use the positive lookahead (<(?=.) where '.' references all character and '<' is the character after the positive lookahead matches.
   It matches  '<'. Similarly, we use negative lookahead >(?!.) where it matches only '>'. Then in between we use (.*?) which matches all the terms between
   the two lookaheads.
   """
   regex_output = re.sub('|\s\s|<(?=.)(.*?)>','', input_data)
   """
   Now we first have the non html characters to be commas sorted, then we join the space seperated words usin '-'
   """
   regex_output = re.sub('(\n)+',',', regex_output)
   regex_output = re.sub('\s','-', regex_output)
   """
   Now we select a subsection of the output, ignoring the commas in the start and the end of the previous output and we combine them to a list.
   Hence, the function is complete.
   """
   regex_output = regex_output[1:(len(regex_output)-1)]
   return regex_output.split(',')  

def title_list(category):
   """
   Initially, we first initialize mechanicalsoup and extract the titles from the respective category page
   then we declare an empty list "title_list" where the the titles are stored and returned by the function
   """
   browser = mechanicalsoup.Browser()
   title_list = []
   browser_instance = browser.get(f'https://books.toscrape.com/catalogue/category/books/{category}/index.html')
   browser_output = browser_instance.soup.find_all('h3')
   # Now we use the the positive lookaahead and negative lookahead to extract the title from the <title> tag
   # We use the positive lookahead (?=.) for all characters and use select all character (.*) to select character to
   # the required parameters. Here we first select characters from <h3> to 'title="' and second one matches
   # the outer tag characters and the subsequent regex match the special characters '</a>, '</h3>' and '&amp;'
   # Then we return the list of titles from a specific category
   for i in browser_output:
      title = re.sub('<h3(?=.)(.*?)title="|">(?=.)(.*?)<|/a>|</h3>|&amp;','', str(i))
      title_list.append(title)
   return title_list

def price_list(category): 
 browser = mechanicalsoup.Browser()
 price_list = []
 browser_instance = browser.get(f'https://books.toscrape.com/catalogue/category/books/{category}/index.html')
 browser_output = browser_instance.soup.find_all('p',{'class':'price_color'})
 for i in browser_output:
    price = re.sub('<(?=.)(.*?)>','',str(i))
    price_list.append(price)
 return price_list   

def availability_list(category):
 browser = mechanicalsoup.Browser()
 availability_list = []
 browser_instance = browser.get(f'https://books.toscrape.com/catalogue/category/books/{category}/index.html')
 browser_output = browser_instance.soup.find_all('p',{'class':'instock availability'})
 for i in browser_output:
    availability = re.sub('<(?=.)(.*?)>|\s\s|\n','',str(i))
    availability_list.append(availability)
 return availability_list   







    
    
    
    
        


