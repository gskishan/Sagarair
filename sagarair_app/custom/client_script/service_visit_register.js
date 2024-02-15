frappe.ui.form.on('Service Visit Register', {
    refresh: function(frm) {
        // Add a custom button to trigger the calculation of total expense
        frm.add_custom_button(__('Calculate Total Expense'), function() {
            calculateTotalExpense(frm);
        });
        // Add a custom button to trigger the calculation of total technician cost
        frm.add_custom_button(__('Calculate Total Technician Cost'), function() {
            calculateTotalTechnicianCost(frm);
        });
    },
});