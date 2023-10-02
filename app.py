"""User creation and authentication practice"""

from flask import Flask, jsonify, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickens"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/feedback', methods=['GET', 'POST'])
def show_feedback():
    if "username" not in session:
        flash("Please login first.")
        return redirect('/login')
    form = FeedbackForm()
    feedbacks = Feedback.query.all()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=session['username'])
        db.session.add(new_feedback)
        db.session.commit()
        flash("Feedback created")
        redirect('/feedback')
    return render_template('feedback.html', form=form, feedbacks=feedbacks)

@app.route('/feedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    if 'username' not in session:
        flash("Please log in first ")
        return redirect('/login')
    feedback = Feedback.query.get_or_404(id)
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback deleted')
        return redirect('/feedback')
    flash("You don't have permission to do that")
    return redirect('/feedback')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        
        session['username'] = new_user.username
        db.session.add(new_user)
        db.session.commit()
        flash('Welcome! Account successfully created')
        return redirect('/feedback')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!")
            session['username'] = user.username
            return redirect('/feedback')
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    #better practice to use a post request 
    session.pop('username')
    flash("Goodbye!")
    return redirect('/')