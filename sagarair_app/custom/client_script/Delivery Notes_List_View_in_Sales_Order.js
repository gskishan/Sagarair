frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        frm.add_custom_button(__('Open Delivery Notes'), function() {
            frappe.set_route('List', 'Delivery Note', {'sales_order_reference': frm.doc.name});
        });
    }
});
