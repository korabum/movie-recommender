import redis
import sys
from stop_words import get_stop_words
import string
from nltk.stem import PorterStemmer
from numpy import log10

stop_words = get_stop_words('en')
ps = PorterStemmer()

reload(sys)
sys.setdefaultencoding('iso-8859-1')

r = redis.StrictRedis(host='localhost', port=6379, db=0, encoding='iso-8859-1')

def removeStopWords(text):
	removed = text.lower()
	removed = [word for word in removed.split() if word not in stop_words]
	return removed

def removePunctuation(text):
	return text.translate(None, string.punctuation)

def stem(text):
	for i in range(len(text)):
		text[i] = ps.stem(text[i])
	return text

if __name__ == "__main__":
	titles = r.smembers('movies')
	number_of_movies = len(titles)
	df = {}
	tf = {}
	idf = {}
	for title in titles:
		tf[title] = {}
		plot = r.hget('movie:' + title, 'plot')
		processed_plot = removePunctuation(plot)
		processed_plot = removeStopWords(processed_plot)
		processed_plot = stem(processed_plot)
		for word in processed_plot:
			if word not in df:
				df[word] = {}
			df[word][title] = True

			if word not in tf[title]:
				tf[title][word] = 0
			tf[title][word] += 1

		# Normalisasi tf
		plot_length = float(len(processed_plot))
		for word in processed_plot:
			tf[title][word] = tf[title][word] / plot_length

	# Menghitung idf
	for word in df:
		idf[word] = log10(number_of_movies / sum(df[word].values()))

	for title in tf:
		for word in tf[title]:
			weight = tf[title][word] * idf[word]
			r.hset('weight:' + title, word, weight)
