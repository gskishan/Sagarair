frappe.ui.form.on('Service Visit Register', {
    refresh: function(frm) {
        // Add a custom button to trigger the calculation
        frm.add_custom_button(__('Calculate Total Expense'), function() {
            calculateTotalExpense(frm);
        });
    }
});

function calculateTotalExpense(frm) {
    let totalExpense = 0;

    frm.doc.expense_reporting.forEach(function(row) {
        totalExpense += row.cost || 0;
    });

    frm.set_value('total_expense', totalExpense);
    frm.refresh_field('total_expense');
}
