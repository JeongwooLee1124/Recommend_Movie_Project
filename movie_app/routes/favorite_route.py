from flask import Blueprint, request, redirect, url_for, Response, render_template
from movie_app import db
from movie_app.models.movie_model import Movies

bp = Blueprint('favorite', __name__)

@bp.route('/favorite', methods=['GET'])
def favorite():
    favorite = Movies.query.all()
    return render_template("favorite.html", favorite=favorite)


@bp.route('/favorite', methods=['POST'])
def delete_movie():
    delete_movie = request.form["delete_movie"]
    if delete_movie is None :
      return "", 400
    
    favmovie =  Movies.query.filter(Movies.id==delete_movie).first()
    if favmovie:
        db.session.delete(favmovie)
        db.session.commit()
    return redirect(url_for('favorite.favorite')) 