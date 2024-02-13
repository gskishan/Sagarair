frappe.ui.form.on('Service Visit Register', {
    refresh: function(frm) {
        frm.add_custom_button(__('Calculate To Pay'), function() {
            // Get the 'advancetaken' and 'total_expense' values
            var advancetaken = frm.doc.advancetaken || 0;
            var totalExpense = frm.doc.total_expense || 0;

            // Calculate 'to_pay' by subtracting 'advancetaken' from 'total_expense'
            var toPay = totalExpense - advancetaken;

            // Update the 'to_pay' field
            frm.set_value('to_pay', toPay);
        });
    }
});
