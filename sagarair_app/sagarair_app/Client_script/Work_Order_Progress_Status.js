frappe.ui.form.on('Work Order', {
    product_group: function(frm) {
        var progress_status_options = [];
        if (frm.doc.product_group === 'AHU/Ventilation/Scrubbers/AirWasher/Fans') {
            progress_status_options = ['Planning', 'Procurement', 'Fabrication', 'Assembly', 'Final Inspection', 'Run Test(QC)', 'Packing','RTD'];
        } else if (frm.doc.product_group === 'Grilles/Diffusers/Aluminium Dampers') {
            progress_status_options = ['Planning', 'Procurement', 'Cutting', 'Assembly', 'Inspection', 'Powder COating','Final Inspection','Packing','RTD'];
        }
        else if (frm.doc.product_group === 'GI VCDs/GI Collar Dampers/Fire and Smoke Dampers') {
            progress_status_options = ['Planning', 'Procurement', 'Fabrication', 'Assembly', 'Final Inspection', 'Packing','RTD'];
        }
        else if (frm.doc.product_group === 'Others') {
            progress_status_options = ['Planning', 'Procurement', 'Fabrication', 'Assembly', 'Inspection', 'Finishing','Final Inspection','Packing','RTD'];
        }
        else if (frm.doc.product_group === 'Dehumidifiers') {
            progress_status_options = ['Planning', 'Procurement', 'Cutting', 'Assembly', 'Inspection', 'Powder COating','Final Inspection','Packing','RTD'];
        }
        else if (frm.doc.product_group === 'Ducting') {
            progress_status_options = ['Planning', 'Procurement', 'Cutting', 'Assembly', 'Inspection', 'Powder COating','Final Inspection','Packing','RTD'];
        }
        
        
        
        frm.set_df_property('progress_status', 'options', progress_status_options);
    },
    refresh: function(frm) {
        // customize progress_status color in list view
        if (frm.doc.__islocal) {
            // only apply this customization for new Work Orders
            var progress_status_field = frm.fields_dict.progress_status;
            progress_status_field.$input.addClass('label-success');
        }
    }
});
