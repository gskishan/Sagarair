frappe.query_reports["Out of Stock Items in Work Order"] = {
  filters: [
    {
      fieldname: "work_order",
      label: "Work Order",
      fieldtype: "Link",
      options: "Work Order"
    },
    {
      fieldname: "sales_order",
      label: "Sales Order",
      fieldtype: "Link",
      options: "Sales Order"
    }
  ]
};
