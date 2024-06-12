// Copyright (c) 2024, GS Kishan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer  Feedback', {
	refresh: function(frm) {
	if (cur_frm.doc.sales_order && cur_frm.is_new()) {
    frappe.db.get_doc('Sales Order', cur_frm.doc.sales_order)
        .then(doc => {

            doc.items.forEach(function (item) {
                var feedback_item = cur_frm.add_child("items");
                feedback_item.item_code = item.item_code;
                feedback_item.item_name = item.item_name;
                feedback_item.qty = item.qty;
                feedback_item.rate = item.rate;
                feedback_item.description = item.description;
                feedback_item.uom = item.uom;
                 feedback_item.amount = item.amount;
                feedback_item.delivery_date = item.delivery_date;


            });
            cur_frm.refresh_fields()

        })

	}
	}
});
