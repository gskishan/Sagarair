import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)

    return columns, data

def get_columns():
    return [
        {"label": "Work Order", "fieldname": "work_order", "fieldtype": "Link", "options": "Work Order", "width": 140},
        {"label": "Sales Order", "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 140},
        {"label": "Stock Entry", "fieldname": "stock_entry", "fieldtype": "Link", "options": "Stock Entry", "width": 140},
        {"label": "Item", "fieldname": "item", "fieldtype": "Link", "options": "Item", "width": 120},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 100},
        {"label": "Required Qty", "fieldname": "required_qty", "fieldtype": "Float", "width": 120}
    ]

def get_data(filters):
    conditions = ""

    if filters.get("work_order"):
        conditions += " AND wo.name = %(work_order)s"
    if filters.get("sales_order"):
        conditions += " AND wo.sales_order = %(sales_order)s"

    query = f"""
        SELECT
            wo.name AS work_order,
            wo.sales_order AS sales_order,
            se.name AS stock_entry,
            sei.item_code AS item,
            item.item_name AS item_name,
            sei.qty AS qty,
            sei.qty AS required_qty
        FROM
            `tabWork Order` wo
        JOIN
            `tabStock Entry` se ON se.work_order = wo.name
        JOIN
            `tabStock Entry Detail` sei ON sei.parent = se.name
        JOIN
            `tabItem` item ON item.item_code = sei.item_code
        LEFT JOIN
            `tabBin` bin ON bin.item_code = sei.item_code AND bin.warehouse = sei.s_warehouse
        WHERE
            sei.qty > IFNULL(bin.actual_qty, 0)
            {conditions}
    """

    return frappe.db.sql(query, filters, as_dict=True)
