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
from collections import Counter
from bs4 import BeautifulSoup
# Begin filling in instructions....

# Define a class called NationalPark that accepts an HTML formatted string and the state name of the park as input. Use BeautifulSoup to parse through the html data 
# in order to correctly assign values to instance variables. Instance variables for this class should include the park's name, description, category, and state. The class should
# also include two methods: 1) one that will define how the park will be represented when printed to the user, making use of each of the instance variables and 2) another that 
# will return a list of useful url's to search for more information on the park such as basic info, alerts and conditions, etc. 
class NationalPark(object): 

	def __init__(self, html_string, current_state):
		park_info = html_string.find(class_= "col-md-9 col-sm-9 col-xs-12 table-cell list_left")

		self.name = park_info.find('a').text

		self.description = park_info.find('p').text

		self.site_category = park_info.find('h2').text

		self.state = current_state

	def __str__(self):
		return "{0} is a {1} located in {2}. Here is a description of the {0}: {3}".format(self.name, self.site_category, self.state, self.description)

	def get_useful_info(self, html_string):
		park_info = html_string.find(class_ = 'col-md-3 col-sm-3 col-xs-12 result-details-container table-cell list_right')
		info = park_info.find_all('li')
		useful_info = [item.find('a').get('href') for item in info]
		return useful_info


# Define a class called Article that accepts an HTML formatted string (representing one article on the National Parks' home page) as input. Use BeautifulSoup to parse through the html data
# in order to correctly assign values to instance variables. Instance variables for this class should include the article's title, description, and the url to search it.
class Article(object):

	def __init__(self, html_string):
		self.title = html_string.find(class_ = "Feature-title carrot-end").text

		self.description = html_string.find('p').text

		self.article_url = html_string.find('a').get('href')

	def __str__(self):
		return '{0}: {1}.\n To read more, visit the national park website at {2}.'.format(self.title, self.description, selt.article_url)

# Define a class called States that accepts an HTML formatted string and the state name as input. Use BeautifulSoup to parse through thr html data in order to correctly
# assign values to instance variables. Instance variables for this class should include the state name, the total number of visitors its national parks, the economic benfit obtained
# from national park tourism, and the total tax incentives that have stimulated rehabilitation projects.
class State(object):

	def __init__(self, html_string, current_state):
		state_info = html_string.find_all("li")

		if " Visitors to National Parks" in state_info[1].text:
			self.visitors = int(state_info[1].find('strong').text.replace(',',''))
		else:
			self.visitors = int(0)

		if " Economic Benefit from National Park Tourism »" in state_info[2].text:
			self.econ_benefit = int(state_info[2].find('strong').text[1:].replace(',',''))
		else:
			self.econ_benefit = int(0)

		if " of Rehabilitation Projects Stimulated by Tax Incentives (since 1995) »" in state_info[3].text:
			self.tax_projects = int(state_info[3].find('strong').text[1:].replace(',',''))
		else:
			self.tax_projects = int(0)
		
		self.name = current_state	

# Create a file to cache the information you retrieve from the internet. Save this in a file called 206finalproj_caching.json. 

CACHE_FNAME = "206final_caching.json"
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
		print("using cached park data")
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
		

# Write a function called get_article_data that retrieves html data for the articles on the National Parks homepage. Add this html data to your cache file. 
# Save and return the html data of the articles in a variable called html_articles, which represents the html data of the National Parks homepage. 
def get_article_data():
	unique_identifier = "article_data"
	if unique_identifier in CACHE_DICTION:
		print("using cached article data")
		html_articles = CACHE_DICTION[unique_identifier]
	else:
		print("accessing article data from internet")
		base_url = "https://www.nps.gov/index.htm"
		html_articles = requests.get(base_url).text
		#print(type(html_articles))
		CACHE_DICTION[unique_identifier] = html_articles
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return html_articles

# Invoke the get_natlparks_data function and save the result to a variable called html_park_data.
html_park_data = get_natlparks_data()
#print(html_park_data)

# Invoke the get_article_data function and save the result to a variable called html_article_data. 
html_article_data = get_article_data()

