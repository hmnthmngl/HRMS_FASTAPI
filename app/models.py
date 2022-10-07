
from typing import Text
from database import Base
from sqlalchemy import Column, Integer,String, Boolean, ForeignKey, Date,DATETIME,Time
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from sqlalchemy.orm import relationship
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

class BaseEntity:
	created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
	created_by = Column(GUID,nullable=True)
	modified_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
	modified_by = Column(GUID,nullable=True)
	status = Column(Integer,nullable=True)
	comments = Column(String(255),nullable=True)


class Users(Base,BaseEntity):
	__tablename__ = 'users'

	id = Column(GUID,server_default=GUID_SERVER_DEFAULT_POSTGRESQL,primary_key=True,nullable=False)
	user_name = Column(String(120),nullable=False)
	password = Column(String(120),nullable=False)
	reset_password = Column(Boolean,nullable=False)


class Roles(Base):
	__tablename__ = 'roles'

	id = Column(Integer,primary_key=True,nullable=False)
	role_name = Column(String(120),nullable=False,unique=True)


class Privileges(Base):
	__tablename__ = 'privileges'

	id = Column(Integer,primary_key=True,nullable=False)
	privilege_name = Column(String(120),nullable=False,unique=True)



class RolePrivileges(Base):
	__tablename__ = 'role_privileges'
	role_id = Column(Integer,ForeignKey("roles.id",ondelete="CASCADE"),primary_key=True,nullable=False)
	privilege_id = Column(Integer,ForeignKey("privileges.id",ondelete="CASCADE"),primary_key=True,nullable=False)



class UserRoles(Base):
	__tablename__ = 'user_roles'
	user_id = Column(GUID,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)
	role_id = Column(Integer,ForeignKey("roles.id",ondelete="CASCADE"),primary_key=True,nullable=False)


class Designation(Base):
	__tablename__ = 'designation'

	designation_id = Column(Integer,primary_key=True,nullable=False)
	designation_name = Column(String(75),nullable=False,unique=True)


class Department(Base):
	__tablename__ = 'department'

	department_id = Column(Integer,primary_key=True,nullable=False)
	department_name = Column(String(75),nullable=False,unique=True)


class EmployementType(Base):
	__tablename__ = 'employement_type'

	id = Column(Integer,primary_key=True,nullable=False)
	type = Column(String(75),nullable=False,unique=True)


class TerminatioReason(Base):
	__tablename__ = 'termination_reason'

	id = Column(Integer,primary_key=True,nullable=False)
	intent = Column(String(75),nullable=False)
	reason = Column(String(75),nullable=False)


class EmployeeInactiveReason(Base):
	__tablename__ = 'employee_inactive_reason'

	id = Column(Integer,primary_key=True,nullable=False)
	type = Column(String(75),nullable=False,unique=True)


class Employees(Base,BaseEntity):
	__tablename__ = 'employee'

	id = Column(GUID,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)
	employee_number = Column(String(12),nullable=False,unique=True)
	first_name = Column(String(75),nullable=False)
	middle_name = Column(String(75),nullable=True)
	last_name = Column(String(75),nullable=False)
	email_id = Column(String(150),nullable=False,unique=True) 
	primary_phone_number = Column(String(15),nullable=False,unique=True)
	secondary_phone_number = Column(String(15),nullable=True,unique=True)
	dob = Column(Date,nullable=True)
	gender = Column(Integer,nullable=True)
	marital_status = Column(Integer,nullable=True)
	employement_start_date = Column(Date,nullable=False)
	employement_end_date = Column(Date,nullable=True)
	rehire_eligibility = Column(Boolean,nullable=True)
	billable_resource = Column(Boolean,nullable=True)
	termination_date = Column(Date,nullable=True)
	designation_id = Column(Integer,ForeignKey("designation.designation_id",ondelete="CASCADE"),nullable=False)
	department_id = Column(Integer,ForeignKey("department.department_id",ondelete="CASCADE"),nullable=False)
	employement_type_id = Column(Integer,ForeignKey("employement_type.id",ondelete="CASCADE"),nullable=False)
	termination_reason__id = Column(Integer,ForeignKey("termination_reason.id",ondelete="CASCADE"),nullable=True)
	emp_inactive_reason_id = Column(Integer,ForeignKey("employee_inactive_reason.id",ondelete="CASCADE"),nullable=True)
	reporting_manager_id = Column(GUID,ForeignKey("employee.id",ondelete="CASCADE"),nullable=True)
	l2_manager_id = Column(GUID,ForeignKey("employee.id",ondelete="CASCADE"),nullable=True)


