import redis
import sys
from numpy import log10

reload(sys)
sys.setdefaultencoding('iso-8859-1')

r = redis.StrictRedis(host='localhost', port=6379, db=0, encoding='iso-8859-1')

if __name__ == "__main__":
    titles = r.smembers('movies')
    number_of_movies = len(titles)
    df = {}
    tf = {}
    idf = {}
    for title in titles:
        genres = r.hget('movie:' + title, 'genre')
        if genres is None:
            continue
        genres = genres.split()
        tf[title] = {}
        for genre in genres:
            if genre not in df:
                df[genre] = {}
            df[genre][title] = True
            if genre not in tf[title]:
                tf[title][genre] = 0
            tf[title][genre] += 1

    print "tf-df count"
    # Menghitung idf
    for genre in df:
        idf[genre] = log10(number_of_movies / sum(df[genre].values()))

    print "idf count"

    for title in tf:
        for genre in tf[title]:
            weight = tf[title][genre] * idf[genre]
            r.hset('genre_weight:' + title, genre, weight)
