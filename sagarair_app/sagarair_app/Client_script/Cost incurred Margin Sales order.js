frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        // calculate margin
        const margin = frm.doc.total - (frm.doc.cost_incurred || 0);
        
        // set value of custom field
        frm.set_value('margin', margin);
    }
});
