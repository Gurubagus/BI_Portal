from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Employee


class RegistrationForm(FlaskForm):
	"""
	Form for users to create new account
	"""
	email = StringField('Email', validators=[DataRequired(), Email()])
	username = StringField('Username', validators=[DataRequired()])
	first_name = StringField('First Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(),
													 EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm Password')
	submit = SubmitField('Register')

	def validate_email(self, field):
		if Employee.query.filter_by(email=field.data).first():
			raise ValidationError('Email is already in use.')

	def validate_username(self, field):
		if Employee.query.filter_by(username=field.data).first():
			raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
	"""
	Form for users to login
	"""
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')

class OrganizationRegistrationForm(FlaskForm):
	"""
	Form for users to create organization entry
	"""
	organization_id = StringField('Organization ID', validators=[DataRequired()])
	company_name = StringField('Company Name', validators=[DataRequired()])
	load_variables = StringField('Load Variables', validators=[DataRequired()])
	variables = StringField('Variables', validators=[DataRequired()])
	contact_info = StringField('Contact Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Submit')

	def validate_copmany(self, field):
		if Employee.query.filter_by(company_name=field.data).first():
			raise ValidationError('Organization already exists in the database.')

	def validate_username(self, field):
		if Employee.query.filter_by(organization_id=field.data).first():
			raise ValidationError('Organization ID is already in use.')