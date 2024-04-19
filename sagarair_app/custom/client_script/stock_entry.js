frappe.ui.form.on('Stock Entry', {
  refresh: function(frm) {
    if (frm.doc.purpose === 'Manufacture') {
      frm.add_custom_button(__('Extract items to BOM'), function() {
        var items = frm.doc.items;
        var bom_items = [];
        for (var i=0; i<items.length; i++) {
          var item = items[i];
          if (item.item_code && item.qty > 0) {
            var bom_item = {
              'item_code': item.item_code,
              'qty': item.qty,
              'uom': item.uom,
              'stock_uom': item.stock_uom,
              'conversion_factor': item.conversion_factor,
              'rate': item.rate,
              'amount': item.amount,
              'warehouse': item.warehouse
            };
            bom_items.push(bom_item);
          }
        }
        var bom = frappe.model.get_new_doc('BOM');
        bom.items = [];
        bom_items.forEach(function(item) {
          var bom_item = frappe.model.add_child(bom, 'BOM Item', 'items');
          bom_item.item_code = item.item_code;
          bom_item.qty = item.qty;
          bom_item.uom = item.uom;
          bom_item.stock_uom = item.stock_uom;
          bom_item.conversion_factor = item.conversion_factor;
          bom_item.rate = item.rate;
          bom_item.amount = item.amount;
          bom_item.warehouse = item.warehouse;
        });
        frappe.set_route('Form', 'BOM', bom.name);
        frappe.after_ajax(function() {
          cur_frm.save();
        });
      }).addClass('btn-primary');
    }
  }
});
frappe.ui.form.on('Landed Cost Taxes and Charges', {
  amount(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    // console.log(row.amount, "ROW")
    if (row.expense_account == "Labour Cost ( Included in Valuation ) - SAPL") {
      frm.set_value("custom_labour_cost_amnt", row.amount)
    }
    else if (row.expense_account == "Powder Coating (Included in Valuation) - SAPL") {
      frm.set_value("custom_powder_coating_amnt", row.amount)
    }
  }
})