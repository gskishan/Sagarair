frappe.ui.form.on('Material Request', {
    refresh: function(frm) {
        // Fetch man_days_calculation value from Sales Order
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Sales Order',
                filters: { name: frm.doc.sales_order },
                fieldname: 'man_days_calculation'
            },
            callback: function(response) {
                if (response && response.message && response.message.man_days_calculation) {
                    // Set the value in man_days_alloted field
                    frm.set_value('man_days_alloted', response.message.man_days_calculation);
                }
            }
        });
    }
});
