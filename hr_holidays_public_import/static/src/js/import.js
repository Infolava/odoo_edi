 openerp.hr_holidays_public_import = function (instance){
    var QWeb = openerp.web.qweb;
    _t = instance.web._t;
    
openerp.web.ListView.include({
    load_list: function() {
    	var self = this;
    	this._super.apply(this, arguments);
        if(this.$buttons) {
            this.$buttons.on('click', '.oe_button_import', function() {
            	self.do_action({
                    type: "ir.actions.act_window",
                    name: "Import Public Holiday",
                    res_model: "hr.holidays.public.wizard",
                    target: 'new',
                    view_type : 'form',
                    view_mode : 'form',
                    views: [[false,'form']],
                }, {
                    on_reverse_breadcrumb: function () {
                        self.reload();
                    },
                });
                return false;
            });
        }
    },
//}
});
}
