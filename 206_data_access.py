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
from re import sub
from decimal import Decimal
from bs4 import BeautifulSoup
# Begin filling in instructions....

# Define a class called NationalPark that accepts an HTML formatted string and the state name of the park as input. Use BeautifulSoup to parse through the html data 
# in order to correctly assign values to instance variables. Instance variables for this class should include the park's name, description, category, and state. The class should
# also include a method that will define how the park will be represented when printed to the user. It should make use of each of the instance variables.

class NationalPark(object): # set up location, description, tel_number, site category
	def __init__(self, html_string, current_state):
		
		park_info = html_string.find(class_= "col-md-9 col-sm-9 col-xs-12 table-cell list_left")

		self.name = park_info.find('a').text

		self.description = park_info.find('p').text

		self.site_category = park_info.find('h2').text

		self.state = current_state

	def __str__(self):
		return "{0} is a {1} located in {2}. Here is a description of the {0}: {3}".format(self.name, self.site_category, self.state, self.description)

	def get_useful_info(self, html_string):
		pass 

# Define a class called Article that accepts an HTML formatted string (representing one article on the National Parks' home page) as input. Use BeautifulSoup to parse through the html data
# in order to correctly assign values to instance variables. Instance variables for this class should include the article' title, description, and the url to search it.

class Article(object):
	def __init__(self, html_string):

		self.title = html_string.find(class_ = "Feature-title carrot-end").text

		self.description = html_string.find('p').text

		self.article_url = html_string.find('a').get('href')

class State(object):
	def __init__(self, html_string, current_state):
	
		state_info = html_string.find_all("li")
		#print(type(state_info))

		if " Visitors to National Parks" in state_info[1].text:
			self.visitors = state_info[1].find('strong').text
		else:
			self.visitors = 0
		#print(type(self.visitors))

		if " Economic Benefit from National Park Tourism »" in state_info[2].text:
			self.econ_benefit = state_info[2].find('strong').text
		else:
			self.econ_benefit = 0
		#self. econ_benefit = int(text_benefit)
		#self.econ_benefit = Decimal(sub(r'[^\d]', '', text_benefit))

		if " of Rehabilitation Projects Stimulated by Tax Incentives (since 1995) »" in state_info[3].text:
			self.tax_projects = state_info[3].find('strong').text
		else:
			self.tax_projects = 0
		
		self.name = current_state	

# Create a file to cache the information you retrieve from the internet. Save this in a file called 206finalproj_caching.json. 

CACHE_FNAME = "206finalproj_caching.json"
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}


# Write a function called get_natl_parks_data that retrieves html data for the nation parks/monuments from each state on the National Parks website. Add this html data to your cache file. 
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

# Write a function called get_article_html that receives a list of article links as input. For each of these links, fetch html data and add it to your cache file. 
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

# Write a function called get_article_data that retrieves html data of the articles on the National Parks homepage. Add this html data to your cache file. 
# Save and return the html data of the articles in a variable called html_articles, which represents the html data of the National Parks homepage. 
def get_article_data():
	unique_identifier = "article_data"
	if unique_identifier in CACHE_DICTION:
		print("using cached data")
		html_articles = CACHE_DICTION[unique_identifier]
	else:
		print("accessing article data from internet")
		base_url = "https://www.nps.gov/index.htm"
		html_articles = requests.get(base_url).text
		print(type(html_articles))
		CACHE_DICTION[unique_identifier] = html_articles
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return html_articles


# Invoke the get_natlparks_data function and save it to a variable called html_park_data.
html_park_data = get_natlparks_data()

# Invoke the get_article_links function and save it to a variable called article_link_data. 
article_link_data = get_article_links()

# Using article_link_data, invoke the get_aticle_html function and save it to a variable called html_article_pages. 
html_article_pages = get_article_html(article_link_data)

# Invoke the get_article_data function and save it to a variable called html_article_data. 
html_article_data = get_article_data()

# Using the information stored in html_park_data, create a list of NationalPark objects and save them in a variable called park_objs.
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

# Sort the list of park objects alphabetically by name and save the new list in a variable called sorted_park_objs. 
sorted_park_objs = [park for park in park_objs]
sorted_park_objs = sorted(park_objs, key = lambda x: x.name)
#print(sorted_park_objs[-1])

state_objs = []
for state_html in html_park_data:
	soup = BeautifulSoup(state_html, "html.parser")
	current_state = soup.find(class_ = "ContentHeader").text
	state_info = soup.find(class_ = "col-md-3 col-sm-12 col-xs-12 stateCol stateCol-right")
	state_objs.append(State(state_info, current_state))

