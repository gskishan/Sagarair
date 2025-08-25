frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        $('.form-link-title span').each(function() {
            if ($(this).text().trim() != "Purchasing") {
                $(this).closest('.col-md-4')
                       .find('.document-link[data-doctype="Material Request"]')
                       .hide();
            }
        });
    }
});
