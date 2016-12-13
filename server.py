from flask import Flask, jsonify
from math import sqrt
from quickselect import select
import redis
import sys
import operator

GENRE_WEIGHT = 0.1

reload(sys)
sys.setdefaultencoding('iso-8859-1')

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0, encoding='iso-8859-1')

titles = r.smembers('movies')
number_of_movies = len(titles)
weight = {}
genre_weight = {}
vector_length = {}
genre_vector_length = {}

for title in titles:
    weight[title] = r.hgetall('weight:' + title)
    for word in weight[title]:
        weight[title][word] = float(weight[title][word])

for title in titles:
    tmp = r.hgetall('genre_weight:' + title)
    if len(tmp) == 0:
        continue
    genre_weight[title] = tmp
    for genre in genre_weight[title]:
        genre_weight[title][genre] = float(genre_weight[title][genre])

for title in weight:
    total = 0
    for word in weight[title]:
        total += weight[title][word] ** 2
    vector_length[title] = sqrt(total)

for title in genre_weight:
    total = 0
    for genre in genre_weight[title]:
        total += genre_weight[title][genre] ** 2
    genre_vector_length[title] = sqrt(total)

print "server is ready"

def get_cosine_similarity(first_title, second_title):
    if first_title in genre_weight and second_title in genre_weight:
        total = 0
        for word in weight[first_title]:
            if word in weight[second_title]:
                total += weight[first_title][word] * weight[second_title][word]
        temp = (vector_length[first_title] * vector_length[second_title])
        if temp == 0:
            return 0
        plot_cosine_similarity = total / temp

        total = 0
        for genre in genre_weight[first_title]:
            if genre in genre_weight[second_title]:
                total += genre_weight[first_title][genre] * genre_weight[second_title][genre]
        temp = (genre_vector_length[first_title] * genre_vector_length[second_title])
        genre_cosine_similarity = total / temp

        return (plot_cosine_similarity * (1 - GENRE_WEIGHT)) + (genre_cosine_similarity * GENRE_WEIGHT)
    else:
        total = 0
        for word in weight[first_title]:
            if word in weight[second_title]:
                total += weight[first_title][word] * weight[second_title][word]
        temp = (vector_length[first_title] * vector_length[second_title])
        if temp == 0:
            return 0
        return total / temp

@app.route('/get-plot-summary/<query>')
def get_plot_summary(query):
    matches = []
    standardized_query = query.lower()
    words = standardized_query.split()
    for title in titles:
        match = True
        standardized_title = title.lower()
        if standardized_title == standardized_query:
            movie = r.hgetall('movie:' + title)
            rating = "N/A"
            genre = "N/A"
            if 'rating' in movie:
                rating = movie['rating']
            if 'genre' in movie:
                genre = movie['genre']
            ret = {'status': 0, 'title': title, 'plot': movie['plot'], 'rating': rating, 'genre': genre}
            return jsonify(ret)
        for word in words:
            if word not in standardized_title:
                match = False
                break
        if match:
            matches.append(title)
    if len(matches) == 1:
        movie = r.hgetall('movie:' + matches[0])
        rating = "N/A"
        genre = "N/A"
        if 'rating' in movie:
            rating = movie['rating']
        if 'genre' in movie:
            genre = movie['genre']
        ret = {'status': 0, 'title': matches[0],'plot': movie['plot'], 'rating': rating, 'genre': genre}
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

@app.route('/get-similar-movies/<query>')
def get_similar_movies(query):
    max_similarity = 0
    similar_title = ""
    return_vector = {}
    similarities = {}
    similarity_values = []
    similar_movies = []

    if query not in vector_length or vector_length[query] == 0:
        ret = {'status': 404}
        return jsonify(ret)

    for title in titles:
        if title == query:
            continue
        similarity = get_cosine_similarity(query, title)
        similarities[title] = similarity
        similarity_values.append(similarity)
    
    k = 11
    kth_value = select(similarity_values, number_of_movies - k)
    for title in similarities:
        if similarities[title] >= kth_value:
            return_vector[title] = similarities[title]

    sorted_values = sorted(return_vector.items(), key=operator.itemgetter(1))
    for (name, value) in sorted_values:
        movie = r.hgetall('movie:' + name)
        rating = "N/A"
        genre = "N/A"
        if 'rating' in movie:
            rating = movie['rating']
        if 'genre' in movie:
            genre = movie['genre']
    
        similar_movies.append({'title': name, 'plot': movie['plot'], 'similarity': value, 'rating': rating, 'genre': genre})

    ret = {'status': 0, 'movies': similar_movies}
    return jsonify(ret)

if __name__ == "__main__":
    app.run()
