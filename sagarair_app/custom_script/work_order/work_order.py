from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder


class CustomWorkOrder(WorkOrder):
	# skip the coverage recompute, keep the qty claimed on the stock entries
	def recompute_material_transferred_for_manufacturing(self, transferred_items):
		return
