import re
from bs4 import BeautifulSoup
import mechanicalsoup
import csv

#TODO
#Get Product url
#Get Price before tax
#Get Price after tax
#Get number_available
#get_product_description
#get universal product code (UPC)


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
   The category_list function outputs 7 different lists i.e, the title list, the price list(since the price pre-tax and
   post tax are the same for every book, it outputs the rate on the category page), the availability_list,
   the image_list, the ratings list, the product_page link and the list of universal product code.
   Usage of function : list1, list2, list3,...,list7 = category_list('category')
   """
   browser = mechanicalsoup.Browser()
   title_list = []
   price_list = []
   image_list = []
   ratings_list = []
   producturl_list = []
   pdescription_list = []
   upc_list = []
   pretax_list = []
   posttax_list = []
   availability_list = []
   browser_instance = browser.get(f'https://books.toscrape.com/catalogue/category/books/{category}/index.html')
   print(browser_instance)
   # First we try and find out the number of results for pagination. We use a simple algoritm for this.
   # We first extract the number using regex by marking the non digits and replacing the number. Then we
   # select the number and find the number of books. Since each page has only 20 books. We divide the
   # number of books by 20 and we check if the remainder is 0. If the remainder is 0, then the minimum
   # number of page is equal to the number of pages. If the remainder is greater than 0, then the total
   # number of pages is equal to the minimum number of pages + 1
   browser_output = browser_instance.soup.find_all('strong')
   for i in browser_output:
      book_results = re.sub('\D|(\n)+','',str(i))
      if book_results != '':
         break
   book_results = int(book_results)
   minimum_pages = int(book_results/20)
   if (book_results%20) != 0:
      book_pages = minimum_pages + 1
   else:
      book_pages = minimum_pages
   for h in range(1, (book_pages+1)):
      if h >= 2:
         browser_instance = browser.get(f'https://books.toscrape.com/catalogue/category/books/{category}/page-{h}.html')
      else:
         pass
      browser_output = browser_instance.soup.find_all('h3')
      # Now we use the the positive lookahead to extract the title from the <title> tag
      # We use the positive lookahead (?=.) for all characters and use select all character (.*) to select character to
      # the required parameters. Here we first select characters from <h3> to 'title="' and second one matches
      # the outer tag characters and the subsequent regex match the special characters '</a>, '</h3>' and '&amp;'
      # Then we return the list of titles from a specific category
      for i in browser_output:
         title = re.sub('<h3(?=.)(.*?)title="|">(?=.)(.*?)<|/a>|</h3>|&amp;','', str(i))
         title_list.append(title)
      
      
      browser_output = browser_instance.soup.find_all('div',{'class':'image_container'})
      # Here we use the positive lookahead with the * function to initially match all the characters
      # between div. Then we match all the characters from  '<a href="' to 'src="'. Then we match the characters
      # '</a>','/> and the newline character '\n' and replace it with the null character '' 
      for i in browser_output:
         image_src = re.sub('<div(?=.)(.*?)>|<a href="(?=.)(.*?)src="|"/></a>|</div>|\n','',str(i))
         image_src = ('https://books.toscrape.com/'+ image_src[12:])
         image_list.append(image_src)
         
      browser_output = browser_instance.soup.find_all('p',{'class':'star-rating'})
      #Here we try and extract the ratings. In order to do thiswe first match the <i> tag.
      #Then we match from the <p class="star-rating to the final apostrophe and tag ">.
      # Then we match the characters '</p>' and the space character '\s'
      for i in browser_output:
         ratings = re.sub('<i(?=.)(.*?)/i>|<p class="star-rating |">|</p>|\s','',str(i))
         ratings_list.append(ratings)

      browser_output = browser_instance.soup.find_all('h3')
      # Here we first filter out the special characters '/a>', 'h3' tags, and '<a href="', tags respectively.
      # then we use positive lookahead around the title tag select all the characters between title and '"'
      # Similary then we use positive lookahead to select all the characters between '>' and '<' tags
      # Leaving us with the product page url
      for i in browser_output:
         product_url = re.sub('/a>|<h3>|</h3>|" title="(?=.)(.*?)"|>(?=.)(.*?)<|<a href="|(../../../)+|\s','',str(i))
         producturl_list.append(product_url)
      for j in producturl_list:
      #Here we first extract the product description by first etting the data from the p tag (get_text method)
      #Then we get the universal product code, pre and post tax rates and then we extract the numbers from
      #the availability column
         browser_instance = browser.get(f'https://books.toscrape.com/catalogue/{j}')
         #We filter out the non-ascii characters by matching 0 or more non-ascii characters
         if browser_instance.soup.find('p', class_=None) == None:
            pdescription_list.append(' ')
         else:
            pdescription_list.append(re.sub('[^\x00-\x7F]*',' ',browser_instance.soup.find('p', class_=None).get_text()))
         if browser_instance.soup.find('td') == None:
            upc_list.append(' ')
            pretax_list.append(' ')
            posttax_list.append(' ')
            availability_list.append(' ')
         else:
            upc_list.append(browser_instance.soup.find_all('td')[0].text)
            pretax_list.append(browser_instance.soup.find_all('td')[2].text)
            posttax_list.append(browser_instance.soup.find_all('td')[3].text)
            availability_list.append(re.sub('\D|\s','', browser_instance.soup.find_all('td')[5].text))   
   #Finally we output the lists      
   return producturl_list, upc_list, title_list, pretax_list, posttax_list, availability_list, pdescription_list, ratings_list, image_list






"""
Now we declare the lists we are going to use, which are [titles], [prices] and [availability].
We also declare the categories list, which gets the categories list from the book_categories
function. We declare the books_dict dictionary and we enter the first entry as 'Title', 'Price'
,'Availability', 'Images', 'Ratings', 'Product_link' and 'UPC (Univrsal product code)'.
"""
product_url = []
upc = []
titles = []
pre_tax = []
post_tax = []
availability = []
pdescription = []
ratings = []
images = []
print('Starting scraper...')
categories = book_categories()
books_dict = {'Key': ['Product Url','Universal Product Code','Title','Price (excl. tax)','Price (incl. tax)','Number Available','Product Description','Category','Ratings', 'Image Source']}
#Category number is the number which is assigned to a category
#example: https://books.toscrape.com/catalogue/category/books/travel_2/index.html
#where 2 is the category number assigned to travel. It is ascending in order and
# increments by 1, per category and starts from 2.

category_number = 2

for i in categories:
   book_number = 1
   product_url, upc, titles, pre_tax, post_tax, availability, pdescription, ratings, images = category_list(f'{i.lower()}_{category_number}')
   for j in range((len(titles))):
      dictionary_list = [f'https://books.toscrape.com/catalogue/{product_url[j]}', upc[j], titles[j], pre_tax[j], post_tax[j], availability[j], pdescription[j], i.lower(), ratings[j], images[j]]
      #Here we set up the mechanicalsoup browser and we request the browser to get the image data
      #and we save the image data using the open function and save the image as {book_number}.jpg
      #associated with each book_number
     
      browser = mechanicalsoup.Browser()
      browser_instance = browser.get(images[j])
      with open(f'{(images[j])[45:]}.jpg', 'wb') as f:
         f.write(browser_instance.content)
      
      books_dict[f'{book_number}'] = dictionary_list
      book_number += 1
# In the end of each loop, we write the dictionary to a csv file. First we set up the csv_writer.
# Then we iterate over the keys and we write the pair of key and the key value.
# which here is in a list. Hence we write the complete dictionary data to the csv file.
   with open(f'{i.lower()}_{category_number}.csv', 'w') as csv_file:
      writer = csv.writer(csv_file)
      for key in books_dict.keys():
         writer.writerow([key] + books_dict[key])
   books_dict.clear()
   books_dict = {'Key': ['Product Url','Universal Product Code','Title','Price (excl. tax)','Price (incl. tax)','Number Available','Product Description','Category','Ratings', 'Image Source']}  
   category_number += 1
print('Done')   
     
   






    
    
    
    
        


