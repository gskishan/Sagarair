
import frappe
from frappe import _


from erpnext.stock.doctype.stock_entry.stock_entry import  StockEntry
from erpnext.stock.doctype.stock_entry.stock_entry import *
from erpnext.manufacturing.doctype.bom.bom import (
	add_additional_cost,
	
)
from frappe.utils import (
	cint,
	
)

class CustomStockEntry(StockEntry):
	@frappe.whitelist()
	def get_items(self):
		self.set("items", [])
		self.validate_work_order()

		if self.purpose == "Disassemble":
			return self.get_items_for_disassembly()

		if not self.posting_date or not self.posting_time:
			frappe.throw(_("Posting date and posting time is mandatory"))

		self.set_work_order_details()
		self.flags.backflush_based_on = frappe.db.get_single_value(
			"Manufacturing Settings", "backflush_raw_materials_based_on"
		)

		if self.bom_no:
			backflush_based_on = frappe.db.get_single_value(
				"Manufacturing Settings", "backflush_raw_materials_based_on"
			)
			frappe.errprint("!1")
			frappe.errprint([self.pro_doc.skip_transfer,self.flags.backflush_based_on, frappe.db.get_single_value("Manufacturing Settings", "material_consumption"),"ll"])
			if self.purpose in [
				"Material Issue",
				"Material Transfer",
				"Manufacture",
				"Repack",
				"Send to Subcontractor",
				"Material Transfer for Manufacture",
				"Material Consumption for Manufacture",
			]:
				if self.work_order and self.purpose == "Material Transfer for Manufacture":
					item_dict = self.get_pending_raw_materials(backflush_based_on)
					if self.to_warehouse and self.pro_doc:
						for item in item_dict.values():
							item["to_warehouse"] = self.pro_doc.wip_warehouse
					self.add_to_stock_entry_detail(item_dict)
					frappe.errprint("2")

				elif (
					self.work_order
					and (
						self.purpose == "Manufacture"
						or self.purpose == "Material Consumption for Manufacture"
					)
					and not self.pro_doc.skip_transfer
					and self.flags.backflush_based_on == "Material Transferred for Manufacture"
				):
					frappe.errprint("3")
					
					self.add_transfered_raw_materials_in_items()

				elif (
					self.work_order
					and (
						self.purpose == "Manufacture"
						or self.purpose == "Material Consumption for Manufacture"
					)
					and self.flags.backflush_based_on == "BOM"
					and frappe.db.get_single_value("Manufacturing Settings", "material_consumption") == 1
				):
					frappe.errprint("4")
					
					self.get_unconsumed_raw_materials()

				else:
					frappe.errprint("5")

					if not self.fg_completed_qty:
						frappe.throw(_("Manufacturing Quantity is mandatory"))

					item_dict = self.get_bom_raw_materials(self.fg_completed_qty)

					# Get Subcontract Order Supplied Items Details
					if (
						self.get(self.subcontract_data.order_field)
						and self.purpose == "Send to Subcontractor"
					):
						# Get Subcontract Order Supplied Items Details
						parent = frappe.qb.DocType(self.subcontract_data.order_doctype)
						child = frappe.qb.DocType(self.subcontract_data.order_supplied_items_field)

						item_wh = (
							frappe.qb.from_(parent)
							.inner_join(child)
							.on(parent.name == child.parent)
							.select(child.rm_item_code, child.reserve_warehouse)
							.where(parent.name == self.get(self.subcontract_data.order_field))
						).run(as_list=True)

						item_wh = frappe._dict(item_wh)

					for item in item_dict.values():
						if self.pro_doc and cint(self.pro_doc.from_wip_warehouse):
							item["from_warehouse"] = self.pro_doc.wip_warehouse
						# Get Reserve Warehouse from Subcontract Order
						if (
							self.get(self.subcontract_data.order_field)
							and self.purpose == "Send to Subcontractor"
						):
							item["from_warehouse"] = item_wh.get(item.item_code)
						item["to_warehouse"] = (
							self.to_warehouse if self.purpose == "Send to Subcontractor" else ""
						)

					self.add_to_stock_entry_detail(item_dict)

			# fetch the serial_no of the first stock entry for the second stock entry
			if self.work_order and self.purpose == "Manufacture":
				work_order = frappe.get_doc("Work Order", self.work_order)
				add_additional_cost(self, work_order)

			# add finished goods item
			if self.purpose in ("Manufacture", "Repack"):
				self.set_process_loss_qty()
				self.load_items_from_bom()

		self.set_scrap_items()
		self.set_actual_qty()
		self.validate_customer_provided_item()
		self.calculate_rate_and_amount(raise_error_if_no_rate=False)

	

# def on_submit(self,method=None):
# 	if self.work_order and self.stock_entry_type=="Material Consumption for Manufacture":
# 		wo=frappe.get_doc("Work Order",self.work_order)
# 		for d in self.items:
# 			for e in wo.items:
# 				if d.custom_work_order_item==e.name:
# 					e.db_set("custom_balance_qty",e.required_qty-d.qty)
# def on_cancel(self,method=None):
# 	if self.work_order  and self.stock_entry_type=="Material Consumption for Manufacture":
# 		wo=frappe.get_doc("Work Order",self.work_order)
# 		for d in self.items:
# 			for e in wo.items:
# 				if d.custom_work_order_item==e.name:
# 					e.db_set("custom_balance_qty",e.required_qty+d.qty)
		
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



	

	
	
	

		
