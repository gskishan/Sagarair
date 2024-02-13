frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        // fetch completed work orders related to the sales order
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Work Order',
                fields: ['name', 'total_incurred_cost'],
                filters: {
                    docstatus: 1,
                    status: 'Completed',
                    sales_order: frm.doc.name
                }
            },
            callback: function(response) {
                if (response.message) {
                    // calculate total cost
                    const total_cost = response.message.reduce((acc, wo) => {
                        return acc + wo.total_incurred_cost;
                    }, 0);

                    // set value of custom field
                    frm.set_value('cost_incurred', total_cost);
                }
            }
        });
    }
});
