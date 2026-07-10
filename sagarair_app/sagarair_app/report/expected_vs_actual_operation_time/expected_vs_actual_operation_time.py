import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "work_order",
			"label": "Work Order",
			"fieldtype": "Link",
			"options": "Work Order",
			"width": 160,
		},
		{
			"fieldname": "operation",
			"label": "Operation",
			"fieldtype": "Link",
			"options": "Operation",
			"width": 200,
		},
		{
			"fieldname": "job_card_status",
			"label": "Status",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"fieldname": "employee_name",
			"label": "Employee Name",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"fieldname": "estimated_time",
			"label": "Estimated Time (Mins)",
			"fieldtype": "Float",
			"width": 180,
		},
		{
			"fieldname": "actual_time",
			"label": "Actual Time (Mins)",
			"fieldtype": "Float",
			"width": 180,
		},
		{
			"fieldname": "difference",
			"label": "Difference (Mins)",
			"fieldtype": "Float",
			"width": 180,
		},
	]


def get_data(filters):
	# docstatus < 2 => include Draft (Open, Work In Progress etc.)
	# and Submitted (Completed) job cards, exclude Cancelled
	jc_conditions = ["jc.docstatus < 2"]
	values = {}

	if filters.get("work_order"):
		jc_conditions.append("jc.work_order = %(work_order)s")
		values["work_order"] = filters["work_order"]

	if filters.get("sales_order"):
		jc_conditions.append("wo.sales_order = %(sales_order)s")
		values["sales_order"] = filters["sales_order"]

	if filters.get("bom"):
		jc_conditions.append("wo.bom_no = %(bom)s")
		values["bom"] = filters["bom"]

	if filters.get("start_date"):
		jc_conditions.append("jc.posting_date >= %(start_date)s")
		values["start_date"] = filters["start_date"]

	if filters.get("end_date"):
		jc_conditions.append("jc.posting_date <= %(end_date)s")
		values["end_date"] = filters["end_date"]

	if filters.get("employee"):
		jc_conditions.append(
			"""jc.name IN (
				SELECT parent FROM `tabJob Card Time Log`
				WHERE employee = %(employee)s
			)"""
		)
		values["employee"] = filters["employee"]

	jc_where = " AND ".join(jc_conditions)

	# Get unique work orders from filtered job cards
	work_orders = frappe.db.sql(
		"""
		SELECT DISTINCT jc.work_order
		FROM `tabJob Card` jc
		LEFT JOIN `tabWork Order` wo ON jc.work_order = wo.name
		WHERE {jc_where}
	""".format(
			jc_where=jc_where
		),
		values,
		as_list=True,
	)

	work_order_list = [wo[0] for wo in work_orders if wo[0]]

	if not work_order_list:
		return []

	# Estimated time from Work Order Operations child table,
	# per (work_order, operation)
	estimated_data = frappe.db.sql(
		"""
		SELECT parent as work_order, operation,
			SUM(time_in_mins) as estimated_time
		FROM `tabWork Order Operation`
		WHERE parent IN %(work_orders)s
		GROUP BY parent, operation
	""",
		{"work_orders": work_order_list},
		as_dict=True,
	)

	estimated_map = {
		(d.work_order, d.operation): d.estimated_time for d in estimated_data
	}

	# Actual time from Job Card Time Log child table,
	# per (work_order, operation).
	# Only sum unique time_in_mins values per job card to avoid duplicates
	actual_data = frappe.db.sql(
		"""
		SELECT work_order, operation, SUM(unique_time) as actual_time
		FROM (
			SELECT jc.work_order, jc.operation, jc.name as job_card,
				jctl.time_in_mins as unique_time
			FROM `tabJob Card Time Log` jctl
			INNER JOIN `tabJob Card` jc ON jctl.parent = jc.name
			LEFT JOIN `tabWork Order` wo ON jc.work_order = wo.name
			WHERE {jc_where}
			GROUP BY jc.work_order, jc.operation, jc.name, jctl.time_in_mins
		) sub
		GROUP BY work_order, operation
	""".format(
			jc_where=jc_where
		),
		values,
		as_dict=True,
	)

	actual_map = {
		(d.work_order, d.operation): d.actual_time for d in actual_data
	}

	# Job Card status(es) per (work_order, operation)
	status_data = frappe.db.sql(
		"""
		SELECT jc.work_order, jc.operation,
			GROUP_CONCAT(DISTINCT jc.status ORDER BY jc.status SEPARATOR ', ') as status
		FROM `tabJob Card` jc
		LEFT JOIN `tabWork Order` wo ON jc.work_order = wo.name
		WHERE {jc_where}
		GROUP BY jc.work_order, jc.operation
	""".format(
			jc_where=jc_where
		),
		values,
		as_dict=True,
	)

	status_map = {(d.work_order, d.operation): d.status for d in status_data}

	# Unique employees from time logs per (work_order, operation)
	employee_condition = ""
	if filters.get("employee"):
		employee_condition = "AND jctl.employee = %(employee)s"

	employee_data = frappe.db.sql(
		"""
		SELECT DISTINCT jc.work_order, jc.operation, jctl.employee
		FROM `tabJob Card Time Log` jctl
		INNER JOIN `tabJob Card` jc ON jctl.parent = jc.name
		LEFT JOIN `tabWork Order` wo ON jc.work_order = wo.name
		WHERE {jc_where}
		AND jctl.employee IS NOT NULL AND jctl.employee != ''
		{employee_condition}
	""".format(
			jc_where=jc_where, employee_condition=employee_condition
		),
		values,
		as_dict=True,
	)

	employee_map = {}
	all_employee_ids = set()
	for d in employee_data:
		key = (d.work_order, d.operation)
		employee_map.setdefault(key, []).append(d.employee)
		all_employee_ids.add(d.employee)

	# Employee names in one query
	employee_names = {}
	if all_employee_ids:
		employee_names = dict(
			frappe.get_all(
				"Employee",
				filters={"name": ["in", list(all_employee_ids)]},
				fields=["name", "employee_name"],
				as_list=True,
			)
		)

	# Combine all (work_order, operation) keys from all sources
	all_keys = (
		set(estimated_map.keys())
		| set(actual_map.keys())
		| set(status_map.keys())
	)

	data = []
	for key in sorted(all_keys, key=lambda k: (k[0] or "", k[1] or "")):
		work_order, operation = key
		est = estimated_map.get(key, 0) or 0
		act = actual_map.get(key, 0) or 0
		status = status_map.get(key, "")

		employees = sorted(employee_map.get(key, []))

		if filters.get("employee"):
			# Only show rows for the selected employee
			if not employees:
				continue
		else:
			# No employee filter: still show operations without time logs
			employees = employees or [None]

		for emp in employees:
			data.append(
				{
					"work_order": work_order,
					"operation": operation,
					"job_card_status": status,
					# employee kept in row data (not a column) so the
					# JS formatter can build the link
					"employee": emp,
					"employee_name": employee_names.get(emp, ""),
					"estimated_time": est,
					"actual_time": act,
					"difference": est - act,
				}
			)

	return data