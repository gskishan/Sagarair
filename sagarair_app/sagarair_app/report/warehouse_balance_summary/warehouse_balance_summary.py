import frappe
from frappe import _
from frappe.utils import fmt_money

COMPANIES = [
	"Sagar Air Private Limited",
	"Sagar Air Private Limited (Unit 2)",
]


def execute(filters=None):
	company_warehouses = {
		company: get_warehouses(company) for company in COMPANIES
	}

	max_count = max(
		(len(whs) for whs in company_warehouses.values()), default=0
	)

	columns = get_columns(max_count)
	data = get_data(filters, company_warehouses)
	return columns, data


def get_warehouses(company):
	return frappe.get_all(
		"Warehouse",
		filters={"company": company, "is_group": 0},
		pluck="name",
		order_by="name asc",
	)


def get_columns(max_count):
	columns = [
		{
			"label": _(""),
			"fieldname": "label",
			"fieldtype": "Data",
			"width": 180,
		},
	]

	for idx in range(max_count):
		columns.append(
			{
				"label": "",
				"fieldname": "wh_{}".format(idx),
				"fieldtype": "Data",
				"align": "right",
				"width": 160,
			}
		)

	return columns


def get_data(filters, company_warehouses):
	to_date = filters.get("to_date")

	all_warehouses = []
	for whs in company_warehouses.values():
		all_warehouses.extend(whs)

	warehouse_balance = get_warehouse_balances(to_date, all_warehouses)

	data = []

	for company, warehouses in company_warehouses.items():
		currency = frappe.get_cached_value("Company", company, "default_currency")

		# Section header
		data.append({"label": company, "bold": 1})

		if not warehouses:
			data.append({"label": _("No warehouses found")})
			data.append({})
			continue

		# Warehouse names row (acts as column headers for this section)
		wh_row = {"label": _("Warehouse"), "bold": 1}
		for idx, wh in enumerate(warehouses):
			wh_row["wh_{}".format(idx)] = wh
		data.append(wh_row)

		# Balance row
		balance_row = {"label": _("Total Balance Value")}
		for idx, wh in enumerate(warehouses):
			balance_row["wh_{}".format(idx)] = fmt_money(
				warehouse_balance.get(wh, 0), currency=currency
			)
		data.append(balance_row)

		# Spacer between sections
		data.append({})

	return data


def get_warehouse_balances(to_date, warehouses):
	if not warehouses:
		return {}

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

	return {d.warehouse: d.balance_value for d in balance_data}