class EmployeeInviteStatus(Base,BaseEntity):  
	__tablename__ = 'invite_status'

	invite_id = Column(Integer, primary_key=True)
	employee_number = Column(String(15), nullable=False)
	employee_email = Column(String(120), nullable=False)
	role_id = Column(Integer,ForeignKey("roles.id",ondelete="CASCADE"),primary_key=True,nullable=False)
	designation_id = Column(Integer,ForeignKey("designation.designation_id",ondelete="CASCADE"),nullable=False)
	department_id = Column(Integer,ForeignKey("department.department_id",ondelete="CASCADE"),nullable=False)
	employement_type_id = Column(Integer,ForeignKey("employement_type.id",ondelete="CASCADE"),nullable=False)
	reporting_manager_id = Column(GUID,ForeignKey("employee.id",ondelete="CASCADE"),nullable=True)
	l2_manager_id = Column(GUID,ForeignKey("employee.id",ondelete="CASCADE"),nullable=True)
	joining_date = Column(Date, nullable=True)
	billable_resource = Column(String(1),nullable=True)
	invitation_status = Column(String(10), nullable=False)
	sent_time = Column(Date, nullable=False) 

class PasswordMailStatus(Base):         
    __tablename__ = 'password_mail_status'

    token_id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(255), nullable=False)
    token_status = Column(String(30), nullable=False) 


class ProjectEmployee(Base):
	__tablename__ = 'project_employee'
	project_id = Column(GUID,ForeignKey("projects.id",ondelete="CASCADE"),primary_key=True,nullable=False)
	employee_id = Column(GUID,ForeignKey("employee.id",ondelete="CASCADE"),primary_key=True,nullable=False)


class TimeSheetsType(Base):
	__tablename__ = 'time_sheets_type'

	id = Column(Integer,primary_key=True,nullable=False)
	type = Column(String(75),nullable=False)

class TimeSheets(Base,BaseEntity):
	__tablename__ = 'time_sheets'

	id = Column(GUID,server_default=GUID_SERVER_DEFAULT_POSTGRESQL,primary_key=True,nullable=False)
	employee_id = Column(GUID,ForeignKey("employee.id",ondelete="CASCADE"),nullable=False)
	project_id = Column(GUID,ForeignKey("projects.id",ondelete="CASCADE"),nullable=False)
	ts_type_id = Column(Integer,ForeignKey("time_sheets_type.id",ondelete="CASCADE"),nullable=False)
	department_id = Column(Integer,ForeignKey("department.department_id",ondelete="CASCADE"),nullable=False)
	ts_start_time=Column(Time,nullable=False)
	ts_end_time=Column(Time,nullable=False)
	approval_level=Column(Integer,nullable=False)
	ts_date=Column(Date,nullable=False) 

class ProjectType(Base):
	__tablename__ = 'project_type'

	id = Column(Integer,primary_key=True,nullable=False)
	project_type = Column(String(120),nullable=False,unique=True)


class Projects(Base,BaseEntity):
	__tablename__ = 'projects'

	id = Column(GUID,server_default=GUID_SERVER_DEFAULT_POSTGRESQL,primary_key=True,nullable=False)
	project_name = Column(String(255),nullable=False,unique=True)
	project_type_id = Column(Integer,ForeignKey("project_type.id",ondelete="CASCADE"),nullable=False)
	department_id = Column(Integer,ForeignKey("department.department_id",ondelete="CASCADE"),nullable=False)
	scheduled_start_date = Column(Date,nullable=True)
	scheduled_end_date = Column(Date,nullable=True)
	actual_start_date = Column(Date,nullable=True)
	actual_end_date = Column(Date,nullable=True)
	project_description = Column(String,nullable=True)


