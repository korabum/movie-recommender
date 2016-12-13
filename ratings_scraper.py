import redis
import codecs

FILENAME = 'ratings.list'

if __name__ == "__main__":
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    total = 0

    with codecs.open(FILENAME, 'r', 'iso-8859-1') as f:
        title = ""
        rating = 0.0
        for line in f:
            # Skip episodes of series
            if '{' in line:
                continue
            # Skip video game titles
            if '(VG)' in line:
                continue
            # Skip video titles 
            if '(V)' in line:
                continue

            title = line[32:-1]
            rating = float(line[26:30])
            total += 1
            r.hset('movie:' + title, 'rating', rating)


        print total
