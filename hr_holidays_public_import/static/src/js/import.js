 openerp.hr_holidays_public_import = function (instance){
    var QWeb = openerp.web.qweb;
    _t = instance.web._t;
    
    instance.web.DataImport.include({
    	get_data: function(model_name, fields) {
    		var data_list = []
    		return new instance.web.Model(model_name)
			.query(fields)
			.all().
			then(function(data) {
					var dd=[];
					var i;
					for (i = 0; i < data.length; i++) {
						dd.push({id : data[i][fields[0]], name : data[i][fields[1]]
							});
						}
						return dd;
					});
    	},
    	start: function () {
    		this._super();
    		var self = this;
    		if (this.res_model == "hr.holidays.public") { 
    			$.when(this.get_data('calendar.provider', ['id', 'provider_name']), this.get_data('res.country', ['id', 'name']))
    			.done(function(providers, countries) {
    				self.$el.append(
    	                    QWeb.render('ImportView.holidays.public', {
    	                    	'providers' :providers,
    	                    	'countries' :countries}
    	                    		));
    				});
    			};
    	},
    	
});
}
