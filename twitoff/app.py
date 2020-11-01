"""Main app/routig file for Twitoff"""

from flask import Flask, render_template, request
from os import getenv
from .models import DB, User
from .twitter import add_or_update_user, update_all_users
from .predict import predict_user

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def create_app():
    """ Creates and Configures a Flask application"""

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template("base.html", title="Home",
                               users=User.query.all())

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        # grabs inputted values from the dropdown
        user0, user1 = sorted(
            [request.values['user1'],
             request.values['user2']]
        )

        if user0 == user1:
            # tells application user they cant compare same twitter users
            message = "Cannot compare users to themselves!"

        else:
            # running prediction and return the prediction to user as a message
            prediction = predict_user(user0, user1,
                                      request.values['tweet_text'])
            message = "{} is more likely to be said by {} than {}".format(
                request.values['tweet_text'], user1 if prediction else user0,
                user0 if prediction else user1)

        return render_template('prediction.html', title='Prediction',
                               message=message)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # either grab a user that already exist in our
        # DB or grab the users input
        name = name or request.values['user_name']

        try:
            # if button is clicked then do this
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} sucessfully added!'.format(name)
            # tweets are always collected if the user exist
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            # if we get an error then no tweets are displayed
            tweets = []

        return render_template('user.html', title=name, tweets=tweets,
                               message=message)

    @app.route('/update')
    def update():
        # updates our users from the function in twitter.py
        update_all_users()
        return render_template('base.html', title="Tweets have been updated!",
                               users=User.query.all())

    @app.route('/reset')
    def reset():
        # resets database
        DB.drop_all()
        # creates database again
        DB.create_all()
        return render_template('base.html', title='Reset Database!')

    return app

footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span('Lester Gomez', className='mr-2'), 
                    html.A(html.I(className='fas fa-envelope-square mr-1'), href='mailto:Lester17.C@Gmail.com'),
                    html.A(html.I(className='fab fa-github-square mr-1'), href='https://github.com/machine-17/Twitoff_App'),
                    html.A(html.I(className='fab fa-linkedin mr-1'), href='https://www.linkedin.com/in/lg17/'),
                    html.A(html.I(className='fab fa-twitter-square mr-1'), href='https://twitter.com/_machine17'),
                ], 
                className='lead'
            )
        )
    )
)

html.Div([footer])