# Using the information stored in html_park_data, create a list of NationalPark objects and save them in a variable called park_objs.
park_objs = []
repeat_parks = []
for state_html in html_park_data:
	soup = BeautifulSoup(state_html, "html.parser")
	current_state = soup.find(class_ = "ContentHeader").text.strip()
	# print()
	# print(type(current_state))
	# print()
	# print(current_state)
	st_parks = soup.find(class_ = "col-md-9 col-sm-12 col-xs-12 stateCol")
	for item in st_parks.find_all(class_= "clearfix"):
		current_obj = NationalPark(item, current_state)
		#print(current_obj.get_useful_info(item))
		if current_obj not in repeat_parks:
			repeat_parks.append(current_obj)
			park_objs.append(current_obj)

# Sort the list of park objects alphabetically by name and save the new list in a variable called sorted_park_objs. 
sorted_park_objs = [park for park in park_objs]
sorted_park_objs = sorted(park_objs, key = lambda x: x.name)

# Using the information stored in html_article_data, create a list of Article objects and save them in a variable called article_objs. 
article_objs = []
soup = BeautifulSoup(html_article_data, "html.parser")
all_articles = soup.find(class_ = "Component FeatureGrid")
article_list1 = [Article(article) for article in all_articles.find_all(class_ = "FeatureGrid-item col-xs-12 col-sm-6")]
article_list2 = [Article(article) for article in all_articles.find_all(class_ = "FeatureGrid-item col-xs-12 col-sm-4")]

article_objs = article_list1 + article_list2

# Using the information stored in html_park_data, create a list of State objects and save them in a variable called state_objs. 
state_objs = []
for state_html in html_park_data:
	soup = BeautifulSoup(state_html, "html.parser")
	current_state = soup.find(class_ = "ContentHeader").text.strip()
	state_info = soup.find(class_ = "col-md-3 col-sm-12 col-xs-12 stateCol stateCol-right")
	state_objs.append(State(state_info, current_state))

# Write a function called get_weather_data that retrieves data about the average temperature for each state.
def get_weather_data():
	unique_identifier = "weather_data"
	if unique_identifier in CACHE_DICTION:
		print('using cached weather data')
		weather_info = CACHE_DICTION[unique_identifier]
	else:
		print('accessing weather data from internet')
		base_url = "https://www.currentresults.com/Weather/US/average-annual-state-temperatures.php"
		weather_info = requests.get(base_url).text
		CACHE_DICTION[unique_identifier] = weather_info
		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return weather_info 

# Invoke the get_weather_data function and save the result to the variable weather_data.
weather_data = get_weather_data()

# Using the information stored in weather_data, create a dictionary with key value pairs that represent states as keys and their average tempertature as the associated value. 
state_weather = {}
soup = BeautifulSoup(weather_data, 'html.parser')
temp_table = soup.find_all(class_ = 'articletable tablecol-1-left')
for st in temp_table:
	table = st.find_all('tbody')
	for elem in table:
		x = elem.find_all('tr')
		for info in x:
			state_name = info.find('a').text
			state_temp = float(info.find_all('td')[1].text)
			state_weather[state_name] = state_temp
#print(state_weather)

# Create a database file called national_parks.db. In the database, you will make three tables called Parks, Articles, and States as follows:

# table Parks, with columns:
# - id (representing the default id settings- this column should be the PRIMARY KEY)
# - name (containing the string that represents the national park's name)
# - site_category (containing the string that represents the type of national park)
# - description (containing the description of the park)
# - state (containing the name of the state the park is located in)

# table Articles, with columns:
# - id (representing the default id settings- this column should be the PRIMARY KEY)
# - title (containing the string that represents the title of the article)
# - description (containing the description of the article)
# - article_url (containing the string that represents that article's url)

# table States, with columns:
# - id (representing the default id settings- this column should be the PRIMARY KEY)
# - name (containing the string that represents the name of the state)
# - visitors (containing the integer representing the number of visitors to the state's national parks)
# - econ_benefit (containing the amount of money representing the economic benefit from national park tourism)
# - tax_projects (containing the amount of money representing the tax incentives used to stimulate projects)
# - weather (containing the average temperature of the state in fahrenheit)

