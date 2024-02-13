frappe.ui.form.on('Work Order', {
    onload: function(frm) {
        // add custom field to the form
        frm.add_custom_field('total_cost_per_unit', 'Currency', 'Total Cost Per Unit');

        // hide the custom field for storing the total cost per unit
        frm.toggle_display('total_cost_per_unit', false);
    },
    refresh: function(frm) {
        // show the custom field for storing the total cost per unit
        frm.toggle_display('total_cost_per_unit', true);
    },
    produced_qty: function(frm) {
        // recalculate the total cost per unit whenever the produced_qty field changes
        calculate_total_cost_per_unit(frm);
    },
    total_incurred_cost: function(frm) {
        // recalculate the total cost per unit whenever the total_incurred_cost field changes
        calculate_total_cost_per_unit(frm);
    }
});

function calculate_total_cost_per_unit(frm) {
    // get the values of the fields
    var produced_qty = frm.doc.produced_qty || 0;
    var total_incurred_cost = frm.doc.total_incurred_cost || 0;

    // calculate the total cost per unit
    var total_cost_per_unit = produced_qty ? (total_incurred_cost / produced_qty) : 0;

    // set the value of the custom field for storing the total cost per unit
    frm.set_value('total_cost_per_unit', total_cost_per_unit);
}
