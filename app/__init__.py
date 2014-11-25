from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "ban2"}
app.config["SECRET_KEY"] = "senha"

db = MongoEngine(app)

def register_blueprints(app):
    from app.views import filmes
    app.register_blueprint(filmes)

register_blueprints(app)

if __name__ == '__main__':
    app.run()