class Dashboard_Status(Base):
	__tablename__ = 'dashboard_status'

	id = Column(Integer,primary_key=True,nullable=False)
	date = Column(Date,nullable=False)
	billable = Column(Integer,nullable=False)
	non_billable = Column(Integer,nullable=False)
	on_billing = Column(Integer,nullable=False)
	on_bench = Column(Integer,nullable=False)
	total_employees = Column(Integer,nullable=False)
	

# class BaseEntity:
# 	created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
# 	created_by = Column(GUID,nullable=True)
# 	modified_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
# 	modified_by = Column(GUID,nullable=True)
# 	status = Column(Integer,nullable=True)
# 	comments = Column(String(255),nullable=True)


# class Users(Base,BaseEntity):
# 	__tablename__ = 'users'

# 	id = Column(GUID,server_default=GUID_SERVER_DEFAULT_POSTGRESQL,primary_key=True,nullable=False)
# 	user_name = Column(String(120),nullable=False)
# 	password = Column(String(120),nullable=False)
# 	reset_password = Column(Boolean,nullable=False)


# class Roles(Base):
# 	__tablename__ = 'roles'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	role_name = Column(String(120),nullable=False,unique=True)


# class Privileges(Base):
# 	__tablename__ = 'privileges'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	privilege_name = Column(String(120),nullable=False,unique=True)

# class RolePrivileges(Base):
# 	__tablename__ = 'role_privileges'
# 	role_id = Column(Integer,ForeignKey("roles.id",ondelete="CASCADE"),primary_key=True,nullable=False)
# 	privilege_id = Column(Integer,ForeignKey("privileges.id",ondelete="CASCADE"),primary_key=True,nullable=False)
# 	role = relationship("Roles")
# 	privilege = relationship("Privileges")


# class UserRoles(Base):
# 	__tablename__ = 'user_roles'
# 	user_id = Column(GUID,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)
# 	role_id = Column(Integer,ForeignKey("roles.id",ondelete="CASCADE"),primary_key=True,nullable=False)
# 	role = relationship("Roles")

# class Designation(Base):
# 	__tablename__ = 'designation'

# 	designation_id = Column(Integer,primary_key=True,nullable=False)
# 	designation_name = Column(String(75),nullable=False,unique=True)

# class Department(Base):
# 	__tablename__ = 'department'

# 	department_id = Column(Integer,primary_key=True,nullable=False)
# 	department_name = Column(String(75),nullable=False,unique=True)

# class EmployementType(Base):
# 	__tablename__ = 'employement_type'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	type = Column(String(75),nullable=False,unique=True)

# class TerminatioReason(Base):
# 	__tablename__ = 'termination_reason'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	intent = Column(String(75),nullable=False)
# 	reason = Column(String(75),nullable=False)

# class EmployeeInactiveReason(Base):
# 	__tablename__ = 'employee_inactive_reason'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	type = Column(String(75),nullable=False,unique=True)


# class Employees(Base,BaseEntity):
# 	__tablename__ = 'employee'

# 	id = Column(GUID,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,nullable=False)
# 	employee_id = Column(String(12),nullable=False,unique=True)
# 	first_name = Column(String(75),nullable=False)
# 	middle_name = Column(String(75),nullable=True)
# 	last_name = Column(String(75),nullable=False)
# 	email_id = Column(String(150),nullable=False,unique=True) 
# 	primary_phone_number = Column(String(15),nullable=False,unique=True)
# 	secondary_phone_number = Column(String(15),nullable=True,unique=True)
# 	dob = Column(Date,nullable=True)
# 	gender = Column(Integer,nullable=True)
# 	marital_status = Column(Integer,nullable=True)
# 	employement_start_date = Column(Date,nullable=False)
# 	employement_end_date = Column(Date,nullable=True)
# 	rehire_eligibility = Column(Boolean,nullable=True)
# 	billable_resource = Column(Boolean,nullable=True)
# 	termination_date = Column(Date,nullable=True)
# 	designation_id = Column(Integer,ForeignKey("designation.designation_id",ondelete="CASCADE"),nullable=False)
# 	department_id = Column(Integer,ForeignKey("department.department_id",ondelete="CASCADE"),nullable=False)
# 	employement_type_id = Column(Integer,ForeignKey("employement_type.id",ondelete="CASCADE"),nullable=False)
# 	termination_reason__id = Column(Integer,ForeignKey("termination_reason.id",ondelete="CASCADE"),nullable=True)
# 	emp_inactive_reason_id = Column(Integer,ForeignKey("employee_inactive_reason.id",ondelete="CASCADE"),nullable=True)


