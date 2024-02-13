frappe.ui.form.on('Purchase Order', {
    refresh: function(frm) {
        frm.add_custom_button(__('Open PR'), function() {
            frappe.set_route('List', 'Purchase Receipt', {'purchase_order': frm.doc.name});
        });
    }
});
