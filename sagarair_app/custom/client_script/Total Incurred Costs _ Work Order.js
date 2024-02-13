frappe.ui.form.on('Work Order', {
    onload: function(frm) {
        // add custom fields to the form
        frm.add_custom_field('additional_costs', 'Currency', 'Additional Costs');
        frm.add_custom_field('raw_material_consumed_cost', 'Currency', 'Raw Material Consumed Cost');

        // hide the custom field for storing the total cost
        frm.toggle_display('total_incurred_cost', false);
    },
    refresh: function(frm) {
        // show the custom field for storing the total cost
        frm.toggle_display('total_incurred_cost', true);
    }
});

frappe.ui.form.on('Work Order', {
    additional_costs: function(frm) {
        // recalculate the total cost whenever the additional_costs field changes
        calculate_total_cost(frm);
    },
    raw_material_consumed_cost: function(frm) {
        // recalculate the total cost whenever the raw_material_consumed_cost field changes
        calculate_total_cost(frm);
    }
});

function calculate_total_cost(frm) {
    // get the values of the custom fields
    var additional_costs = frm.doc.additional_costs || 0;
    var raw_material_consumed_cost = frm.doc.raw_material_consumed_cost || 0;

    // calculate the total cost
    var total_cost = additional_costs + raw_material_consumed_cost;

    // set the value of the custom field for storing the total cost
    frm.set_value('total_incurred_cost', total_cost);
}
