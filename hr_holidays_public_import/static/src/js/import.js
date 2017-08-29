 openerp.hr_holidays_public_import = function (instance){
    var QWeb = openerp.web.qweb;
    _t = instance.web._t;
    
    //var base_import = instance.base_import
    instance.web.DataImport.include({
    	start: function () {
    		this._super();
    		var self = this;
    		if (this.res_model == "hr.holidays.public") { 
    			var provider_list = new instance.web.Model('calendar.provider')
    			.query(['id','provider_name'])
    			.all().
    			then(function(data) {
    					var dd=[];
    					var i;
    					for (i = 0; i < data.length; i++) {dd.push({id : data[i].id, name : data[i].provider_name});}
    						return dd;
    					}).then(function(result) {self.$el.append(
    		                    QWeb.render('ImportView.holidays.public', {'providers' : result}
    		                    ));});
    			/*this.$el.append(
                    QWeb.render('ImportView.holidays.public', {'providers' : provider_list}
));*/
    			};
    	},
    	
});
}