# class EmployeeInviteStatus(Base,BaseEntity):  
# 	__tablename__ = 'invite_status'

# 	invite_id = Column(Integer, primary_key=True)
# 	employee_number = Column(String(15), nullable=False)
# 	employee_email = Column(String(120), nullable=False)
# 	role_id = Column(Integer,ForeignKey("roles.id",ondelete="CASCADE"),primary_key=True,nullable=False)
# 	designation_id = Column(Integer,ForeignKey("designation.designation_id",ondelete="CASCADE"),nullable=False)
# 	department_id = Column(Integer,ForeignKey("department.department_id",ondelete="CASCADE"),nullable=False)
# 	employement_type_id = Column(Integer,ForeignKey("employement_type.id",ondelete="CASCADE"),nullable=False)
# 	joining_date = Column(Date, nullable=True)
# 	billable_resource = Column(String(1),nullable=True)
# 	invitation_status = Column(String(10), nullable=False)
# 	sent_time = Column(Date, nullable=False) 

# class PasswordMailStatus(Base):         
#     __tablename__ = 'password_mail_status'

#     token_id = Column(Integer, primary_key=True, autoincrement=True)
#     token = Column(String(255), nullable=False)
#     token_status = Column(String(30), nullable=False) 

# class ProjectEmployee(Base):
# 	__tablename__ = 'project_employee'
# 	project_id = Column(GUID,ForeignKey("projects.id",ondelete="CASCADE"),primary_key=True,nullable=False)
# 	employee_id = Column(GUID,ForeignKey("employee.id",ondelete="CASCADE"),primary_key=True,nullable=False)


# class TimeSheetsType(Base):
# 	__tablename__ = 'time_sheets_type'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	type = Column(String(75),nullable=False)

# class TimeSheets(Base,BaseEntity):
# 	__tablename__ = 'time_sheets'

# 	id = Column(GUID,server_default=GUID_SERVER_DEFAULT_POSTGRESQL,primary_key=True,nullable=False)
# 	employee_id = Column(GUID,ForeignKey("employee.id",ondelete="CASCADE"),nullable=False)
# 	project_id = Column(GUID,ForeignKey("projects.id",ondelete="CASCADE"),nullable=False)
# 	ts_type_id = Column(Integer,ForeignKey("time_sheets_type.id",ondelete="CASCADE"),nullable=False)
# 	department_id = Column(Integer,ForeignKey("department.department_id",ondelete="CASCADE"),nullable=False)
# 	ts_start_time=Column(Time,nullable=False)
# 	ts_end_time=Column(Time,nullable=False)
# 	approval_level=Column(Integer,nullable=False)
# 	ts_date=Column(Date,nullable=False) 

# class ProjectType(Base):
# 	__tablename__ = 'project_type'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	project_type = Column(String(120),nullable=False,unique=True)

# class Projects(Base,BaseEntity):
# 	__tablename__ = 'projects'

# 	id = Column(GUID,server_default=GUID_SERVER_DEFAULT_POSTGRESQL,primary_key=True,nullable=False)
# 	project_name = Column(String(255),nullable=False,unique=True)
# 	project_type_id = Column(Integer,ForeignKey("project_type.id",ondelete="CASCADE"),nullable=False)
# 	department_id = Column(Integer,ForeignKey("department.department_id",ondelete="CASCADE"),nullable=False)
# 	project_manager_id = Column(GUID,ForeignKey("employee.id",ondelete="CASCADE"),nullable=False)
# 	work_location = Column(String(75),nullable=True)
# 	scheduled_start_date = Column(Date,nullable=True)
# 	scheduled_end_date = Column(Date,nullable=True)
# 	actual_start_date = Column(Date,nullable=True)
# 	actual_end_date = Column(Date,nullable=True)
# 	project_description = Column(String,nullable=True)


# class Dashboard_Status(Base):
# 	__tablename__ = 'dashboard_status'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	date = Column(Date,nullable=False)
# 	billable = Column(Integer,nullable=False)
# 	non_billable = Column(Integer,nullable=False)
# 	on_billing = Column(Integer,nullable=False)
# 	on_bench = Column(Integer,nullable=False)
# 	total_employees = Column(Integer,nullable=False)


	




  







