console.log("Service_Register")
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
        console.log("Pay")

         // Add a custom button to trigger the calculation
         frm.add_custom_button(__('Calculate Total Expense'), function() {
            calculateTotalExpense(frm);
        });
        console.log("Total")

        frm.fields_dict['service_visit_manday_reporting'].grid.get_field('technician_cost').get_query = function(doc, cdt, cdn) {
            var row = locals[cdt][cdn];
            return {
                filters: {
                    'monthly_wages': row.monthly_wages,
                    'number_of_days_worked': row.number_of_days_worked,
                    'extra_days_absent': row.extra_days_absent,
                }
            };
        };
        console.log("reporting")

        // Add a custom button to trigger the calculation
        frm.add_custom_button(__('Calculate Total Service Cost'), function() {
            calculateTotalServiceCost(frm);
        });
        console.log("Service")

        // Add a custom button to trigger the calculation
        frm.add_custom_button(__('Calculate Total Technician Cost'), function() {
            calculateTotalTechnicianCost(frm);
        });
        console.log("Tech")

    },
    sales_order_reference: function(frm) {
        // Listen for changes in the Sales Order Reference field
        // Fetch and set data when the Sales Order Reference changes
        fetch_and_set_sales_order_data(frm);
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

function calculateTotalTechnicianCost(frm) {
    let totalTechnicianCost = 0;

    if (frm.doc.service_visit_manday_reporting){

        frm.doc.service_visit_manday_reporting.forEach(function(row) {
            totalTechnicianCost += row.technician_cost || 0;
        });
    }

    frm.set_value('total_technician_cost', totalTechnicianCost);
    frm.refresh_field('total_technician_cost');
}



frappe.ui.form.on('Service Visit Manday Reporting', {
    monthly_wages: function(frm, cdt, cdn) {
        calculateTechnicianCost(frm, cdt, cdn);
    },
    number_of_days_worked: function(frm, cdt, cdn) {
        calculateTechnicianCost(frm, cdt, cdn);
    },
    extra_days_absent: function(frm, cdt, cdn) {
        calculateTechnicianCost(frm, cdt, cdn);
    }
});

function calculateTechnicianCost(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    if (row.monthly_wages && row.number_of_days_worked && row.extra_days_absent) {
        var mw = row.monthly_wages;
        var nd = row.number_of_days_worked;
        var ex = row.extra_days_absent;
        var technician_cost = (mw / 26) * nd * 1.5 + ex * (mw / 26);
        frappe.model.set_value(cdt, cdn, 'technician_cost', technician_cost);
    } else {
        frappe.model.set_value(cdt, cdn, 'technician_cost', 0);
    }
}
