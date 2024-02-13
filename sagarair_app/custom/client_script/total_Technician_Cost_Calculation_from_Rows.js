frappe.ui.form.on('Service Visit Register', {
    refresh: function(frm) {
        // Add a custom button to trigger the calculation
        frm.add_custom_button(__('Calculate Total Technician Cost'), function() {
            calculateTotalTechnicianCost(frm);
        });
    }
});

function calculateTotalTechnicianCost(frm) {
    let totalTechnicianCost = 0;

    frm.doc.service_visit_manday_reporting.forEach(function(row) {
        totalTechnicianCost += row.technician_cost || 0;
    });

    frm.set_value('total_technician_cost', totalTechnicianCost);
    frm.refresh_field('total_technician_cost');
}
