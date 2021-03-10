from flask import url_for, redirect, render_template, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm, db
from app.forms import ExampleForm, LoginForm
from app.models import User, ModelExample

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_login import LoginManager

from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision
from google.cloud import bigquery


#CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET")

app = Flask(__name__)

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
		client = bigquery.Client()
		table_id = "flask-app-307203.cryptopulo.table1"    
		rows_to_insert = [
				{u"title": title, u"contente": content}
		]
		errors = client.insert_rows_json(table_id, rows_to_insert, skip_invalid_rows=True, ignore_unknown_values=True)
		if errors == []:
            print("New rows have been added.")
    	else:
        	print("Encountered errors while inserting rows: {}".format(errors))
		flash('Load successfull')

		return redirect(url_for('index'))
	return render_template('new.html', form=form)


@app.route('/view/<id>/')
def view(id):
	return render_template('view.html')


# ====================
@app.errorhandler(500)
def server_error(e):
    logging.exception("An error occurred during a request.")
    return (
        """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(
            e
        ),
        500,
    )


if __name__ == "__main__":
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)