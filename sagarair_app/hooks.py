app_name = "sagarair_app"
app_title = "Sagarair APP"
app_publisher = "GS Kishan"
app_description = "This is for Development Purpose"
app_email = "gskishan123@gmail.com"
app_license = "mit"

# Includes in <head>
# ------------------

scheduler_events = {
    "cron": {
        "* * * * * *": [
            "frappe.email.queue.flush"
        ]
    },
    "daily_long": [
        "sagarair_app.tasks.biometric.get_checkins"
    ],
}


# include js, css files in header of desk.html
# app_include_css = "/assets/sagarair_app/css/sagarair_app.css"
# app_include_js = "/assets/sagarair_app/js/sagarair_app.js"

# include js, css files in header of web template
# web_include_css = "/assets/sagarair_app/css/sagarair_app.css"
# web_include_js = "/assets/sagarair_app/js/sagarair_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sagarair_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"Service Visit Register": "public/js/service_register.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "BOM" : "custom/client_script/bom.js",
    "Sales Order" : "custom/client_script/sales_order.js",
    "Purchase Order" : "custom/client_script/purchase_order.js",
    "Work Order" : "custom/client_script/work_order.js",
    "Stock Entry" : "custom/client_script/stock_entry.js",
    "Material Request" : "custom/client_script/material_request.js",
    "Labour Timesheet" : "custom/client_script/labour_timesheet.js",
    #"Service Visit Register" : "custom/client_script/service_register.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "sagarair_app.utils.jinja_methods",
# 	"filters": "sagarair_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "sagarair_app.install.before_install"
# after_install = "sagarair_app.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sagarair_app.uninstall.before_uninstall"
# after_uninstall = "sagarair_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sagarair_app.utils.before_app_install"
# after_app_install = "sagarair_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sagarair_app.utils.before_app_uninstall"
# after_app_uninstall = "sagarair_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sagarair_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Salary Slip": "sagarair_app.custom.client_script.salary_slip.CustomSalarySlip",
    "Request for Quotation": "sagarair_app.custom_script.request_for_quotation.request_for_quotation.CustomRequestforQuotation",
    "Stock Entry": "sagarair_app.custom_script.stock_entry.stock_entry.CustomStockEntry",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Stock Entry":{
		"on_update":"sagarair_app.custom_script.stock_entry.stock_entry.on_update",
		# "validate":"sagarair_app.custom_script.stock_entry.stock_entry.validate",

	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sagarair_app.tasks.all"
# 	],
# 	"daily": [
# 		"sagarair_app.tasks.daily"
# 	],
# 	"hourly": [
# 		"sagarair_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sagarair_app.tasks.weekly"
# 	],
# 	"monthly": [
# 		"sagarair_app.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "sagarair_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sagarair_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sagarair_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sagarair_app.utils.before_request"]
# after_request = ["sagarair_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["sagarair_app.utils.before_job"]
# after_job = ["sagarair_app.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sagarair_app.auth.validate"
# ]

fixtures = [
    # Export specific Client Scripts
    {
        "dt": "Client Script",
        "filters": [
            ["name", "in", [
                "Proforma Invoice - Tax Rows from Template",
                "Auto Calculate Item Amounts - Proforma",
                "Auto Compute Taxes - Proforma Invoice"
            ]]
        ]
    },
    # Export a specific Report
    {
        "dt": "Report",
        "filters": [
            ["name", "=", "Out of Stock Items in Work Orders"]
        ]
    },
    # Export a specific Print Format
    {
        "dt": "Print Format",
        "filters": [
            ["name", "=", "Proforma_Invoice"]
        ]
    },
    # Export specific Doctypes
    {
        "dt": "DocType",
        "filters": [
            ["name", "in", ["Proforma Invoice", "Proforma Invoice Item"]]
        ]
    }
]

override_doctype_class = {
    "Service Visit Register": "sagarair_app.service_visit_register_override.service_visit_register.CustomServiceVisitRegister"
}

