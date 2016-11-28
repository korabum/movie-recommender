from flask import Flask, jsonify
import redis
import sys

reload(sys)
sys.setdefaultencoding('iso-8859-1')

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0, encoding='iso-8859-1')

@app.route('/get-plot-summary/<query>')
def get_plot_summary(query):
    titles = r.smembers('movies')
    matches = []
    standardized_query = query.lower()
    words = standardized_query.split()
    for title in titles:
        match = True
        standardized_title = title.lower()
        if standardized_title == standardized_query:
            movie = r.hgetall('movie:' + title)
            ret = {'status': 0, 'title': title, 'plot': movie['plot']}
            return jsonify(ret)
        for word in words:
            if word not in standardized_title:
                match = False
                break
        if match:
            matches.append(title)
    if len(matches) == 1:
        movie = r.hgetall('movie:' + matches[0])
        ret = {'status': 0, 'title': matches[0],'plot': movie['plot']}
        return jsonify(ret)
    elif len(matches) == 0:
        ret = {'status': 404}
        return jsonify(ret)
    else:
        movies = []
        for title in matches:
            movies.append({'title': title})
        ret = {'status': 1, 'movies': movies}
        return jsonify(ret)

if __name__ == "__main__":
    app.run()
