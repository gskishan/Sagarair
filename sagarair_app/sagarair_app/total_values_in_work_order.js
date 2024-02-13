frappe.ui.form.on('Work Order', {
    refresh: function(frm) {
        if (frm.doc.__islocal) return;

        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Stock Entry',
                filters: {
                    work_order: frm.doc.name,
                    purpose: 'Manufacture'
                },
                fieldname: ['total_outgoing_value']
            },
            callback: function(r) {
                if (r.message && r.message.total_outgoing_value) {
                    frm.set_df_property('raw_material_consumed_cost', 'hidden', false);
                    frm.set_value('raw_material_consumed_cost', r.message.total_outgoing_value);
                } else {
                    frm.set_df_property('raw_material_consumed_cost', 'hidden', true);
                }
            }
        });
    }
});
