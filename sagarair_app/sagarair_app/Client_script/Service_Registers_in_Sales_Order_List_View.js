frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        frm.add_custom_button(__('Open Service Visits'), function() {
            frappe.set_route('List', 'Service Visit Register', {'sales_order_reference': frm.doc.name});
        });
    }
});
