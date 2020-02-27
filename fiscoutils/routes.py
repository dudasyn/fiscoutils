from flask import render_template, url_for, flash, redirect
from fiscoutils import app
from fiscoutils.forms import RegistrationForm, LoginForm
from fiscoutils.models import User, Post

# Some dumb data
posts = [

    {
        'author': 'Corey Schafer',
        'title': 'Blog Post n 1',
        'content': 'April 20,2018'
    },
    {
        'author': 'Eduardo de Santana',
        'title': 'Blog Post n 2',
        'content': 'April 21,2017'
    },
    {
        'author': 'Julia Bandeira',
        'title': 'Blog Post n 5',
        'content': 'April 15,2017'
    }
]

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
