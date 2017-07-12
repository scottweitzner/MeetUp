from flask import Flask, request, session, redirect, url_for, render_template, flash
from .models import User, get_skill_and_interest_suggestions, filter_duplicate_skills, filter_duplicate_interests, get_all_events


# import classes and functions from models an initialize app

app = Flask(__name__)


@app.route('/')
def index():
    events = get_all_events()
    return render_template('index.html', events=events)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        if not User(email).verify_password(password):
            error = "Invalid Login"
            flash('Invalid login.')
        else:
            session['user'] = email
            flash('Logged in!')
            return redirect(url_for('index'))

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.')
    return redirect(url_for('index'))


@app.route('/profile')
def profile():

    current_user_email = session.get('user', None)

    if current_user_email is not None:
        current_user = User(current_user_email)
        user_details = current_user.find()

        name = user_details['name']
        bio = user_details['bio']
        school = user_details['school']
        position = user_details['position']
        group = user_details['group']

        skills = current_user.get_skills()
        interests = current_user.get_interests()

        raw_suggestions = get_skill_and_interest_suggestions(bio)
        skill_suggestions = filter_duplicate_skills(raw_suggestions, skills)
        interest_suggestions = filter_duplicate_interests(raw_suggestions, interests)

        return render_template(
            'profile.html',
            name=name,
            bio=bio,
            school=school,
            position=position,
            group=group,
            skills=skills,
            interests=interests,
            skill_suggestions=skill_suggestions,
            interest_suggestions=interest_suggestions
        )

    return render_template('not_authorized.html')


@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():

    current_user_email = session.get('user', None)

    if not current_user_email:
        return render_template('not_authorized.html')

    if request.method == 'POST':
        title = request.form.get('title')
        event_type = request.form.get('type')
        date = request.form.get('date')
        time = request.form.get('time')
        max_participants = request.form.get('max_participants')
        description = request.form.get('description', None)

        current_user = User(current_user_email)
        current_user.create_event(title, event_type, date, time, max_participants, "" if description is None else description)
        flash("Event Created!")
        return render_template('index.html')

    return render_template('create_event.html')


@app.route('/add_skills', methods=['POST'])
def add_skills():
    current_user_email = session.get('user', None)

    if not current_user_email:
        return render_template('not_authorized.html')

    if request.method == 'POST':
        current_user = User(current_user_email)
        skills = request.json['tags']
        current_user.add_skills(skills)
        return profile()

    return render_template('profile.html')


@app.route('/add_interests', methods=['POST'])
def add_interests():
    current_user_email = session.get('user', None)

    if not current_user_email:
        return render_template('not_authorized.html')

    if request.method == 'POST':
        current_user = User(current_user_email)
        interests = request.json['tags']
        current_user.add_interests(interests)
        return profile()

    return render_template('profile.html')


@app.route('/get_events')
def get_events():
    events = get_all_events()
    render_template(
        'calendar.html',
        events=events
    )

