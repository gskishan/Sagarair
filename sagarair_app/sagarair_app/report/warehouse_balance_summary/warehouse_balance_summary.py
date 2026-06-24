import frappe
from frappe import _


WAREHOUSES = [
	"Goods In Transit - SAPL(2)",
	"Finished Goods - SAPL(2)",
	"Work In Progress - SAPL(2)",
	"Stores - SAPL(2)",
	"All Warehouses - SAPL(2)",
	"USABLE SCRAP - SAPL",
	"PRODUCTION - SAPL",
	"Fabrication - SAPL",
	"Goods In Transit - SAPL",
	"Finished Goods - SAPL",
	"Work In Progress - SAPL",
	"Stores - SAPL",
	"All Warehouses - SAPL",
]


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	columns = [
		{
			"label": _(""),
			"fieldname": "label",
			"fieldtype": "Data",
			"width": 150,
		},
	]

	for idx, wh in enumerate(WAREHOUSES):
		columns.append(
			{
				"label": _(wh),
				"fieldname": "wh_{}".format(idx),
				"fieldtype": "Currency",
				"width": 160,
			}
		)

	return columns


def get_data(filters):
	to_date = filters.get("to_date")

	# Get balance value per warehouse as of to_date
	# For each item-warehouse combo, take the latest SLE and sum stock_value
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
		) sub
		WHERE rn = 1
		GROUP BY warehouse
	""",
		{"to_date": to_date},
		as_dict=True,
	)

	warehouse_balance = {d.warehouse: d.balance_value for d in balance_data}

	# Build single row with each warehouse as a column
	row = {"label": "Total Balance Value"}
	for idx, wh in enumerate(WAREHOUSES):
		row["wh_{}".format(idx)] = warehouse_balance.get(wh, 0)

	return [row]