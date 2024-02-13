frappe.ui.form.on("Sales Order", {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    "doctype": "Work Order",
                    "filters": {
                        "sales_order": frm.doc.name
                    },
                    "fields": ["progress_status"]
                },
                callback: function(response) {
                    if (response.message && response.message.length > 0) {
                        var all_ready = true;
                        for (var i = 0; i < response.message.length; i++) {
                            if (response.message[i].progress_status !== "RTD") {
                                all_ready = false;
                                break;
                            }
                        }
                        if (all_ready) {
                            frm.set_value("manufacture_status", "ALL-RTD");
                        } else {
                            frm.set_value("manufacture_status", "IN-PROG");
                        }
                    } else {
                        frm.set_value("manufacture_status", "NO-WO");
                    }
                }
            });
        }
    }
});