# You should load all of the above information into their respective tables.

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
table_spec += 'States (id INTEGER PRIMARY KEY, name TEXT, visitors INTEGER, econ_benefit MONEY, tax_projects MONEY, avg_temperature REAL)'
cur.execute(table_spec)

for st in state_objs:
	if st.name in state_weather:
		avg_temperature = state_weather[st.name]
	else:
		avg_temperature = 0
	s3 = 'INSERT OR IGNORE INTO States Values(?, ?, ?, ?, ?, ?)'
	st_vals = (None, st.name, st.visitors, st.econ_benefit, st.tax_projects, avg_temperature)
	cur.execute(s3, st_vals)

conn.commit()

##### QUERIES #####

# Make a query to select all of the parks and the states thet are located in.
# Save the results in a variable called query_res1. 
query = 'SELECT Parks.name, States.name FROM Parks INNER JOIN States on Parks.state = States.name'
q1 = cur.execute(query)
query_res1 = q1.fetchall()

# Make a query to select the name and economic benefit due to tourism from the states whose economic beneift is greater than $1 bllion.
# Save the results in a variable called most_econ_benefit. 
query = 'SELECT name, econ_benefit FROM States WHERE States.econ_benefit > 1000000000'
q2 = cur.execute(query)
most_econ_benefit = q2.fetchall()
#print(most_econ_benefit)

# Make a query to select the name and number of visitors from each state where the number of visitors is greater than 10 million.
# Save the results in a variable called query_res3. 
query = 'SELECT name, visitors FROM States WHERE States.visitors > 10000000'
q3 = cur.execute(query)
query_res3 = q3.fetchall()

# Make a query to select the name of the parks and the average temperture of the states they're located in where the average temperature is over 65 degrees.
# Save the results in a variable called query_res4. 
query = 'SELECT Parks.name, States.avg_temperature FROM Parks INNER JOIN States on Parks.state = States.name WHERE States.avg_temperature > 65.0'
q4 = cur.execute(query)
query_res4 = q4.fetchall()

# Make a query to select the name of all states of each of the parks in the Parks table.
# Save the results in a variable called query_res5.
query = 'SELECT state FROM Parks'
q5 = cur.execute(query)
query_res5 = q5.fetchall()


##### DATA MANIPULATION #####

# Using the State instances in the list state_objs, use list comprehension to create a list with the names of the states with the largest number of national park visitors.
# Save the result in the list top_visitors.
sorted_output = sorted(state_objs, key = lambda x: x.visitors, reverse = True)
output_visitors = sorted_output[:3]
top_visitors = [st.name for st in output_visitors]

# Using the data stored in query_res1, find the name of park that runs through the most states/region. Save the result in the variable largest_park_span. 
park_span = {}
for tup in query_res1:
	if tup[0] in park_span:
		park_span[tup[0]] += 1
	else:
		park_span[tup[0]] = 1 
sorted_park_span = sorted(park_span, key = lambda x: park_span[x], reverse = True)
largest_park_span = sorted_park_span[0]

# Using the data stored in query_res4, perform dictionary comprehension to create a dictionary using the state names as the key and their average temperatures
# as the associated values. Save the result in a variable called temperature_dict.
temperature_dict = {k:v for (k,v) in query_res4}

# Using the data stored in query_res5 and Counter from the collections library, find the top 5 states contain the most national sites. Then, use dictionary comprehension
# to create a dictionary using the state names as the keys and the number of national monuments as their associated values. Save the result in a variable called most_parks. 
most_common_state = Counter(query_res5).most_common(5)
most_parks = {k[0]:v for (k,v) in most_common_state}


##### CREATING THE OUTPUT FILE #####
file_name = '206finalproj_output.txt'
output_file = open(file_name, 'w')

user_input = input("Type the letter of which of the following options you would like to see: \n A) Most popular parks \n B) Parks in warm weather \n C) The largest park \n D) States with the most parks \n Or press 'enter' to see all of the above \n").upper()
if user_input == 'A':
	output_file.write('The following sites are located in the states with the most nation park visitors! \n')
	for park in park_objs:
		if park.state in top_visitors:
			output_file.write(park.__str__()+'\n')
		else: 
			pass
