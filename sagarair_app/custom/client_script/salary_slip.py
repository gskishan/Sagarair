import frappe
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
from frappe.utils import flt
from hrms.hr.utils import validate_active_employee

class CustomSalarySlip(SalarySlip):

    @frappe.whitelist()
    def pull_sal_struct(self):
        from hrms.payroll.doctype.salary_structure.salary_structure import make_salary_slip
        rt = 0
        if self.salary_slip_based_on_timesheet:
            self.salary_structure = self._salary_structure_doc.name
            self.total_working_hours = sum([d.working_hours or 0.0 for d in self.timesheets]) or 0.0
            make_salary_slip(self._salary_structure_doc.name, self)

            # Calculate the sum of Basic and House Rent Allowance
            adding = 0
            for e in self.earnings:
                if e.salary_component in ['Basic', 'House Rent Allowance']:
                    adding += e.amount
                    print(adding)
            
            # Reset earnings and deductions
            self.set("earnings", [])
            self.set("deductions", [])
            base = get_base_amount(self.employee)
            rt = ((adding / self.total_working_days) / 8.0)
            self.hour_rate = rt
            self.base_hour_rate = flt(self.hour_rate) * flt(self.exchange_rate)
            wages_amount = self.hour_rate * self.total_working_hours
            self.add_earning_for_hourly_wages(
                self, self._salary_structure_doc.salary_component, wages_amount
            )

        make_salary_slip(self._salary_structure_doc.name, self)
        if self.salary_slip_based_on_timesheet:
            self.hour_rate = rt

def get_base_amount(employee):
    base = frappe.db.get_value('Salary Structure Assignment', {'employee': employee}, 'base')
    if base:
        return base
    else:
        frappe.msgprint(_("Issue in finding salary assignment"))
        return 0
