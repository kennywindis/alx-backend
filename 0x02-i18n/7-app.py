#!/usr/bin/env python3
""" Define a get_timezone function and use the babel.timezoneselector decorator. """
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext
import pytz

app = Flask(__name__)
babel = Babel(app)
""" instantiate the Babel object """
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}
""" mock a database user table """


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
    return render_template("7-index.html")


@babel.localeselector
def get_locale():
    """ to determine the best match with our supported languages """
    localLang = request.args.get('locale')
    supportLang = app.config['LANGUAGES']
    if localLang in supportLang:
        return localLang
    userId = request.args.get('login_as')
    if userId:
        localLang = users[int(userId)]['locale']
        if localLang in supportLang:
            return localLang
    localLang = request.headers.get('locale')
    if localLang in supportLang:
        return localLang
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """ returns a user dictionary or None
    if the ID cannot be found or if login_as was not passed """
    try:
        userId = request.args.get('login_as')
        return users[int(userId)]
    except Exception:
        return None


@app.before_request
def before_request():
    """ use get_user to find a user if any,
    and set it as a global on flask.g.user  """
    g.user = get_user()


@babel.timezoneselector
def get_timezone():
    """ Infer appropriate time zone """
    localTimezone = request.args.get('timezone')
    if localTimezone in pytz.all_timezones:
        return localTimezone
    else:

