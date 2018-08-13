from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm, OrganizationRegistrationForm
from .. import db
from ..models import Employee, Organization


@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		employee = Employee(email=form.email.data,
							username=form.username.data,
							first_name=form.first_name.data,
							last_name=form.last_name.data,
							password=form.password.data)

		# add employee to the database
		db.session.add(employee)
		db.session.commit() 
		flash('You have successfully registered %s. Please log in as employee to verify functionality.' % employee.username)

		# redirect to the login page
		return redirect(url_for('auth.login'))

	# load registration template
	return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():

		# check whether employee exists in the database and whether
		# the password entered matches the password in the database
		employee = Employee.query.filter_by(email=form.email.data).first()
		if employee is not None and employee.verify_password(form.password.data):
			# log employee in
			login_user(employee)

			# redirect to the appropriate dashboard page
			if employee.is_admin:
				return redirect(url_for('home.admin_dashboard'))
			
			elif employee.role_id==1:
				return redirect(url_for('home.biteam_dashboard'))
			
			elif employee.role_id==2:
				return redirect(url_for('home.client_dashboard'))
			else:
				
				return redirect(url_for('home.dashboard'))

		# when login details are incorrect
		else:
			flash('Invalid email or password.')

	# load login template
	return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have successfully been logged out.')

	# redirect to the login page
	return redirect(url_for('auth.login'))

@auth.route('/organization_register', methods=['GET', 'POST'])
def organization_register():
	form = OrganizationRegistrationForm()
	if form.validate_on_submit():
		organization = Organization(organization_id=form.organization_id.data,
							company_name=form.company_name.data,
							load_variables=form.load_variables.data,
							variables=form.variables.data,
							contact_info=form.contact_info.data)

		# add employee to the database
		db.session.add(organization)
		db.session.commit() 
		flash('You have successfully registered %s.' % organization.company_name)

		# redirect to the login page
		return redirect(url_for('admin.list_organizations'))

	# load registration template
	return render_template('auth/organization_register.html', form=form, title='Organization Register')