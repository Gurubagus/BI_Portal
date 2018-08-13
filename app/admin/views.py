from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required 

from . import admin
from forms import DepartmentForm, EmployeeAssignForm, RoleForm, OrganizationAssignForm
from .. import db
from ..models import Department, Employee, Role, Organization



def check_admin():
	# prevent non-admins from accessing the page
	if not current_user.is_admin:
		abort(403)
	
def check_client_permission():
	# prevents non-authorized users from accessing through url
	
	if not current_user.role_id==2:	
		check_admin()


		
def check_BI_permission():
	# prevents non-authorized users from accessing through url
	
	if not current_user.role_id==1:		
		check_admin()




# Department Views

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
	"""
	List all departments
	"""
	check_BI_permission()
	departments = Department.query.all()
	
	return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")

@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
	"""
	Add a department to the database
	"""
	check_BI_permission()
	
	add_department = True

	form = DepartmentForm()
	if form.validate_on_submit():
		department = Department(name=form.name.data,
								description=form.description.data)
		try:
			# add department to the database
			db.session.add(department)
			db.session.commit()
			flash('You have successfully added a new department.')
		except:
			# in case department name already exists
			flash('Error: department name already exists.')

		# redirect to departments page
		return redirect(url_for('admin.list_departments'))

	# load department template
	return render_template('admin/departments/department.html', action="Add",
						   add_department=add_department, form=form,
						   title="Add Department")


@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
	"""
	Edit a department
	"""
	check_BI_permission()

	add_department = False

	department = Department.query.get_or_404(id)
	form = DepartmentForm(obj=department)
	if form.validate_on_submit():
		department.name = form.name.data
		department.description = form.description.data
		db.session.commit()
		flash('You have successfully edited the department.')

		# redirect to the departments page
		return redirect(url_for('admin.list_departments'))

	form.description.data = department.description
	form.name.data = department.name
	return render_template('admin/departments/department.html', action="Edit",
						   add_department=add_department, form=form,
						   department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
	"""
	Delete a department from the database
	"""
	check_BI_permission()
	
	department = Department.query.get_or_404(id)
	db.session.delete(department)
	db.session.commit()
	flash('You have successfully deleted the department.')

	# redirect to the departments page
	return redirect(url_for('admin.list_departments'))

	return render_template(title="Delete Department")


# Role Views

@admin.route('/roles')
@login_required
def list_roles():
	check_admin()
	
	"""
	List all roles
	"""
	roles = Role.query.all()
	return render_template('admin/roles/roles.html',
						   roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
	"""
	Add a role to the database
	"""
	check_admin()

	add_role = True

	form = RoleForm()
	if form.validate_on_submit():
		role = Role(name=form.name.data,
					description=form.description.data)

		try:
			# add role to the database
			db.session.add(role)
			db.session.commit()
			flash('You have successfully added a new role.')
		except:
			# in case role name already exists
			flash('Error: role name already exists.')

		# redirect to the roles page
		return redirect(url_for('admin.list_roles'))

	# load role template
	return render_template('admin/roles/role.html', add_role=add_role,
						   form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
	"""
	Edit a role
	"""
	
	check_admin()
	
	add_role = False

	role = Role.query.get_or_404(id)
	form = RoleForm(obj=role)
	if form.validate_on_submit():
		role.name = form.name.data
		role.description = form.description.data
		db.session.add(role)
		db.session.commit()
		flash('You have successfully edited the role.')

		# redirect to the roles page
		return redirect(url_for('admin.list_roles'))

	form.description.data = role.description
	form.name.data = role.name
	return render_template('admin/roles/role.html', add_role=add_role,
						   form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
	"""
	Delete a role from the database
	"""
	check_admin()
	
	role = Role.query.get_or_404(id)
	db.session.delete(role)
	db.session.commit()
	flash('You have successfully deleted the role.')

	# redirect to the roles page
	return redirect(url_for('admin.list_roles'))

	return render_template(title="Delete Role")


# Employee Views

@admin.route('/employees')
@login_required
def list_employees():
	"""
	List all employees
	"""
	check_admin()

	employees = Employee.query.all()
	return render_template('admin/employees/employees.html',
						   employees=employees, title='Employees')


@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
	"""
	Assign a department and a role to an employee
	"""
	check_admin()

	employee = Employee.query.get_or_404(id)

	# prevent admin from being assigned a department or role
	if employee.is_admin:
		abort(403)

	form = EmployeeAssignForm(obj=employee)
	if form.validate_on_submit():
		employee.department = form.department.data
		employee.role = form.role.data
		db.session.add(employee)
		db.session.commit()
		flash('You have successfully assigned a department and role.')

		# redirect to the roles page
		return redirect(url_for('admin.list_employees'))

	return render_template('admin/employees/employee.html',
						   employee=employee, form=form,
						   title='Assign Employee')

@admin.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required

def delete_employee(id):
	"""
	Delete an employee from the database
	"""
	check_admin()
	
	employee = Employee.query.get_or_404(id)
	db.session.delete(employee)
	db.session.commit()
	flash('You have successfully deleted the employee.')

	# redirect to the roles page
	return redirect(url_for('admin.list_employees'))

	return render_template('admin/employees/employee.html',
						   employee=employee, form=form,
						   title='Assign Employee')

# Organizations Views

@admin.route('/organizations')
@login_required
def list_organizations():
	"""
	List all organizations
	"""
	check_BI_permission()

	organizations = Organization.query.all()
	return render_template('admin/organizations/organizations.html',
						   organizations=organizations, title='Organizations')


@admin.route('/organizations/assign/<id>', methods=['GET', 'POST'])
@login_required
def assign_organizations(id):
	"""
	Assign Load Variables and Variables to an organization
	"""
	check_BI_permission()

	organization = Organization.query.get_or_404(id)

	form = OrganizationAssignForm(obj=organization)
	if form.validate_on_submit():
		organization.load_variables = form.load_variables.data
		organization.variables = form.variables.data
		db.session.add(organization)
		db.session.commit()
		flash('You have successfully assigned new Load Variables and Variables.')

		# redirect to the roles page
		return redirect(url_for('admin.list_organizations'))

	return render_template('admin/organizations/organization.html',
						   organization=organization, form=form,
						   title='Assign Organization')

@admin.route('/organizations/delete/<id>', methods=['GET', 'POST'])
@login_required

def delete_organization(id):
	"""
	Delete an organization from the database
	"""
	check_BI_permission()
	
	organization = Organization.query.get_or_404(id)
	db.session.delete(organization)
	db.session.commit()
	flash('You have successfully deleted the organization.')

	# redirect to the roles page
	return redirect(url_for('admin.list_organizations'))

	return render_template('admin/organizations/organizations.html',
						   organizations=organizations, form=form,
						   title='Assign Organization')