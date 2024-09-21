import frappe
from frappe import _
from erpnext.buying.doctype.request_for_quotation.request_for_quotation import RequestforQuotation
from erpnext.buying.doctype.request_for_quotation.request_for_quotation import  *
from frappe.utils.user import get_user_fullname
STANDARD_USERS = ("Guest", "Administrator")

class CustomRequestforQuotation(RequestforQuotation):
	def send_to_supplier(self):
		"""Sends RFQ mail to involved suppliers."""
		for rfq_supplier in self.suppliers:
			if rfq_supplier.email_id is not None and rfq_supplier.send_email:
				self.validate_email_id(rfq_supplier)

				update_password_link, contact = self.update_supplier_contact(rfq_supplier, self.get_link())

				self.update_supplier_part_no(rfq_supplier.supplier)
				frappe.errprint(rfq_supplier.email_id)
				self.supplier_rfq_mail(rfq_supplier, update_password_link, self.get_link(),rfq_supplier.email_id)
				rfq_supplier.email_sent = 1
				if not rfq_supplier.contact:
					rfq_supplier.contact = contact
				rfq_supplier.save()
	def supplier_rfq_mail(self, data, update_password_link, rfq_link,,email_id=None, preview=False):
		full_name = get_user_fullname(frappe.session["user"])
		frappe.errprint([email_id,"email_id"])
		if full_name == "Guest":
			full_name = "Administrator"

		doc_args = self.as_dict()

		if data.get("contact"):
			contact = frappe.get_doc("Contact", data.get("contact"))
			doc_args["contact"] = contact.as_dict()
		if not email_id:
			frappe.throw("Email Missing")
		else:
			custom_link=_generate_temporary_login_link(email_id,rfq_link)

		doc_args.update(
			{
				"supplier": data.get("supplier"),
				"supplier_name": data.get("supplier_name"),
				"update_password_link": f'<a href="{update_password_link}" class="btn btn-default btn-xs" target="_blank">{_("Set Password")}</a>',
				"portal_link": f'<a href="{rfq_link}" class="btn btn-default btn-xs" target="_blank"> {_("Submit your Quotation")} </a>',
				"user_fullname": full_name,
				"login_link":custom_link

			}
		)

		if not self.email_template:
			return

		email_template = frappe.get_doc("Email Template", self.email_template)
		message = frappe.render_template(email_template.response_, doc_args)
		subject = frappe.render_template(email_template.subject, doc_args)
		sender = frappe.session.user not in STANDARD_USERS and frappe.session.user or None

		if preview:
			return {"message": message, "subject": subject}

		attachments = []
		if self.send_attached_files:
			attachments = self.get_attachments()

		if self.send_document_print:
			supplier_language = frappe.db.get_value("Supplier", data.supplier, "language")
			system_language = frappe.db.get_single_value("System Settings", "language")
			attachments.append(
				frappe.attach_print(
					self.doctype,
					self.name,
					doc=self,
					print_format=self.meta.default_print_format or "Standard",
					lang=supplier_language or system_language,
					letterhead=self.letter_head,
				)
			)

		self.send_email(data, sender, subject, message, attachments)


def _generate_temporary_login_link(email: str, redirect_url: str):
	from frappe.utils import get_url
	assert isinstance(email, str)
	assert isinstance(redirect_url, str)
	expiry = frappe.get_system_settings("login_with_email_link_expiry") or 10

	if not frappe.db.exists("User", email):
		frappe.throw(_("User with email address {0} does not exist").format(email), frappe.DoesNotExistError)

	key = frappe.generate_hash()
	cache_instance = frappe.cache()
	cache_instance.set_value(f"one_time_login_key:{key}", email, expires_in_sec=expiry * 60)
	return get_url(f"/api/method/frappe.www.login.login_via_key?key={key}")


