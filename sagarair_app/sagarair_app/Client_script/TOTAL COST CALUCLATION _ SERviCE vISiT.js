frappe.ui.form.on('Service Visit Register', {
    refresh: function(frm) {
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
    }
});

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