elif user_input == 'B':
	output_file.write('Looking for warm weather? The following attractions are located in 65 degree weather or better! \n')
	output_file.write(json.dumps(temperature_dict, indent = 2)+'\n')
elif user_input == 'C':
	output_file.write('The following is a brief summary of the park that spans the most states: \n')
	for park in park_objs:
		if park.name == largest_park_span:
			output_file.write(park.__str__()+'\n')
			break
elif user_input == 'D':
	output_file.write('Here are the top 5 states with the most national monuments! \n')
	output_file.write(json.dumps(most_parks, indent = 2)+'\n')
else: 
	output_file.write('The following sites are located in the states with the most nation park visitors! \n')
	for park in park_objs:
		if park.state in top_visitors:
			output_file.write(park.__str__()+'\n')
	output_file.write('Looking for warm weather? The following attractions are located in 65 degree weather or better! \n')
	output_file.write(json.dumps(temperature_dict, indent = 2)+'\n')
	output_file.write('The following is a brief summary of the park that spans the most states: \n')
	for park in park_objs:
		if park.name == largest_park_span:
			output_file.write(park.__str__()+'\n')
			break
	output_file.write('Here are the top 5 states with the most national monuments! \n')
	output_file.write(json.dumps(most_parks, indent = 2)+'\n')

output_file.close()


# Put your tests here, with any edits you now need from when you turned them in with your project plan.


# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)

###################### TEST CASES #########################

class TestPlan(unittest.TestCase):

	def test_get_data(self):
		html_park_data = get_natlparks_data()
		self.assertEqual(type(html_park_data), type([]), 'Testing that the return value of the get_natlpark_data() function is a list')
	def test_park_name(self):
		self.assertEqual(type(sorted_park_objs[0].name), type(""), 'Testing that the name of the park is a string')
	def test_article_text(self):
		self.assertEqual(type(article_objs[0].title), type(""), 'Testing that the title of the article is a string')
	def test_description_list(self):
		self.assertEqual(type(sorted_park_objs), type([]), 'Testing that the sorted_park_objs is a list')
	def test_park_list(self):
		self.assertEqual(sorted_park_objs[-1].name, "Zion", 'Testing that the last park in sorted_park_objs is Zion')
	def test_state_name(self):
		html_file = open('Michigan (U.S. National Park Service).htm', 'r')
		file_contents = html_file.read()
		html_file.close()
		soup = BeautifulSoup(file_contents, "html.parser")
		self.assertEqual(soup.find(class_ = "ContentHeader").text.strip(), 'Michigan', 'Testing the assignment statement leads to the correct state name')
	def test_state_visitors(self):
		html_file = open('Michigan (U.S. National Park Service).htm', 'r')
		file_contents = html_file.read()
		html_file.close()
		soup = BeautifulSoup(file_contents, "html.parser")
		current_state = soup.find(class_ = "ContentHeader").text.strip()
		state_info = soup.find(class_ = "col-md-3 col-sm-12 col-xs-12 stateCol stateCol-right")
		self.assertEqual(State(state_info, current_state).visitors, 2386613, 'Testing that the number of visitors is correct')
	def test_park_span1(self):
		self.assertEqual(type(largest_park_span), type(""), 'Testing that the result of largest_park_span is a string')
	def test_park_span2(self):
		self.assertEqual(largest_park_span, 'Appalachian', 'Testing that the value of largest_park_span is Appalachian')
	def test_most_parks(self):
		self.assertEqual(len(most_parks), 5, 'Testing that the value of the first key in most_parks is a string')
	def test_top_visitors1(self):
		self.assertEqual(len(top_visitors), 3, 'Testing that top_visitors holds three elements')
	def test_top_visitors2(self):
		self.assertEqual(type(top_visitors), type([]),'Testing that top_visitors is a list')
	def test_park_num(self):
		conn = sqlite3.connect('national_parks.db')
		cur = conn.cursor()
		cur.execute('SELECT name FROM Parks')
		result = cur.fetchall()
		self.assertTrue(len(result) > 640, 'Testing that the number of national parks in the database is 644')
		conn.close()



## Remember to invoke all your tests...
if __name__ == "__main__":
	unittest.main(verbosity=2)