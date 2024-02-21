import frappe
@frappe.whitelist()
def email_set():
  if frappe.db.get_default("suspend_email_queue"):
    frappe.db.set_default("suspend_email_queue", 0)
  else:
    frappe.db.set_default("suspend_email_queue", 1)
  frappe.errprint([int(frappe.db.get_default("suspend_email_queue")),"em"])
