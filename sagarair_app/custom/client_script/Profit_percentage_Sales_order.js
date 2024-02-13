frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        // get custom field value
        
        if (frm.doc.cost_incurred > 0){
        const margin = frm.doc.margin;

        // calculate and set profit percentage
        const profit_percentage = (margin / frm.doc.total) * 100;
        frm.set_value('profit_percentage', profit_percentage);
    }}
});
