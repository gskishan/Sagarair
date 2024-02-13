frappe.ui.form.on('Service Visit Register', {
    refresh: function(frm) {
        // Add a custom button to trigger the calculation
        frm.add_custom_button(__('Calculate Total Service Cost'), function() {
            calculateTotalServiceCost(frm);
        });
    }
});

function calculateTotalServiceCost(frm) {
    // Get the values of the custom fields
    var totalTechnicianCost = frm.doc.total_technician_cost || 0;
    var totalExpense = frm.doc.total_expense || 0;

    // Calculate the total service cost
    var totalServiceCost = totalTechnicianCost + totalExpense;

    // Update the 'total_service_cost' field with the calculated total
    frm.set_value('total_service_cost', totalServiceCost);
    frm.refresh_field('total_service_cost');
}
