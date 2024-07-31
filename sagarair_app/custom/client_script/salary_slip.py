import frappe
from frappe import _
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
            
            adding = 0
            for e in self.earnings:
                if e.salary_component in ['Basic', 'House Rent Allowance']:
                    adding += e.amount

            self.set("earnings", [])
            self.set("deductions", [])

            base = get_base_amount(self.employee)
            if base:
                rt = (adding / self.total_working_days) / 8.0

                self.hour_rate = rt
                self.base_hour_rate = flt(self.hour_rate) * flt(self.exchange_rate)
                wages_amount = self.hour_rate * self.total_working_hours
                self.add_earning_for_hourly_wages(
                    self, self._salary_structure_doc.salary_component, wages_amount
                )
            else:
                frappe.msgprint(_("Could not find base amount for employee {0}").format(self.employee))

        # Handle additional salary structure cases
        elif self.salary_structure == "Salary (Without ESI)":
            # Specific logic for "Salary (Without ESI)"
            self.handle_salary_without_esi()

        else:
            make_salary_slip(self._salary_structure_doc.name, self)

        if self.salary_slip_based_on_timesheet:
            self.hour_rate = rt

    def handle_salary_without_esi(self):
        # Custom logic for handling "Salary (Without ESI)"
        adding = 0
        for e in self.earnings:
            if e.salary_component in ['Basic + Da']:  # Assuming 'DA' is the other component
                adding += e.amount

        self.set("earnings", [])
        self.set("deductions", [])

        base = get_base_amount(self.employee)
        if base:
            rt = (adding / self.total_working_days) / 8.0

            self.hour_rate = rt
            self.base_hour_rate = flt(self.hour_rate) * flt(self.exchange_rate)
            wages_amount = self.hour_rate * self.total_working_hours
            self.add_earning_for_hourly_wages(
                self, self._salary_structure_doc.salary_component, wages_amount
            )
        else:
            frappe.msgprint(_("Could not find base amount for employee {0}").format(self.employee))

def get_base_amount(employee):
    sql = """SELECT base FROM `tabSalary Structure Assignment` WHERE employee=%s"""
    base = frappe.db.sql(sql, (employee,), as_dict=True)
    
    if base:
        return base[0].base
    else:
        frappe.msgprint(_("Issue in finding salary assignment for employee {0}").format(employee))
        return 0
