from flask import Blueprint, request, render_template, url_for, Response
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from imdb import IMDb
import tmdbsimple as tmdb
from movie_app.key import api_key

bp = Blueprint('recommend', __name__)

tmdb.API_KEY = api_key

tmdb_img_url = r'https://image.tmdb.org/t/p/w342'

ia = IMDb()

enable_extra=True

df = pd.read_csv('movie_app/routes/imdb.csv')
df.fillna('',inplace=True)
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df['soup'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df = df.reset_index()
indices = pd.Series(df.index, index=df['title'])
all_titles = [df['title'][i] for i in range(len(df['title']))]

def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]
    movie_indices = [i[0] for i in sim_scores]
    moviename= df['title'].iloc[movie_indices]
    movie_list = []

    for m in moviename:
        if not m:
            return ('')
        else:
            movid = ia.search_movie(m)[0].getID()
            mov = ia.get_movie(movid)
            movie={}
            title = mov.get('title')
            year = mov.get('year', None)
            rating = mov.get('rating', None)
            genres = (", ".join(mov.get('genres', []))).title()
            director = ''
            writer = ''
            if mov.get('director'):
                director = mov.get('director')[0]['name']
            if mov.get('writer'):
                writer = mov.get('writer')[0]['name']
            cover = mov.get('full-size cover url', None)
            plot = mov.get('plot', [''])[0].split('::')[0]
            if enable_extra:
                find = tmdb.Find(movid)
                find.info(external_source='imdb_id')
            if (find.movie_results and find.movie_results[0]['poster_path']
            and find.movie_results[0]['overview']):
                cover = tmdb_img_url + find.movie_results[0]['poster_path']
                plot = find.movie_results[0]['overview']
            elif (find.tv_results and find.tv_results[0]['poster_path']
            and find.tv_results[0]['overview']):
                cover = tmdb_img_url + find.tv_results[0]['poster_path']
                plot = find.tv_results[0]['overview']
            
            movie = {
                'id': mov.getID(),
                'title': title,
                'year': year,
                'rating': rating if rating else '',
                'genres': genres,
                'director': director,
                'writer': writer,
                'plot': plot if plot else '',
                'cover': cover if cover else ''
            }

            movie_list.append(movie)
            
    return  movie_list

@bp.route('/recommend')
def index():
    return render_template('recommend.html')

@bp.route('/recommend/result', methods=['GET','POST'])
def main():
    if request.method == 'GET':
        return render_template('recommend.html')

    if request.method == 'POST':
        m_name = request.form['movie_name']
        m_name = m_name.title()
        if m_name not in all_titles:
            
            msg = "데이터베이스에 없는 영화입니다."
            return render_template('recommend.html',msg=msg)
        else:
            movie_list = get_recommendations(m_name)
            
    return render_template('recommend.html',results = movie_list, search_name=m_name)


