frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        // Open MR Button
        frm.add_custom_button(__('Open MR'), function() {
            frappe.set_route('List', 'Material Request', {'sales_order': frm.doc.name, 'status': 'Manufacture'});
        });

        // Open WO Button
        frm.add_custom_button(__('Open WO'), function() {
            frappe.set_route('List', 'Work Order', {'sales_order': frm.doc.name});
        });

        // Open Service Visits Button
        frm.add_custom_button(__('Open Service Visits'), function() {
            frappe.set_route('List', 'Service Visit Register', {'sales_order_reference': frm.doc.name});
        });

        // Open Delivery Notes Button
        frm.add_custom_button(__('Open Delivery Notes'), function() {
            frappe.set_route('List', 'Delivery Note', {'sales_order_reference': frm.doc.name});
        });

        // Fetch and calculate completed work orders
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
                    const total_cost = response.message.reduce((acc, wo) => acc + wo.total_incurred_cost, 0);
                    frm.set_value('cost_incurred', total_cost);
                    const margin = frm.doc.total - (frm.doc.cost_incurred || 0);
                    frm.set_value('margin', margin);
                    const profit_percentage = (margin / frm.doc.total) * 100;
                    frm.set_value('profit_percentage', profit_percentage);
                }
            }
        });

        // Calculate manufacturing status
        if (frm.doc.docstatus === 1) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    "doctype": "Work Order",
                    "filters": {
                        "sales_order": frm.doc.name
                    },
                    "fields": ["progress_status"]
                },
                callback: function(response) {
                    if (response.message && response.message.length > 0) {
                        var all_ready = true;
                        for (var i = 0; i < response.message.length; i++) {
                            if (response.message[i].progress_status !== "RTD") {
                                all_ready = false;
                                break;
                            }
                        }
                        if (all_ready) {
                            frm.set_value("manufacture_status", "ALL-RTD");
                        } else {
                            frm.set_value("manufacture_status", "IN-PROG");
                        }
                    } else {
                        frm.set_value("manufacture_status", "NO-WO");
                    }
                }
            });
        }

        // Calculate man_days
        var netTotal = frm.doc.net_total || 0;
        var manDays = netTotal * (0.05 / 800);
        frm.set_value('man_days_calculation', manDays);


        // calculate margin
        const margin = frm.doc.total - (frm.doc.cost_incurred || 0);
    
        // set value of custom field
        frm.set_value('margin', margin);


        // get custom field value
        if (frm.doc.cost_incurred > 0){
            const margin = frm.doc.margin;

            // calculate and set profit percentage
            const profit_percentage = (margin / frm.doc.total) * 100;
            frm.set_value('profit_percentage', profit_percentage);
        }
    },

    // Validate function for man_days calculation
    validate: function(frm) {
        var netTotal = frm.doc.net_total || 0;
        var manDays = netTotal * (0.05 / 800);
        frm.set_value('man_days_calculation', manDays);
    },
    custom_get_costing_from_work_orders(frm) {
        if(frm.doc.custom_get_costing_from_work_orders && !frm.doc.name.startsWith("new")){
            frappe.db.get_list("Work Order", {
                filters: {
                    sales_order: frm.doc.name
                },
                fields:["raw_material_consumed_cost", "additional_costs", "total_incurred_cost"]
            }).then(r => {
                let raw_material_cost = 0
                let additional_cost = 0
                let incurred_cost = 0
                for (let i = 0; i < r.length; i++) {
                    let row = r[i]
                    raw_material_cost += row.raw_material_consumed_cost
                    additional_cost += row.additional_costs
                    incurred_cost += row.total_incurred_cost
                }
                frm.set_value("custom_raw_material_consumed_cost", raw_material_cost )
                frm.set_value("custom_total_additional_cost", additional_cost )
                frm.set_value("custom_total_incurred_cost", incurred_cost )
                frm.refresh()
            })
        }
    }
});
