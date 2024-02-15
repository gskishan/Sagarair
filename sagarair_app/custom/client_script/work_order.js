frappe.ui.form.on("Work Order Item", "consumed_qty", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    frm.doc.required_items.forEach(function(item) {
        item.consumed_value = flt(item.consumed_qty * item.rate);
    });
    frm.refresh_field("required_items");
});

frappe.ui.form.on('Work Order', {
    onload: function(frm) {
        frm.add_custom_field('additional_costs', 'Currency', 'Additional Costs');
        frm.add_custom_field('raw_material_consumed_cost', 'Currency', 'Raw Material Consumed Cost');
        frm.toggle_display('total_incurred_cost', false);
        frm.add_custom_field('total_cost_per_unit', 'Currency', 'Total Cost Per Unit');
        frm.toggle_display('total_cost_per_unit', false);
    },
    refresh: function(frm) {
        frm.toggle_display('total_incurred_cost', true);
        frm.toggle_display('total_cost_per_unit', true);
    },
    additional_costs: function(frm) {
        calculate_total_cost(frm);
    },
    raw_material_consumed_cost: function(frm) {
        calculate_total_cost(frm);
    },
    produced_qty: function(frm) {
        calculate_total_cost_per_unit(frm);
    },
    total_incurred_cost: function(frm) {
        calculate_total_cost_per_unit(frm);
    },
    refresh: function(frm) {
        if (frm.doc.status === 'Completed') {
            frm.add_custom_button(__('Manufacture Stock Entry'), function() {
                frappe.set_route('List', 'Stock Entry', {'work_order': frm.doc.name});
            });
        }
    },
    product_group: function(frm) {
        var progress_status_options = [];
        if (frm.doc.product_group === 'AHU/Ventilation/Scrubbers/AirWasher/Fans') {
            progress_status_options = ['Planning', 'Procurement', 'Fabrication', 'Assembly', 'Final Inspection', 'Run Test(QC)', 'Packing','RTD'];
        } else if (frm.doc.product_group === 'Grilles/Diffusers/Aluminium Dampers') {
            progress_status_options = ['Planning', 'Procurement', 'Cutting', 'Assembly', 'Inspection', 'Powder COating','Final Inspection','Packing','RTD'];
        } else if (frm.doc.product_group === 'GI VCDs/GI Collar Dampers/Fire and Smoke Dampers') {
            progress_status_options = ['Planning', 'Procurement', 'Fabrication', 'Assembly', 'Final Inspection', 'Packing','RTD'];
        } else if (frm.doc.product_group === 'Others') {
            progress_status_options = ['Planning', 'Procurement', 'Fabrication', 'Assembly', 'Inspection', 'Finishing','Final Inspection','Packing','RTD'];
        } else if (frm.doc.product_group === 'Dehumidifiers' || frm.doc.product_group === 'Ducting') {
            progress_status_options = ['Planning', 'Procurement', 'Cutting', 'Assembly', 'Inspection', 'Powder COating','Final Inspection','Packing','RTD'];
        }
        frm.set_df_property('progress_status', 'options', progress_status_options);
    }
});

function calculate_total_cost(frm) {
    var additional_costs = frm.doc.additional_costs || 0;
    var raw_material_consumed_cost = frm.doc.raw_material_consumed_cost || 0;
    var total_cost = additional_costs + raw_material_consumed_cost;
    frm.set_value('total_incurred_cost', total_cost);
}

function calculate_total_cost_per_unit(frm) {
    var produced_qty = frm.doc.produced_qty || 0;
    var total_incurred_cost = frm.doc.total_incurred_cost || 0;
    var total_cost_per_unit = produced_qty ? (total_incurred_cost / produced_qty) : 0;
    frm.set_value('total_cost_per_unit', total_cost_per_unit);
}
