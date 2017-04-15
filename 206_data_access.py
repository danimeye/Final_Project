###### INSTRUCTIONS ###### 





# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import json
import requests
import unittest
import sqlite3
from bs4 import BeautifulSoup
# Begin filling in instructions....


# Create a file to cache the information you retrieve from the internet. Save this in a file called 206finalproj_caching.json. 

CACHE_FNAME = "206finalproj_caching.json"
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}


# Write a function called get_natl_parks_data that retrieves html data for the nation parks/monuments from each state on the National Parks website. Add this html data into your cache file. 
# Save and return your results in a variable called html_park_list, which should represent a list of html strings with info from each park. 

def get_natlparks_data():

	unique_identifier = "natl_parks_data"
	state_codes = ['al','ak','as','az','ca','co','ct','de','dc','fl','ga','gu','hi','id','il','in','ia','ks','ky','la','me',
	'md','ma','mi','mn','ms','mo','mt','ne','nv','nh','nj','nm','ny','nc','nd','mp','oh','ok','or','pa','pr','ri','sc','sd','tn','tx','ut','vt','vi','va','wa','wv','wi','wy']
	html_park_list = []
	if unique_identifier in CACHE_DICTION:
		print("using cached data")
		html_park_list = CACHE_DICTION[unique_identifier]
	else:
		print("accessing park data from internet")
		for code in state_codes:
			base_url = "https://www.nps.gov/state/" + code + "/index.htm"
			html_text = requests.get(base_url)
			#print(html_text.text)
			html_park_list.append(html_text.text)
			# print(html_text.url)
		CACHE_DICTION[unique_identifier] = html_park_list # adding the new data to the cache dictionary
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
		#print(html_park_list[0])
	return html_park_list
		

# Write a function called get_article_links that retrieves the article links on the National Parks Website. These links should specific to each article and will eventually be used to attach to the site's base url to access html data from each article's page. 
# Save and return these links in a variable called article_links, which represent a list of article link-endings. 

def get_article_links(): 

	base_url = "https://www.nps.gov/index.htm"
	req_text = requests.get(base_url).text
	soup = BeautifulSoup(req_text, "html.parser")
	articles = soup.find(class_ = "Component FeatureGrid")
	article_links = []
	for link in articles.find_all('a'):
		article_links.append(link.get('href'))
	return article_links 

# Write a function called get_article_data that receives a list of article links as input. For each of these links, fetch html data and add it to your cache file. 
# Save and return the html data of the articles in a variable called html_article_list, which represent a list of html strings with info from each article.

def get_article_data(article_links):
	unique_identifier = "article_data"
	html_article_list = []
	if unique_identifier in CACHE_DICTION:
		print("using cached data")
		html_article_list = CACHE_DICTION[unique_identifier]
	else:
		print("accessing article data from internet")
		for link in article_links:
			base_url = "https://www.nps.gov" + link
			html_text = requests.get(base_url)
			html_article_list.append(html_text.text)
			print(html_text.url)
		CACHE_DICTION[unique_identifier] = html_article_list # adding the new data to the cache dictionary
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return html_article_list


# Invoke the get_natlparks_data function and save it a variable called html_park_data. Using this html data, create a list of NationalPark objects and save them in a variable called park_objs.

html_park_data = get_natlparks_data()
#print(html_park_data[0])

article_link_data = get_article_links()
#print(article_link_data)

html_article_data = get_article_data(article_link_data)

print(html_article_data[0])
'''
for state_html in html_park_data:
	soup = BeautifulSoup(state_html, html.parser)
	st_parks = soup.find(id = "parkListResult")
	park_objs = []
	for item in st_parks.find_all(class_= "clearfix"):
		park_objs.append(NationalPark(item))

class NationalPark(html_string): # set up location, description, tel_number, site category

	def __init__(self, html_string):
		soup = BeautifulSoup(html_string, html.parser)

		self.name = soup.find(a).text

		self.description = soup.find(p)

		self.site_category = soup.find(h2).text

		#city 
'''

# CREATING DATABASES

conn = sqlite3.connect("national_parks.db")
cur = conn.cursor()

statement = 'DROP TABLE IF EXISTS Parks'
cur.execute(statement)
statement = 'DROP TABLE IF EXISTS States'
cur.execute(statement)
statement = 'DROP TABLE IF EXISTS Articles'
cur.execute(statement)

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Parks (name TEXT PRIMARY KEY, state TEXT, description TEXT, site_category TEXT)'
cur.execute(table_spec)









# WRITE METHOD TO GET TUPLE THAT RETURNS DATA YOU WANT IN YOUR DATA BASE- WILL CALL ON EACH PARK TO LOAD INTO TABLES
		







# Put your tests here, with any edits you now need from when you turned them in with your project plan.


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)

###################### TEST CASES #########################
'''
class TestPlan(unittest.TestCase):
	def test_get_data(self):
		self.assertEqual(type(html_list), type([]), 'Testing that the return value of the get_park_data() function is a list')
	def test_description1(self):
		park1 = NationalPark()
		self.assertEqual(type(park1.description), type(""), 'Testing that the description of the park is a string')
	def test_articleText(self):
		article1 = Article()
		self.assertEqual(type(article1.title), type(""), 'Testing that the title of the article is a string')
	def test_description_list():
		self.assertEqual(type(test_description_list), type([]), 'Testing that the list of national park descriptions, description_list, is a list')
	def test_park_list(self):
		park1 = NationalPark()
		self.assertEqual(type(park_list[0]), type(park1), 'Testing that the first element in the list of park instances, park_list, is a NationalPark object')
	def test_article_list(self):
		article1 = Article()
		self.assertEqual(type(article_list[0]), type(article1), 'Testing that the first element in the list of article instances, article_list, is an Article object')
	def test_mentioned_parks(self):
		self.assertEqual(type(mentioned_parks) type({'state':'park'})
	def test_DB(self):
		conn = sqlite3.connect('natlparks.db')
		cur = conn.cursor()
		cur.execute('SELECT name FROM Parks INNER JOIN States WHERE States.name = 'Florida'')
		result = cur.fetchall()
		self.assertEqual(len(result), 12, 'Testing that the number of national parks in Florida in the database is 12')
		conn.close()
	




## Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)
'''