from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .key import DATABASE_URI

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context() :
        db.init_app(app)
        migrate.init_app(app, db)

    from movie_app.routes import (main_route, recommend_route,favorite_route)
    app.register_blueprint(main_route.bp)
    app.register_blueprint(recommend_route.bp)
    app.register_blueprint(favorite_route.bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
