import re
from bs4 import BeautifulSoup
import mechanicalsoup
import csv



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
   We use the regex '\s\s', to match with the double space in the data. Then we use positive lookahead and the * function
   to match with all the characters between the tags, and replace it with a null character, hence remmoving the tags and the spacing
   which makes it easier to process the data.
   """
   regex_output = re.sub('|\s\s|<(?=.)(.*?)>','', input_data)
   """
   Now we first have the non html characters to be commas sorted, then we join the space seperated words usin '-'
   """
   regex_output = re.sub('(\n)+',',', regex_output)
   regex_output = re.sub('\s','-', regex_output)
   """
   Now we select a subsection of the output, ignoring the ',books,' in the start and the ',' in the end of the previous output and we combine them to a list.
   Hence, the function is complete.
   """
   regex_output = regex_output[7:(len(regex_output)-1)]
   return regex_output.split(',')  

def category_list(category):
   """
   The category_list function outputs 3 different lists i.e, the title list, the price list and the availability_;ist
   Usage of function : list1, list2, list3 = category_list('category')
   """
   browser = mechanicalsoup.Browser()
   title_list = []
   price_list = []
   availability_list = []
   image_list = []
   browser_instance = browser.get(f'https://books.toscrape.com/catalogue/category/books/{category}/index.html')
   print(browser_instance)
   browser_output = browser_instance.soup.find_all('h3')
   # Now we use the the positive lookaahead to extract the title from the <title> tag
   # We use the positive lookahead (?=.) for all characters and use select all character (.*) to select character to
   # the required parameters. Here we first select characters from <h3> to 'title="' and second one matches
   # the outer tag characters and the subsequent regex match the special characters '</a>, '</h3>' and '&amp;'
   # Then we return the list of titles from a specific category
   for i in browser_output:
      title = re.sub('<h3(?=.)(.*?)title="|">(?=.)(.*?)<|/a>|</h3>|&amp;','', str(i))
      title_list.append(title)
      
   browser_output = browser_instance.soup.find_all('p',{'class':'price_color'})
   # Here we use the positive lookahead and the * function to match all characters between
   # the tags and replace it with the null character, hence, extracting the price
   for i in browser_output:
      price = re.sub('<(?=.)(.*?)>','',str(i))
      price_list.append(price)  

   browser_output = browser_instance.soup.find_all('p',{'class':'instock availability'})
   # Here we use the positive lookahead and the * function to match all characters between
   # the tags and we also match with the double space character '\s\s' and the newline character '\n'
   # and replace it with the null character ''
   for i in browser_output:
      availability = re.sub('<(?=.)(.*?)>|\s\s|\n','',str(i))
      availability_list.append(availability)
   

   browser_output = browser_instance.soup.find_all('div',{'class':'image_container'})
   # Here we use the positive lookahead with the * function to initially match all the characters
   # between div. Then we match all the characters from  '<a href="' to 'src="'. Then we match the characters
   # '</a>','/> and the newline character '\n' and replace it with the null character '' 
   for i in browser_output:
      image_src = re.sub('<div(?=.)(.*?)>|<a href="(?=.)(.*?)src="|"/></a>|</div>|\n','',str(i))
      image_src = ('https://books.toscrape.com/'+ image_src[12:])
      image_list.append(image_src)

   return title_list, price_list, availability_list, image_list
   
   
"""
Now we declare the lists we are going to use, which are [titles], [prices] and [availability].
We also declare the categories list, which gets the categories list from the book_categories
function. We declare the books_dict dictionary and we enter the first entry as 'Title', 'Price'
and 'Availability'.
"""
titles = []
prices = []
availability = []
images = []
categories = book_categories()
books_dict = {'Key': ['Title', 'Price', 'Availability', 'Image Source']}
#Category number is the number which is assigned to a category
#example: https://books.toscrape.com/catalogue/category/books/travel_2/index.html
#where 2 is the category number assigned to travel. It is ascending in order and
# increments by 1, per category and starts from 2.

category_number = 2
book_number = 1
for i in categories:  
   titles, prices, availability, images = category_list(f'{i.lower()}_{category_number}')
   category_number += 1
   for j in range(1, (len(titles))):
      dictionary_list = [titles[j], prices[j], availability[j], f'{book_number}.jpg']
      #Here we set up the mechanicalsoup browser and we request the browser to get the image data
      #and we save the image data using the open function and save the image as {book_number}.jpg
      #associated with each book_number
      browser = mechanicalsoup.Browser()
      browser_instance = browser.get(images[j])
      with open(f'{book_number}.jpg', 'wb') as f:
         f.write(browser_instance.content)
       
      books_dict[f'{book_number}'] = dictionary_list
      book_number += 1
# In the end we write the dictionary to a csv file. First we set up the csv_writer.
# Then we iterate over the keys and we write the pair of key and the key value.
# which here is in a list. Hence we write the complete dictionary data to the csv file.
with open('scraper_data.csv', 'w') as csv_file:
   writer = csv.writer(csv_file)
   for key in books_dict.keys():
      writer.writerow([key] + books_dict[key])

      
   






    
    
    
    
        


