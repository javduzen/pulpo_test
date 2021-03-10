from flask import url_for, redirect, render_template, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm, db
from app.forms import ExampleForm, LoginForm
from app.models import User, ModelExample


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/list/')
def posts():
	return render_template('list.html')

#a basic form
@app.route('/new/')
#@login_required
def new():
	form = ExampleForm()

	return render_template('new.html', form=form)


@app.route('/save/', methods = ['GET','POST'])
#@login_required
def save():
	form = ExampleForm()
	if form.validate_on_submit():
		print("saving data:")
		title = form.title.data
		content = form.content.data
		new_data = ModelExample(title=title, content=content)
		db.session.add(new_data)
		db.session.commit()
		flash('Load successfull')
		return redirect(url_for('index'))
	return render_template('new.html', form=form)


@app.route('/view/<id>/')
def view(id):
	return render_template('view.html')

# === User login methods ===

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(g.user)

    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

# ====================
