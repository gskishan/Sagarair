
import frappe
from frappe import _


def on_submit(self,method=None):
	if self.work_order:
		wo=frappe.get_doc("Work Order",self.work_order)
		for d in self.items:
			for e in wo.items:
				if d.custom_work_order_item==e.name:
					e.db_set("custom_balance_qty",e.required_qty-d.qty)
def on_cancel(self,method=None):
	if self.work_order:
		wo=frappe.get_doc("Work Order",self.work_order)
		for d in self.items:
			for e in wo.items:
				if d.custom_work_order_item==e.name:
					e.db_set("custom_balance_qty",e.required_qty+d.qty)
		
# @frappe.whitelist()
# def validate(self,method):
# 	if not self.additional_costs:
# 		self.append('additional_costs',{
# 			'expense_account':"Powder Coating (Included in Valuation) - SAPL",
# 			'description':"power",
# 			'amount':1
# 		})
# 		self.append('additional_costs',{
# 			'expense_account':"Labour Cost ( Included in Valuation ) - SAPL",
# 			'description':"lab",
# 			'amount':2
# 		})

@frappe.whitelist()
def reset_all_cal(stock_entry):
	self=frappe.get_doc("Stock Entry",stock_entry)
	on_update(self)
@frappe.whitelist()
def on_update(self,method=None):
	if self.work_order and self.docstatus==1:
		labour = 0
		power = 0
		for d in self.additional_costs:
			if d.expense_account == "Powder Coating (Included in Valuation) - SAPL":
				power += d.amount
			if d.expense_account == "Labour Cost ( Included in Valuation ) - SAPL":
				labour += d.amount

		wo = frappe.get_doc("Work Order", self.work_order)
		wo.db_set("custom_labour_cost",labour, update_modified=False)
		wo.custom_labour_cost = labour
		wo.db_set("powder_coating",power, update_modified=False)
		wo.powder_coating = power
		
		wo.db_set("raw_material_consumed_cost", self.total_outgoing_value)
		wo.db_set("additional_costs", self.total_additional_costs)
		additional_costs = wo.additional_costs or 0
		raw_material_consumed_cost = wo.raw_material_consumed_cost or 0
		total_cost = additional_costs + raw_material_consumed_cost
		wo.db_set('total_incurred_cost', total_cost, update_modified=False)

		produced_qty = self.fg_completed_qty or wo.produced_qty
		total_cost_per_unit = total_cost /produced_qty
		wo.db_set('total_cost_per_unit', total_cost_per_unit, update_modified=False)
		status=agrigate_costing(wo.sales_order)
		if status:
			so=frappe.get_doc("Sales Order",wo.sales_order)
			so.db_set('raw_material_consumed_cost',self.total_outgoing_value, update_modified=False)
			so.db_set('labour_cost',wo.custom_labour_cost, update_modified=False)
			so.db_set('powder_coating', wo.powder_coating, update_modified=False)
			so.db_set('additional_costs',  self.total_additional_costs, update_modified=False)
			so.db_set('total_incurred_cost',total_cost, update_modified=False)
			so.db_set('total_cost_per_unit',total_cost_per_unit, update_modified=False)


		
		

@frappe.whitelist()
def agrigate_costing(sales_order):
	sql="""select sum(raw_material_consumed_cost) raw_material_consumed_cost,sum(total_cost_per_unit) total_cost_per_unit,sum(total_incurred_cost) total_incurred_cost,
	sum(additional_costs) additional_costs,sum(custom_labour_cost) custom_labour_cost,sum(powder_coating) powder_coating 
	from `tabWork Order` where docstatus=1 and sales_order="{0}" """.format(sales_order)
	costing=frappe.db.sql(sql,as_dict=True)
	if costing:
		so=frappe.get_doc("Sales Order",sales_order)
		so.db_set('raw_material_consumed_cost', costing[0].raw_material_consumed_cost, update_modified=False)
		so.db_set('labour_cost', costing[0].custom_labour_cost, update_modified=False)
		so.db_set('powder_coating', costing[0].powder_coating, update_modified=False)
		so.db_set('additional_costs', costing[0].additional_costs, update_modified=False)
		so.db_set('total_incurred_cost', costing[0].total_incurred_cost, update_modified=False)
		so.db_set('total_cost_per_unit', costing[0].total_cost_per_unit, update_modified=False)

		return False
	else:
		return True



	

	
	
	

		
