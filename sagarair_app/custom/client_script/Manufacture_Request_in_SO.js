frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        frm.add_custom_button(__('Open MR'), function() {
            frappe.set_route('List', 'Material Request', {'sales_order': frm.doc.name, 'status': 'Manufacture'});
        });
    }
});
