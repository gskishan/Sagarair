frappe.ui.form.on('Service Visit Register', {
    sales_order_reference: function(frm) {
        // Listen for changes in the Sales Order Reference field
        // Fetch and set data when the Sales Order Reference changes
        fetch_and_set_sales_order_data(frm);
    }
});

function fetch_and_set_sales_order_data(frm) {
    var sales_order_reference = frm.doc.sales_order_reference;
    if (sales_order_reference) {
        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Sales Order',
                name: sales_order_reference,
                filters: {
                    fields: ['items']
                }
            },
            callback: function(r) {
                if (r.message && r.message.items) {
                    var items = r.message.items;
                    var purpose_table = frm.doc.purposes || [];
                    
                    // Clear existing rows in the child table
                    purpose_table.splice(0, purpose_table.length);
                    
                    // Loop through the fetched data and add it to the 'purposes' table
                    $.each(items, function(i, item) {
                        var child_row = frappe.model.add_child(frm.doc, 'Service Visit Purpose', 'purposes');
                        child_row.item_code = item.item_code;
                        child_row.item_name = item.item_name;
                        child_row.description = item.description;
                    });

                    frm.refresh_field('purposes');
                }
            }
        });
    }
}
