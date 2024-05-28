import frappe
from frappe import _
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
from frappe.utils import flt
from hrms.hr.utils import validate_active_employee

class CustomSalarySlip(SalarySlip):

    @frappe.whitelist()
    def pull_sal_struct(self):
        rt = 0
        try:
            if self.salary_slip_based_on_timesheet:
                self.salary_structure = self._salary_structure_doc.name
                self.total_working_hours = sum([d.working_hours or 0.0 for d in self.timesheets]) or 0.0
                make_salary_slip(self._salary_structure_doc.name, self)
                
                adding = 0
                for e in self.earnings:
                    if e.salary_component == 'Basic' or e.salary_component == 'House Rent Allowance':
                        adding += e.amount
                
                self.set("earnings", [])
                self.set("deductions", [])
                
                base = get_base_amount(self.employee)
                if base is None:
                    frappe.throw(_("Base amount for employee {0} not found").format(self.employee))
                
                rt = ((adding / self.total_working_days) / 8.0)
                self.hour_rate = rt
                self.base_hour_rate = flt(self.hour_rate) * flt(self.exchange_rate)
                wages_amount = self.hour_rate * self.total_working_hours
                self.add_earning_for_hourly_wages(self._salary_structure_doc.salary_component, wages_amount)

            make_salary_slip(self._salary_structure_doc.name, self)
            if self.salary_slip_based_on_timesheet:
                self.hour_rate = rt
            frappe.msgprint(_("Salary structure pulled successfully"))
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), _("Error in CustomSalarySlip.pull_sal_struct"))
            frappe.throw(_("An error occurred while pulling the salary structure: {0}").format(str(e)))

def get_base_amount(employee):
    try:
        base = frappe.db.get_value("Salary Structure Assignment", {"employee": employee}, "base")
        if base:
            return base
        else:
            frappe.msgprint(_("No salary structure assignment found for employee {0}").format(employee))
            return None
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error in get_base_amount"))
        frappe.msgprint(_("An error occurred while fetching the base amount for employee {0}: {1}").format(employee, str(e)))
        return None
