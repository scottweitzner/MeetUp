from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify
from .models import User

# import classes and functions from models an initialize app

app = Flask(__name__)


@app.route('/')
def index():
    posts = []  # from the tutorial - will change
    return render_template('index.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        if not User(email).verify_password(password):
            flash('Invalid login.')
        else:
            session['user'] = email
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.')
    return redirect(url_for('index'))


# @app.route('/add_post', methods=['POST'])
# def add_post():
#     title = request.form['title']
#     tags = request.form['tags']
#     text = request.form['text']
#
#     if not title:
#         flash('You must give your post a title.')
#     elif not tags:
#         flash('You must give your post at least one tag.')
#     elif not text:
#         flash('You must give your post a text body.')
#     else:
#         User(session['username']).add_post(title, tags, text)
#
#     return redirect(url_for('index'))

#
# @app.route('/like_post/<post_id>')
# def like_post(post_id):
#     username = session.get('username')
#
#     if not username:
#         flash('You must be logged in to like a post.')
#         return redirect(url_for('login'))
#
#     User(username).like_post(post_id)
#
#     flash('Liked post.')
#     return redirect(request.referrer)
#
#


@app.route('/profile')
def profile():

    current_user_email = session.get('user')

    if current_user_email is not None:
        current_user = User(current_user_email)
        user_details = current_user.find()

        name = user_details['name']
        bio = user_details['bio']
        school = user_details['school']
        position = user_details['position']
        group = user_details['group']

        print user_details
        flash("HERE")

        return render_template(
            'profile.html',
            name=name
        )

    return render_template('not_authorized.html')


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        # do stuff here
        render_template('index.html')
    return render_template('CreateEvent.html')

#
# ################################################################################
# #  My Routes
# ################################################################################
# @app.route('/get_sentiment_history_search')
# def get_sentiment_history_search():
#     return render_template('sentiment_history_search.html')
#
#
# @app.route('/get_sentiment_history', methods=['POST'])
# def get_sentiment_history():
#     company = request.form['company_ticker']
#     sentiment_time_data = get_sentiment_over_time(company)
#     return render_template(
#         'sentiment_history.html',
#         data=sentiment_time_data,
#         ticker=company
#     )
