import requests
import unittest
from pprint import pprint
import json


print("\nThis code gives you suggested movies on Netflix to watch. You input your favorite movie and then this code will look up movies on Netflix that the director of your favorite movie has directed. If he has not directed anything on Netflix you will be notified.\n")

name_of_movie = input("Enter in your favorite movie: ")

omdb_cached_data = 'omdbcache.json'
netflix_cached_data = 'netflixcache.json'

try:
	omdb_cache_file = open(omdb_cached_data, 'r')
	omdb_cache_contents = omdb_cache_file.read()
	omdb_cache_diction = json.loads(omdb_cache_contents)
	cache_file.close()
except:
	omdb_cache_diction = {}

def get_omdb_with_caching(name_of_movie):
	base_url = 'http://www.omdbapi.com/'
	full_url = requestURL(base_url, params = {"t": name_of_movie})

	if full_url in omdb_cache_diction:
		omdb_response_text = omdb_cache_diction[full_url]
	else:
		omdb_response = requests.get(full_url)
		omdb_cache_diction[full_url] = omdb_response.text
		omdb_response_text = omdb_response.text

		cache_file = open(omdb_cached_data, 'w')
		cache_file.write(json.dumps(omdb_cache_diction))
		cache_file.close
	return json.loads(omdb_response_text)


try:
	netflix_cache_file = open(netflix_cached_data, 'r')
	netflix_cache_contents = netflix_cache_file.read()
	netflix_cache_diction = json.loads(netflix_cache_contents)
	cache_file.close()
except:
	netflix_cache_diction = {}


def requestURL(base_url, params = {}):
	r = requests.Request(method = 'GET', url = base_url, params = params)
	prep = r.prepare()
	return prep.url

dogs = get_omdb_with_caching(name_of_movie)
#pprint(dogs)
director_name = dogs['Director']


def get_netflix_with_caching(director_name):
	base_url = 'http://netflixroulette.net/api/api.php'
	full_url = requestURL(base_url, params= {'director': director_name})

	if full_url in netflix_cache_diction:
		netflix_response_text = netflix_cache_diction[full_url]
	else:
		netflix_response = requests.get(full_url)
		netflix_cache_diction[full_url] = netflix_response.text
		netflix_response_text = netflix_response.text

		cache_file = open(netflix_cached_data, 'w')
		cache_file.write(json.dumps(netflix_cache_diction))
		cache_file.close()
	return json.loads(netflix_response_text)



try:

	OMDB_data = get_omdb_with_caching(name_of_movie)
	netflix_data = get_netflix_with_caching(director_name)


	class Movie:
		def __init__(self, OMDB_data,netflix_data):
			self.OMDB_data = OMDB_data
			self.netflix_data = netflix_data
			self.year = str(self.OMDB_data['Year'])

		def get_director(self):
			return "Director: " + netflix_data[0]['director']

		def get_plot(self):
			return "Plot: " + self.OMDB_data['Plot']

		def get_genre(self):
			return "Genre: " + self.OMDB_data['Genre']

		def get_year(self):
			return "Released in: {}".format(self.year)

		def get_runtime(self):
			return "Runtime: " + self.OMDB_data['Runtime']

	

	p = Movie(OMDB_data,netflix_data)
	plot = p.get_plot()
	genre = p.get_genre()
	year = p.get_year()
	director = p.get_director()
	runtime = p.get_runtime()
	movie_details = "\nBelow are details about your favorite movie:\n\n{} \n\n{} \n\n{} \n\n{} \n\n{} \n\n-----------------------------\n".format(plot, genre, year, director, runtime)
	print(movie_details)





#This list below gets every movie that the director has filmed on Netflix
	
	director_movies_on_netflix=[]
	
	for dictionary in get_netflix_with_caching(director_name):
		current_movie = dictionary['show_title']
		director_movies_on_netflix.append(current_movie)

	
	
	def compare_movies(director_movies_on_netflix):
		movies = get_netflix_with_caching(director_name)
		d = {}
		for movie in movies:
			d[movie['show_title']] = movie['rating']
		movie_by_rating = sorted(d.keys(), key = lambda k: d[k], reverse = True)
		return movie_by_rating
		

	print("Suggested Netflix movies to watch in order of rating from highest to lowest: \n\n" + str((compare_movies(director_movies_on_netflix))) + '\n')

	# print omdb_cache_diction
	# print netflix_cache_diction
	#*********Tests*********

	#When testing, enter "The Departed" as your favorite movie, and uncomment the following lines in this file.

	omdb_data_test = get_omdb_with_caching('The Departed')
	netflix_data_test = get_netflix_with_caching('Martin Scorsese')


	the_departed = Movie(omdb_data_test,netflix_data_test)
	
	
	# class Test(unittest.TestCase):
	# 	def test1(self):
	# 		self.assertEqual(the_departed.get_plot(), 'Plot: An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.')
	# 	def test2(self):
	# 		self.assertEqual(the_departed.get_genre(), 'Genre: Crime, Drama, Thriller')
	# 	def test3(self):
	# 		self.assertEqual(the_departed.get_year(), 'Released in: 2006')
	# 	def test4(self):
	# 		self.assertEqual(the_departed.get_director(), 'Director: Martin Scorsese')
	# 	def test5(self):
	# 		self.assertEqual(compare_movies(director_movies_on_netflix), ['Raging Bull', 'The Wolf of Wall Street', 'Hugo', 'Taxi Driver', 'The Last Temptation of Christ'])
	# 	def test6(self):
	# 		self.assertEqual(the_departed.get_runtime(), 'Runtime: 151 min')

	

	

	
except:
	print("\nI'm sorry. We could not give you suggested movies on Netflix because the director of your favorite movie does not direct anything on netflix. Please run the program again and enter another movie.\n")

# unittest.main(verbosity = 2)














