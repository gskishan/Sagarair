# Copyright (c) 2024, GS Kishan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.user import get_user_fullname
from frappe.core.doctype.communication.email import make

from frappe import _
STANDARD_USERS = ("Guest", "Administrator")
class CustomerFeedback(Document):
	@frappe.whitelist()
	def validate(self):
	    if self.is_new():
		self.email_sent=0
	        parameters = ["Product", "Size", "Finish", "Packing"]
	        for parameter in parameters:
	            child_row = self.append('parameter', {})
	            child_row.parameter = parameter
	
	@frappe.whitelist()
	def send_to_customer(self):
		update_password_link = self.update_customer_contact(self.get_link())
		
		self.customer_rfq_mail( update_password_link, self.get_link())




	def update_customer_contact(self, link):
	

		update_password_link=""
		if frappe.db.exists("User", self.email_id):
			user = frappe.get_doc("User", self.email_id)
			update_password_link = user.reset_password()
		else:
			user, update_password_link = self.create_user(self.get_link())
		return update_password_link



		

	

	def create_user(self, link):


		user = frappe.get_doc(
			{
				"doctype": "User",
				"send_welcome_email": 0,
				"email": self.email_id,
				"first_name": self.customer_name or self.customer,
				"user_type": "Website User",
				"redirect_url": link,
			}
		)
		user.save(ignore_permissions=True)
		update_password_link = user.reset_password()

		return user, update_password_link

	def customer_rfq_mail(self, update_password_link, rfq_link, preview=False):
		full_name = get_user_fullname(frappe.session["user"])
		if full_name == "Guest":
			full_name = "Administrator"

		doc_args = self.as_dict()


		doc_args.update(
			{
				"customer": self.get("customer"),
				"customer_name": self.get("customer_name"),
				"update_password_link": f'<a href="{update_password_link}" class="btn btn-default btn-xs" target="_blank">{_("Set Password")}</a>',
				"portal_link": f'<a href="{rfq_link}" class="btn btn-default btn-xs" target="_blank"> {_("Submit your FeedBack")} </a>',
				"user_fullname": full_name,
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
		# if self.send_attached_files:
		# 	attachments = self.get_attachments()

		# if self.send_document_print:
		# 	customer_language = frappe.db.get_value("customer", data.customer, "language")
		# 	system_language = frappe.db.get_single_value("System Settings", "language")
		# 	attachments.append(
		# 		frappe.attach_print(
		# 			self.doctype,
		# 			self.name,
		# 			doc=self,
		# 			print_format=self.meta.default_print_format or "Standard",
		# 			lang=customer_language or system_language,
		# 			letterhead=self.letter_head,
		# 		)
		# 	)

		self.send_email(sender, subject, message, attachments)

	def send_email(self, sender, subject, message, attachments):


		make(
			subject=subject,
			content=message,
			recipients=self.email_id,
			sender=sender,
			attachments=attachments,
			send_email=True,
			doctype=self.doctype,
			name=self.name,
		)["name"]
		self.db_set('email_sent',1, update_modified=False)
		frappe.msgprint(_("Email Sent to Customer {0}").format(self.customer))

	def get_attachments(self):
		return [d.name for d in get_attachments(self.doctype, self.name)]
	
	def get_link(self):
		url="https://sagarair.gtksoft.in/customer-feedback/{0}/edit".format(self.name)
		return url

	


