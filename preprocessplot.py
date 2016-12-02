import redis
import sys
from stop_words import get_stop_words
import string
from nltk.stem import PorterStemmer

stop_words = get_stop_words('en')
ps = PorterStemmer()

reload(sys)
sys.setdefaultencoding('iso-8859-1')

r = redis.StrictRedis(host='localhost', port=6379, db=0, encoding='iso-8859-1')

def removeStopWords(text):
	removed = text.lower()
	removed = ' '.join([word for word in removed.split() if word not in stop_words])
	return removed

def removePunctuation(text):
	return text.translate(None, string.punctuation)

def stem(text):
	words = text.split()
	stemmed_words = [ps.stem(word) for word in words]
	return ' '.join(stemmed_words)


if __name__ == "__main__":
	titles = r.smembers('movies')
	for title in titles:
	    movie = r.hgetall('movie:' + title)
	    plot = movie['plot']
	    processed_plot = removePunctuation(plot)
	    processed_plot = removeStopWords(processed_plot)
	    processed_plot = stem(processed_plot)
	    r.hset('process_movie:' + title, 'plot', processed_plot)