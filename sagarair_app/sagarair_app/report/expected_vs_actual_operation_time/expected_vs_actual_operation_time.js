// Copyright (c) 2026, GS Kishan and contributors
// For license information, please see license.txt
frappe.query_reports["Expected vs Actual Operation time"] = {
	filters: [
		{
			fieldname: "sales_order",
			label: __("Sales Order"),
			fieldtype: "Link",
			options: "Sales Order",
		},
		{
			fieldname: "bom",
			label: __("BOM"),
			fieldtype: "Link",
			options: "BOM",
		},
		{
			fieldname: "work_order",
			label: __("Work Order"),
			fieldtype: "Link",
			options: "Work Order",
			get_query: function () {
				var filters = {};
				var so = frappe.query_report.get_filter_value("sales_order");
				var bom = frappe.query_report.get_filter_value("bom");
				if (so) filters["sales_order"] = so;
				if (bom) filters["bom_no"] = bom;
				return { filters: filters };
			},
		},
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
		},
		{
			fieldname: "start_date",
			label: __("Start Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "end_date",
			label: __("End Date"),
			fieldtype: "Date",
		},
	],

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (
			column.fieldname === "employee_name" &&
			data &&
			data.employee &&
			value
		) {
			value =
				'<a href="/app/employee/' +
				encodeURIComponent(data.employee) +
				'">' +
				value +
				"</a>";
		}
		return value;
	},
};