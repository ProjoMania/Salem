odoo.define('test.shop_cart', function (require) {
"use strict";

var rpc = require('web.rpc');
var core = require('web.core');
var _t = core._t;
var form_widget = require('web.Widget');

$(document).on('click', '#test_button', function(){
        return rpc.query({
            model: 'employee.attendance.map',
            method: 'show_map',
            args: [1],
        }, {
            async: false
        }).then(function (result) {
            if(result && result[0]){
                if(!result[0].connection){
                    alert("No inernet connection.");
                    return false;
                }
                var lat_long = [];
                var str = "";
                for(var i=0; i<result.length; i++){
                        var exit = true;
                        if(result[i].latitude && result[i].longitude){
                            if(lat_long.length > 0){
                                _.each(lat_long, function(item){
                                    if($.inArray(result[i].latitude, item) !== -1 && $.inArray(result[i].longitude,item) !== -1){
                                        item[1] = item[1] + 1;
                                        exit = false;
                                        return;
                                    }
                                });
                            }
                            if(exit){
                                if(result[i].image)
                                {
                                 str = "<img class='img-circle' src='data:image/png;base64,"+ result[i].image +"' width='50' height='50'> "
                                }
                                str += result[i].name
                                console.log(result[i].job_position,result[i].dept_id,result[i].date,result[i].emp_id)
                                str += "<button style='margin-left:15px;' title='Attendance Detail' class='btnpopup btn btn-icon fa fa-lg fa-list-ul o_cp_switch_list' data-job_position="+result[i].job_position+" data-dept_id="+result[i].dept_id+" data-date="+result[i].date+" data-cust-id="+result[i].emp_id+" data-btn='30'></button>"
                                lat_long.push([str,result[i].latitude,result[i].longitude, 0]);
                            }
                        }
                    }
                if(lat_long.length > 0){
                    initialize_gmap(lat_long);
                    $('.o_statusbar_buttons > ').prop("disabled", false);
                    return true
                }else{
                    alert("No Record Found")
                    if(result && result[0].connection){
                        initialize_gmap([]);
                        $('.o_statusbar_buttons > ').prop("disabled", false);
                    }
                    return false;
                }
            }
         })

});


form_widget.include({
		events: {
	        'click .btnpopup': '_onclick_btnpopup',
	    },
	    _onclick_btnpopup : function(event){
	    	var self = this;
	    	event.handled = false;
	    	if(event.handled !== true) // This will prevent event triggering more then once
        	{
            	event.handled = true;
            	var id = $(event.currentTarget).data('cust-id')
            	var at_date = $(event.currentTarget).data('date')
            	var btn = $(event.currentTarget).data('btn')
            	var job_position = $(event.currentTarget).data('job_position')
            	var dept_id = $(event.currentTarget).data('dept_id')
                if (id && btn){

                     return rpc.query({
                        model: 'employee.attendance.map',
                        method: 'employee_attendance',
                        args: [id,id,at_date,dept_id,job_position],
                    }, {
                        async: false
                    }).then(function (result) {
                        var result = JSON.parse(result);
                        if(result && result.filter_domain){
                            self.do_action({
                                type: 'ir.actions.act_window',
                                res_model: "hr.attendance",
                                name: _t('Employee Attendance'),
                                views: [[false,"list"]],
                                domain: result.filter_domain,
                                context: {
                                    create: false,
                                    edit:false,
                                },
                                target: 'new',
                            });
                        }
                        else{
                               alert("No Employee Found");
                            }
                     })
				}
			}
	    },
    });
});