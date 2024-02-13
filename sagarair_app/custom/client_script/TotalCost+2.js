frappe.ui.form.on('Labour Timesheet', {
    refresh: function(frm) {
        frm.fields_dict['labour_timesheet_detail'].grid.get_field('total_hrs').get_query = function(doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            var total_hrs = child.hours + (1.5 * child.ot_hrs);
            frappe.model.set_value(child.doctype, child.name, 'total_hrs', total_hrs);
            calculateLabourCost(child);
            refreshTotalCost(frm);
        };
    }
});

frappe.ui.form.on('Labour Timesheet Detail', {
    hours: function(frm, cdt, cdn) {
        calculateTotalHrs(frm, cdt, cdn);
    },
    ot_hrs: function(frm, cdt, cdn) {
        calculateTotalHrs(frm, cdt, cdn);
    },
    employee: function(frm, cdt, cdn) {
        calculateTotalHrs(frm, cdt, cdn);
    },
    labour_cost: function(frm, cdt, cdn) {
        calculateTotalCost(frm);
    }
});

function calculateTotalHrs(frm, cdt, cdn) {
    var child = locals[cdt][cdn];
    var total_hrs = child.hours + (1.5 * child.ot_hrs);
    frappe.model.set_value(cdt, cdn, 'total_hrs', total_hrs);
    calculateLabourCost(child);
    refreshTotalCost(frm);
}

function calculateLabourCost(child) {
    frappe.call({
        method: 'frappe.client.get_value',
        args: {
            doctype: 'Employee',
            filters: { name: child.employee },
            fieldname: ['salary_per_month_']
        },
        callback: function(response) {
            if (response && response.message && response.message.salary_per_month_) {
                var labour_cost = response.message.salary_per_month_ * child.total_hrs / 208;
                frappe.model.set_value(child.doctype, child.name, 'labour_cost', labour_cost);
            }
        }
    });
}

//function refreshTotalCost(frm) {
   // var total_cost = 0;
  //  frm.doc.labour_timesheet_detail.forEach(function(child) {
  //      total_cost += child.labour_cost;
  //  });
  //  frm.set_value('total_cost', total_cost);
// }
