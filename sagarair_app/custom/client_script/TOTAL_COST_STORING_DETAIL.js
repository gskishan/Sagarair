frappe.ui.form.on('Labour Timesheet', {
    refresh: function(frm) {
        frm.add_custom_button(__('Calculate Total Cost'), function() {
            calculateTotalCost(frm);
        });
    }
});

function calculateTotalCost(frm) {
    var totalCost = 0;
    frm.doc.labour_timesheet_details.forEach(function(row) {
        totalCost += row.labour_cost;
    });
    frm.set_value('total_cost', totalCost);
    frm.save();
}
