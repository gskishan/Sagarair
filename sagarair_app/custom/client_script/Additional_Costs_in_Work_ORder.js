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
                fieldname: ['total_additional_costs']
            },
            callback: function(r) {
                if (r.message && r.message.total_additional_costs) {
                    frm.set_df_property('additional_costs', 'hidden', false);
                    frm.set_value('additional_costs', r.message.total_additional_costs);
                } else {
                    frm.set_df_property('additional_costs', 'hidden', true);
                }
            }
        });
    }
});
