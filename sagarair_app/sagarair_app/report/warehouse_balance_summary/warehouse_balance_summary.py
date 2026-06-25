import frappe
from frappe import _


def execute(filters=None):
	company = filters.get("company")
	if not company:
		frappe.throw(_("Please select a Company"))

	warehouses = get_warehouses(company)
	columns = get_columns(warehouses)
	data = get_data(filters, warehouses)
	return columns, data


def get_warehouses(company):
	return frappe.get_all(
		"Warehouse",
		filters={"company": company, "is_group": 0},
		pluck="name",
		order_by="name asc",
	)


def get_columns(warehouses):
	columns = [
		{
			"label": _(""),
			"fieldname": "label",
			"fieldtype": "Data",
			"width": 150,
		},
	]

	for idx, wh in enumerate(warehouses):
		columns.append(
			{
				"label": _(wh),
				"fieldname": "wh_{}".format(idx),
				"fieldtype": "Currency",
				"width": 160,
			}
		)

	return columns


def get_data(filters, warehouses):
	if not warehouses:
		return []

	to_date = filters.get("to_date")

	balance_data = frappe.db.sql(
		"""
		SELECT warehouse, SUM(stock_value) as balance_value
		FROM (
			SELECT item_code, warehouse, stock_value,
				ROW_NUMBER() OVER (
					PARTITION BY item_code, warehouse
					ORDER BY posting_datetime DESC, creation DESC
				) as rn
			FROM `tabStock Ledger Entry`
			WHERE posting_date <= %(to_date)s
			AND docstatus < 2
			AND is_cancelled = 0
			AND warehouse IN %(warehouses)s
		) sub
		WHERE rn = 1
		GROUP BY warehouse
		""",
		{"to_date": to_date, "warehouses": warehouses},
		as_dict=True,
	)

	warehouse_balance = {d.warehouse: d.balance_value for d in balance_data}

	row = {"label": "Total Balance Value"}
	for idx, wh in enumerate(warehouses):
		row["wh_{}".format(idx)] = warehouse_balance.get(wh, 0)

	return [row]