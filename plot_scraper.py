import redis
import codecs

FILENAME = 'plot.list'

if __name__ == "__main__":
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    total = 0

    with codecs.open(FILENAME, 'r', 'iso-8859-1') as f:
        temp = []
        scraping_plots = False
        title = ""
        for line in f:
            if len(line) > 3:
                if line[:2] == 'MV':
                    title = line[4:-1]
                    total += 1
                    temp = []
                    scraping_plots = True
                    r.sadd('movies', title)
                elif line[:2] == 'PL':
                    temp.append(line[4:-1])
                else:
                    if scraping_plots:
                        plot = " ".join(temp)
                        r.hset('movie:' + title, 'plot', plot)
                        scraping_plots = False

        print total
