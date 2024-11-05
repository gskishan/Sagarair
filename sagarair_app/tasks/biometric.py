import requests
import frappe, json
from frappe.utils.data import now,get_datetime,get_datetime_str
from frappe.utils import (
	add_days,
	time_diff,
	now
)
import json

def get_checkins():
	url = 'https://sagaraircheckin-8grgp13z9-mohammed-zafars-projects.vercel.app'
	
	# Date Time String Format 2024-06-22 00:00:00.000000
	# response = requests.get(f"{url}?from_date={'2024-07-09 00:00:00.000000'}&to_date={'2024-07-09 23:00:00.000000'}")
	response = requests.get(f"{url}?from_date={get_datetime_str(add_days(now(),-1))}&to_date={get_datetime_str(now())}")
	data = response.content.decode()
	data = frappe.parse_json(data)

	if data.data:
		result = {}
		for each in data.data:
			if each["BiometricId"] in result:
				array = result[each["BiometricId"]]
				array.append(each["logdate"])
				result[each["BiometricId"]] = array
			else:
				result[each["BiometricId"]] = [each["logdate"]]


		for employee_id, checkins in result.items():
			login = ''
			logout = ''
			prev_checkin =''
			for each_checkin in checkins:
				if not prev_checkin:
					prev_checkin = get_datetime(each_checkin)
					login = prev_checkin
				else:
					time = time_diff(get_datetime(each_checkin), prev_checkin)
					if str(time)[0] == "-":
						time = time_diff( prev_checkin, get_datetime(each_checkin))

					if str(time)[0]!= "-" and int(str(time).split(":")[0]) >=1:
						logout = get_datetime(each_checkin)
					prev_checkin = get_datetime(each_checkin)
			
			if login != "" and logout != "" and login > logout:
				temp_login = login
				login = logout
				logout = temp_login

			name = frappe.db.get_value('Employee', {'attendance_device_id': employee_id}, ['name'])
			if name:
				if not logout:
					# Create Checkin
					doc = frappe.new_doc("Employee Checkin")
					doc.employee = name
					doc.log_type = "IN"
					doc.time = get_datetime_str(login)
					doc.insert()

				else:
					# Create Checkin
					log_in = frappe.new_doc("Employee Checkin")
					log_in.employee = name
					log_in.log_type = "IN"
					log_in.latitude = "7.366"
					log_in.longitude = "78.476"


					log_in.time = get_datetime_str(login)
			
					log_in.insert()

					# Create Checkout
					log_out = frappe.new_doc("Employee Checkin")
					log_out.employee = name
					log_out.log_type = "OUT"
					log_out.time = get_datetime_str(logout)
					log_out.latitude = "7.366"
					log_out.longitude = "78.476"


					log_out.insert()
		
		# print(json.dumps(result, indent=4), 'RESULT ,\n\n\n')
		# Update the Last Sync of Checkin
		shift_types = frappe.db.get_list("Shift Type", pluck="name")
		for each_shift in shift_types:
			frappe.db.set_value('Shift Type', each_shift, 'last_sync_of_checkin', now())
		# print("Completed \n\n\n\nn\n")
