import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "operation",
			"label": "Operation",
			"fieldtype": "Link",
			"options": "Operation",
			"width": 250,
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
	jc_conditions = ["jc.docstatus = 1"]
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

	# Estimated time from Work Order Operations child table
	estimated_data = frappe.db.sql(
		"""
		SELECT operation, SUM(time_in_mins) as estimated_time
		FROM `tabWork Order Operation`
		WHERE parent IN %(work_orders)s
		GROUP BY operation
	""",
		{"work_orders": work_order_list},
		as_dict=True,
	)

	estimated_map = {d.operation: d.estimated_time for d in estimated_data}

	# Actual time from Job Card Time Log child table
	# Only sum unique time_in_mins values per job card to avoid duplicates
	actual_data = frappe.db.sql(
		"""
		SELECT operation, SUM(unique_time) as actual_time
		FROM (
			SELECT jc.operation, jc.name as job_card, jctl.time_in_mins as unique_time
			FROM `tabJob Card Time Log` jctl
			INNER JOIN `tabJob Card` jc ON jctl.parent = jc.name
			LEFT JOIN `tabWork Order` wo ON jc.work_order = wo.name
			WHERE {jc_where}
			GROUP BY jc.operation, jc.name, jctl.time_in_mins
		) sub
		GROUP BY operation
	""".format(
			jc_where=jc_where
		),
		values,
		as_dict=True,
	)

	actual_map = {d.operation: d.actual_time for d in actual_data}

	# Combine all operations from both sources
	all_operations = set(list(estimated_map.keys()) + list(actual_map.keys()))

	data = []
	for op in sorted(all_operations):
		est = estimated_map.get(op, 0) or 0
		act = actual_map.get(op, 0) or 0
		data.append(
			{
				"operation": op,
				"estimated_time": est,
				"actual_time": act,
				"difference": est - act,
			}
		)

	return data