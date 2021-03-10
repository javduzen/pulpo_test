from flask_wtf import FlaskForm
from wtforms  import TextField, TextAreaField, DateTimeField, PasswordField
from wtforms.validators import Required

class ExampleForm(FlaskForm):
	#title = TextField(u'Title', validators = [Required()])
	title = TextAreaField(u'Title', validators = [Required()])
	content = TextAreaField(u'Content')
	date = DateTimeField(u'Date', format='%d/%m/%Y %H:%M')
	#recaptcha = RecaptchaField(u'Recaptcha')

class LoginForm(FlaskForm):
	user = TextField(u'User', validators = [Required()])
	password = PasswordField(u'Password', validators = [Required()])
