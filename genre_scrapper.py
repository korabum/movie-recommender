import redis
import codecs

FILENAME = 'genre.list'

if __name__ == "__main__":
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    genreDict = {}

    with codecs.open(FILENAME, 'r', 'iso-8859-1') as f:
        for line in f:
            if "(V)" in line:
                continue
            elif "(VG)" in line:
                continue
            elif "{" in line:
                continue
            splitted = line.split()

            n = len(splitted)
            title = " ".join(splitted[:-1])
            if title in genreDict:
                genreDict[title] += " " + splitted[-1]
            else:
                genreDict[title] = splitted[-1]

    for title in genreDict:
        r.hset('movie:' + title, 'genre', genreDict[title])