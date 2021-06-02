from flask import Blueprint, render_template, request, redirect, url_for
from imdb import IMDb
import tmdbsimple as tmdb
from movie_app.models.movie_model import Movies
from movie_app import db
from movie_app.key import api_key

bp = Blueprint('main', __name__)

tmdb.API_KEY = api_key

tmdb_img_url = r'https://image.tmdb.org/t/p/w342'

enable_extra=True

ia = IMDb()

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/search')
def search():
    query = request.args.get('moviename', None)
    results = []
    id_list = []
    if query:
        q_res = ia.search_movie(query)
        for m in q_res:
            try: 
                mdata = ia.get_movie(m.getID())
                genre = mdata.data['genres']
                rating = mdata.data['rating']
                if (m['kind'] == 'movie') & ({m['title']:m['year']} not in id_list):
                    movie_dict = {'id': m.getID(),
                        'title': m['title'],
                        'year': m['year'],
                        'cover': m['full-size cover url'] if m['full-size cover url'] else m['cover url'],
                        'genre': genre if genre else 'N/A',
                        'rating' : rating if rating else 'N/A'
                        }
                    # 중복 입력 방지
                    id_list.append({m['title']:m['year']})
                    results.append(movie_dict.copy())
            except KeyError:
                pass
        return render_template("index.html", results=results, search_name = query)
    else: #not query
        return ('')

@bp.route('/info', methods=['Get','POST'])
def info():
    query = request.args.get('moviename', None)
    movid = request.args.get('id', None)
    if not movid:
        return ('')
    else:
        mov = ia.get_movie(movid)
        movie={}

        #collect all the relevent info in a dict 'movie'
        long_title = mov.get('long imdb title')
        title = mov.get('title')
        rating = mov.get('rating', None)
        genres = (", ".join(mov.get('genres', []))).title()
        runmin = 0
        if mov.get('runtime'):
            runmin = int(mov.get('runtime', ['0'])[0])
        runtime = "{}h {}m".format(runmin//60, runmin%60)

        director = ''
        writer = ''
        if mov.get('director'):
            director = mov.get('director')[0]['name']
        if mov.get('writer'):
            writer = mov.get('writer')[0]['name']

        cover = mov.get('full-size cover url', None)
        plot = mov.get('plot', [''])[0].split('::')[0]

        if enable_extra:
            find = tmdb.Find('tt{:07}'.format(int(movid)))
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
                'long title': long_title,
                'title': title,
                'rating': rating if rating else '',
                'genres': genres,
                'runtime': runtime,
                'director': director,
                'writer': writer,
                'plot': plot if plot else '',
                'cover': cover if cover else ''
        }
        if request.method == "POST":
            movie_id = request.form["favoritemovie"]
            if Movies.query.filter(Movies.id==movie_id).first() == None:
                favorie_movie = Movies(id = movie_id, year =  mov.get('year'), title = title, rating = rating,
                genre = genres, director = director, writer = writer, cover = cover, plot = plot)
                db.session.add(favorie_movie)
                db.session.commit()
                return render_template("info.html",movie=movie)

        return render_template("info.html",movie=movie)