# class Countries(Base):
# 	__tablename__ = 'countries'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	name = Column(String(75),nullable=False,unique=True)

# class States(Base):
# 	__tablename__ = 'states'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	name = Column(String(75),nullable=False,unique=True)
# 	country_id = Column(Integer,ForeignKey("countries.id",ondelete="CASCADE"),nullable=False)

# class Cities(Base):
# 	__tablename__ = 'cities'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	name = Column(String(75),nullable=False)
# 	country_id = Column(Integer,ForeignKey("countries.id",ondelete="CASCADE"),nullable=False)
# 	state_id = Column(Integer,ForeignKey("states.id",ondelete="CASCADE"),nullable=False)
    

# class Address(Base,BaseEntity):
# 	__tablename__ = 'address'
# 	id = Column(GUID,server_default=GUID_SERVER_DEFAULT_POSTGRESQL,primary_key=True,nullable=False)
# 	line1 = Column(String(255),nullable=False)
# 	line2 = Column(String(255),nullable=False)
# 	zip = Column(String(10),nullable=False)
# 	country_id = Column(Integer,ForeignKey("countries.id",ondelete="CASCADE"),nullable=False)
# 	state_id = Column(Integer,ForeignKey("states.id",ondelete="CASCADE"),nullable=False)
# 	city_id = Column(Integer,ForeignKey("cities.id",ondelete="CASCADE"),nullable=False)

# class StaffingSupplier(Base,BaseEntity):
# 	__tablename__ = 'staffing_supplier'
# 	id = Column(GUID,server_default=GUID_SERVER_DEFAULT_POSTGRESQL,primary_key=True,nullable=False)
# 	supplier_name = Column(String(255),nullable=False)
# 	contact_number = Column(String(15),nullable=False)
# 	termination_reason = Column(String(255),nullable= True)
# 	company_website_url = Column(String(255),nullable= True)

# class SupplierAddress(Base):
# 	__tablename__ = 'supplier_address'
# 	supplier_id = Column(GUID,ForeignKey("staffing_supplier.id",ondelete="CASCADE"),primary_key=True,nullable=False)
# 	address_id = Column(GUID,ForeignKey("address.id",ondelete="CASCADE"),primary_key=True,nullable=False)

# class SupplierContactType(Base):
# 	__tablename__ = 'supplier_contact_type'

# 	id = Column(Integer,primary_key=True,nullable=False)
# 	name = Column(String(75),nullable=False)

# class SupplierContact(Base,BaseEntity):
# 	__tablename__ = 'supplier_contact'
# 	id = Column(GUID,server_default=GUID_SERVER_DEFAULT_POSTGRESQL,primary_key=True,nullable=False)
# 	supplier_id = Column(GUID,ForeignKey("staffing_supplier.id",ondelete="CASCADE"),nullable=False)
# 	first_name = Column(String(75),nullable=False)
# 	middle_name = Column(String(75),nullable=True)
# 	last_name = Column(String(75),nullable=False)
# 	email_id = Column(String(150),nullable=False,unique=True) 
# 	phone_number = Column(String(15),nullable=False,unique=True)
# 	supplier_contact_type_id = Column(Integer,ForeignKey("supplier_contact_type.id",ondelete="CASCADE"),nullable=False)

# class Consultant(Base,BaseEntity):
# 	__tablename__ = 'consultant'

# 	id = Column(GUID,server_default=GUID_SERVER_DEFAULT_POSTGRESQL,primary_key=True,nullable=False)
# 	supplier_id = Column(GUID,ForeignKey("staffing_supplier.id",ondelete="CASCADE"),nullable=False)
# 	first_name = Column(String(75),nullable=False)
# 	middle_name = Column(String(75),nullable=True)
# 	last_name = Column(String(75),nullable=False)
# 	email_id = Column(String(150),nullable=False,unique=True) 
# 	phone_number = Column(String(15),nullable=False,unique=True)
# 	dob = Column(Date,nullable=True)
# 	gender = Column(Integer,nullable=True)
# 	rehire_eligibility = Column(Boolean,nullable=True)
# 	termination_reason = Column(String(255),nullable=True)


	