# for st in state_objs:
# 	print(st.econ_benefit)
#print(type(state_info))
# Using the information stored in html_article_data, create a list of Article objects and save them in a variable called article_objs. 
article_objs = []
soup = BeautifulSoup(html_article_data, "html.parser")
all_articles = soup.find(class_ = "Component FeatureGrid")
article_list1 = [Article(article) for article in all_articles.find_all(class_ = "FeatureGrid-item col-xs-12 col-sm-6")]
article_list2 = [Article(article) for article in all_articles.find_all(class_ = "FeatureGrid-item col-xs-12 col-sm-4")]

article_objs = article_list1 + article_list2


# Create a database file called national_parks.db. In the database, you will make three tables called Parks, Articles, and States as follows:

# table Parks, with columns:
# - id (representing the default id settings- this column should be the PRIMARY KEY)
# - name (containing the string that represents the national park's name)
# - site_category (containing the string that represents the type of national park)
# - description (containing the description of the park)
# - state (containing the name of the state the park is located in)

# table Articles, with columns:
# - id (representing the default id settings- this column should be the PRIMARY KEY)
# - title (containing the string that represents th title of the article)
# - description (containing the description of the park)
# - article_url (containing the string that represents that article's url)

# table States, with columns:
# - id (representing the default id settings- this column should be the PRIMARY KEY)
# - name (containing the string that represents the name of the state)
# - visitors (containing the integer representing the number of visitors to the national park)
# - econ_benefit (containing the amount of money representing the economic benefit from national park tourism)
# - tax_projects (containing the amount of money representing the tax incentives used to stimulate projects)

# You should load all of the above information into their respective tables

conn = sqlite3.connect("national_parks.db")
cur = conn.cursor()

statement = 'DROP TABLE IF EXISTS Parks'
cur.execute(statement)

statement = 'DROP TABLE IF EXISTS Articles'
cur.execute(statement)

statement = 'DROP TABLE IF EXISTS States'
cur.execute(statement)

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Parks (id INTEGER PRIMARY KEY, name TEXT, site_category TEXT, description TEXT, state TEXT)'
cur.execute(table_spec)

for park in sorted_park_objs:
	s1 = 'INSERT OR IGNORE INTO Parks Values(?, ?, ?, ?, ?)'
	park_vals = (None, park.name, park.site_category, park.description, park.state)
	cur.execute(s1, park_vals)

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Articles (id INTEGER PRIMARY KEY, title TEXT, description TEXT, url TEXT)'
cur.execute(table_spec)

for article in article_objs:
	s2 = 'INSERT OR IGNORE INTO Articles Values(?, ?, ?, ?)'
	article_vals = (None, article.title, article.description, article.article_url)
	cur.execute(s2, article_vals)

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'States (id INTEGER PRIMARY KEY, name TEXT, visitors INTEGER, econ_benefit MONEY, tax_projects MONEY)'
cur.execute(table_spec)

for st in state_objs:
	s3 = 'INSERT OR IGNORE INTO States Values(?, ?, ?, ?, ?)'
	st_vals = (None, st.name, st.visitors, st.econ_benefit, st.tax_projects)
	cur.execute(s3, st_vals)

conn.commit()




		







# Put your tests here, with any edits you now need from when you turned them in with your project plan.


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)

###################### TEST CASES #########################

class TestPlan(unittest.TestCase):
	def test_get_data(self):
		html_park_data = get_natlpark_data()
		self.assertEqual(type(html_park_data), type([]), 'Testing that the return value of the get_natlpark_data() function is a list')
	def test_park_name(self):
		self.assertEqual(type(sorted_park_objs[0].name), type(""), 'Testing that the name of the park is a string')
	def test_articleText(self):
		self.assertEqual(type(article_objs[0].title), type(""), 'Testing that the title of the article is a string')
	def test_description_list():
		self.assertEqual(type(sorted_park_objs), type([]), 'Testing that the sorted_park_objs is a list')
	def test_park_list(self):
		self.assertEqual(sorted_park_objs[0].name, "Zion", 'Testing that the last park in sorted_park_objs is Zion')
	def test_article_list(self):
		article1 = Article()
		self.assertEqual(type(article_list[0]), type(article1), 'Testing that the first element in the list of article instances, article_list, is an Article object')
	# def test_mentioned_parks(self):
	# 	self.assertEqual(type(mentioned_parks) type({'state':'park'})
	def test_DB(self):
		conn = sqlite3.connect('national_parks.db')
		cur = conn.cursor()
		cur.execute('SELECT name FROM Parks')
		result = cur.fetchall()
		self.assertEqual(len(result), 644, 'Testing that the number of national parks in the database is 644')
		conn.close()
	




## Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)