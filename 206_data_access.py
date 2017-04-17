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

class NationalPark(object): # set up location, description, tel_number, site category

	def __init__(self, html_string, current_state):
		
		park_info = html_string.find(class_= "col-md-9 col-sm-9 col-xs-12 table-cell list_left")

		self.name = park_info.find('a').text

		self.description = park_info.find('p').text

		self.site_category = park_info.find('h2').text

		self.state = current_state

	def get_useful_info(self, html_string):
		pass 

class Article(object):

	def __init__(self, html_string):

		self.title = html_string.find('a').text

		self.description = html_string.find('p').text

		self.article_url = html_string.find('a').get('href')

		# article_info = html_string.find(class_ = "FeatureGrid-item col-xs-12")
		# try: 
		# 	smaller_info = html_string.find(class_ = "FeatureGrid-item col-xs-12 col-sm-6")

		# 	self.title = smaller_info.find('h3').text

		# 	self.description = smaller_info.find('p').text

		# 	self.article_url = smaller_info.find('a').get('href')
		# except:
		# 	smaller_info = html_string.find(class_ = "FeatureGrid-item col-xs-12 col-sm-4")

		# 	self.title = smaller_info.find('h3').text

		# 	self.description = smaller_info.find('p').text

		# 	self.article_url = smaller_info.find('a').get('href')

		
'''
	def __str__(self):
		if self.city == "":
			return "{0} is a {1}. Here is a description of the {0}: {2}".format(self.name, self.site_category, self.description)
		else:
			return "{0} is a {1} located in {2}. Here is a description of the {0}: {3}".format(self.name, self.site_category, self.city, self.description)

	def other_info():
		pass 
'''
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

def get_article_html(article_links):
	unique_identifier = "article_html"
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

def get_article_data():
	unique_identifier = "article_data"
	if unique_identifier in CACHE_DICTION:
		print("using cached data")
		req_text = CACHE_DICTION[unique_identifier]
	else:
		print("accessing article data from internet")
		base_url = "https://www.nps.gov/index.htm"
		req_text = requests.get(base_url).text
		print(type(req_text))
		CACHE_DICTION[unique_identifier] = req_text
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return req_text

# Invoke the get_natlparks_data function and save it a variable called html_park_data. Using this html data, create a list of NationalPark objects and save them in a variable called park_objs.

html_park_data = get_natlparks_data()
#print(html_park_data[0])
#print(type(html_park_data[0]))

article_link_data = get_article_links()
#print(article_link_data)

html_article_pages = get_article_html(article_link_data)
#print(html_article_data[0])

html_article_data = get_article_data()
#print(html_article_data)

park_objs = []
repeat_parks = []
for state_html in html_park_data:
	soup = BeautifulSoup(state_html, "html.parser")
	current_state = soup.find(class_ = "ContentHeader").text
	#print(current_state)
	st_parks = soup.find(class_ = "col-md-9 col-sm-12 col-xs-12 stateCol")
	for item in st_parks.find_all(class_= "clearfix"):
		current_obj = NationalPark(item, current_state)
		if current_obj not in repeat_parks:
			repeat_parks.append(current_obj)
			park_objs.append(current_obj)

sorted_park_objs = [park for park in park_objs]
sorted_park_objs = sorted(park_objs, key = lambda x: x.name)
for park in sorted_park_objs:
	#print(park.name, park.state)
	pass

article_objs = []
soup = BeautifulSoup(html_article_data, "html.parser")
all_articles = soup.find(class_ = "Component FeatureGrid")
#print(type(all_articles))
#print(all_articles)

article_list1 = [Article(article) for article in all_articles.find_all(class_ = "FeatureGrid-item col-xs-12 col-sm-6")]
# for article in all_articles.find_all(class_ = "FeatureGrid-item col-xs-12 col-sm-6"):
# 	# article_objs.append(Article(article))

article_list2 = [Article(article) for article in all_articles.find_all(class_ = "FeatureGrid-item col-xs-12 col-sm-4")]

article_objs = article_list1 + article_list2

# for article in all_articles.find_all(class_ = "FeatureGrid-item col-xs-12 col-sm-4"):
# 	article_objs.append(Article(article))

for article in article_objs:
	print(article.description)

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
table_spec += 'Parks (id INTEGER PRIMARY KEY, name TEXT, site_category TEXT, description TEXT, state TEXT)'
cur.execute(table_spec)

for park in sorted_park_objs:
	s1 = 'INSERT OR IGNORE INTO Parks Values(?, ?, ?, ?, ?)'
	park_vals = (None, park.name, park.site_category, park.description, park.state)
	cur.execute(s1, park_vals)

conn.commit()







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