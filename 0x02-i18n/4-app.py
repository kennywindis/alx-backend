#!/usr/bin/env python3
""" implement a way to force a particular locale by passing the locale=fr parameter to app’s URLs """
from flask import Flask, render_template, request
from flask_babel import Babel, gettext

app = Flask(__name__)
babel = Babel(app)
""" instantiate the Babel object """


class Config(object):
    """ config class """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
""" Use that class as config for Flask app """


@app.route('/')
def one():
    """ basic Flask app """
    return render_template("4-index.html")


@babel.localeselector
def get_locale():
    """ to determine the best match with our supported languages """
    localLang = request.args.get('locale')
    supportLang = app.config['LANGUAGES']
    if localLang in supportLang:
        return localLang
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == "__main__":
    app.run()