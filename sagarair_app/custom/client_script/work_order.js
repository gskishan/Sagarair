frappe.ui.form.on("Work Order Item", "consumed_qty", function (frm, cdt, cdn) {
var d = locals[cdt][cdn];
frm.doc.required_items.forEach(function(d){d.consumed_value = flt(d.consumed_qty * d.rate) });
frappe.model.set_value("consumed_value",consumed_value);
})


frappe.ui.form.on("Work Order Item", "consumed_qty", function on_change_consumed_qty(doc, cdt, cdn){
    if (doc.consumed_qty){ 
        
doc.consumed_value = flt(doc.consumed_qty * doc.rate) ;
cur_frm.refresh();
}
cur_frm.custom_consumed_qty = on_change_consumed_qty;

});



frappe.ui.form.on("Work Order Item", "consumed_qty", function on_change_consumed_qty(doc, cdt, cdn){
    if (doc.consumed_qty){ 
        var d = locals[cdt][cdn];
frm.doc.required_items.forEach(function(d){d.consumed_value = flt(d.consumed_qty * d.rate) });
frappe.model.set_value("consumed_value",consumed_value);
cur_frm.refresh();
}
cur_frm.custom_consumed_qty = on_change_consumed_qty;

});


frappe.ui.form.on("Work Order Item", "consumed_qty", function(frm, cdt, cdn){

var d = locals[cdt][cdn];
frm.doc.required_items.forEach(function(d){d.consumed_value = flt(d.consumed_qty * d.rate) });
frappe.model.set_value("consumed_value",consumed_value);

});

// frappe.ui.form.on("Work Order", "onload", function(frm, cdt, cdn) {
//     var d = locals[cdt][cdn];
// var expenses = cur_frm.doc.required_items;
// console.log("expenses--------------"+expenses.length);
// var total_clm = 0;
//     for (var i = 0; i < required_items.length; i++){
// var amount = required_items[i].consumed_value;

// total_clm = total_clm + consumed_value;

// }
// console.log("total_expense---------------"+total_clm); 

// cur_frm.doc.total_consumed_value = total_clm;
// cur_frm.refresh_field("total_consumed_value");
// cur_frm.refresh();


// });
// frappe.ui.form.on("Work Order","before_save",function(frm, cdt, cdn){
//     var d = locals[cdt][cdn];
//     frappe.model.set_value(cdt, cdn, "actual_cost", d.total_consumed_value + d.labour_cost);
    
//     });
