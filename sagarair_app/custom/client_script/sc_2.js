frappe.ui.form.on("BOM", {
    total_cost: function(frm,cdt,cdn) {
        var d = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, 'total_cost_with_labour', (d.total_cost + d.labour_cost));
    }
});

