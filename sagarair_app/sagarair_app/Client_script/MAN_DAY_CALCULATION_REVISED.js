frappe.ui.form.on('Sales Order', {
    validate: function(frm) {
        // Calculate man_days based on net_total
        var netTotal = frm.doc.net_total || 0;
        var manDays = netTotal * (0.05 / 800);
        
        // Set the calculated man_days value in the custom field
        frm.set_value('man_days_calculation', manDays);

    }
});
