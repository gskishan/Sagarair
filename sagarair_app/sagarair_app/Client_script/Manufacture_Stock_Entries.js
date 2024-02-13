frappe.ui.form.on('Work Order', {
    refresh: function(frm) {
        if(frm.doc.status === 'Completed') {
            frm.add_custom_button(__('Manufacture Stock Entry'), function() {
                frappe.set_route('List', 'Stock Entry', {'work_order': frm.doc.name});
            });
        }
    }
});
