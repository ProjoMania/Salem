odoo.define('aspl_employee_attendance_map.main', function(require) {
    "use strict";

    var hr_attendance = require('hr_attendance.my_attendances');
    var KioskMode = require('hr_attendance.kiosk_confirm');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var _t = core._t;
    var isloc=1;
    var list=[]
    function check_att(latitude, longitude, employee_id) {
        var isWithinPolygon
        if (latitude && longitude && employee_id) {
            var data = [];
            rpc.query({
                    model: 'hr.employee',
                    method: 'search_lat_lng',
                    args: [employee_id],
                }, {
                    async: false
                })
                .then(function(res) {
                    if (res) {
                        $.each(res, function(key, value) {
                            $.each(value, function(k, v) {
                                data.push({
                                    'lat': parseFloat(v.latitude),
                                    'lng': parseFloat(v.longitude)
                                })
                            });
                        });
                var rightShoulderFront = new google.maps.Polygon({
                    paths: data,
                    strokeColor: '#0000CC',
                    strokeOpacity: 0.5,
                    strokeWeight:1,
                    fillColor:'red',
                    fillOpacity:0.25
                });
                const geocoder = new google.maps.Geocoder();
                const selectedFullAddress='Jalan Chengal, Kampung Melayu Subang, 40150 Shah Alam, Selangor, Malaysia';
                geocoder.geocode({ address: selectedFullAddress },function(results,status){
                        var curPosition     = new google.maps.LatLng(latitude,longitude);
                        isWithinPolygon = google.maps.geometry.poly.containsLocation(curPosition, rightShoulderFront)

                        rpc.query({
                            model: 'hr.employee',
                            method: 'inside_poly',
                            args:[employee_id,isWithinPolygon],
                        }).then(function () {
                            console.log("Success")
                        }).catch(function (reason){
                            var error = reason.message;

                        });
                    });
                    }
                });
                return true
        }
    }

    hr_attendance.include({
        events: _.extend(hr_attendance.prototype.events ,{
            "click .o_hr_attendance_sign_in_out_icon": _.debounce(function(e) {
                this.state = $(e.currentTarget).data('state');
                this.update_attendance();
            }, 10, true),
        }),
        update_attendance: function() {
            var self = this;
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    self.latitude = position.coords.latitude;
                    self.longitude = position.coords.longitude;
                    console.log(self.latitude,self.longitude)
                    var isWithinPolygon = check_att(self.latitude, self.longitude, self.employee.id)
                    setTimeout(function() {
                        console.log(isWithinPolygon,"ll")
                        if (isWithinPolygon && self.latitude) {
                            self._rpc({
                                    model: 'hr.employee',
                                    method: 'attendance_manual',
                                    args: [
                                        [self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances', '', self.latitude, self.longitude
                                    ],
                                    context: {
                                        'state': self.state,
                                    },
                                })
                                .then(function(result) {
                                    if(result){
                                        if (result.action) {
                                       self.do_action(result.action);

                                    } else if (result.warning) {
                                          Dialog.alert(
                                           this,
                                           result.warning,
                                           {
                                               confirm_callback: function(){
                                               }
                                           }
                                        );
                                    }
                                    }
                                    if(!result){
                                        Dialog.alert(
                                           this,
                                           "You are not Allowed to make Attendance entry from This Location!",
                                           {
                                               confirm_callback: function(){
                                               }
                                           }
                                        );
                                    }
                                });
                        } else {
                            if(self.latitude){
                                self._rpc({
                                    model: 'hr.employee',
                                    method: 'attendance_manual',
                                    args: [
                                        [self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances', '', self.latitude,[0,self.longitude]
                                    ],
                                })
                                Dialog.alert(
                                   this,
                                   "You are not Allowed to make Attendance entry from This Location!",
                                   {
                                       confirm_callback: function(){
                                       }
                                   }
                                );
                            }
                            else{
                                Dialog.alert(
                                   this,
                                   "Try Again",
                                   {
                                       confirm_callback: function(){
                                       }
                                   }
                                );
                            }
                        }
                    }, 400);
                });
            }
        },
    });
    KioskMode.include({
        events: _.extend({}, KioskMode.prototype.events, {
            "click .o_hr_attendance_sign_in_out_icon": function() {
                var self = this;
                if ("geolocation" in navigator) {
                    navigator.geolocation.getCurrentPosition(function(position) {
                        self.latitude = position.coords.latitude;
                        self.longitude = position.coords.longitude;
                    });
                }
                this.$('.o_hr_attendance_sign_in_out_icon').attr("disabled", "disabled");
                setTimeout(function() {
                    var isWithinPolygon = check_att(self.latitude, self.longitude, self.employee_id)
                    if (isWithinPolygon) {
                        self._rpc({
                                model: 'hr.employee',
                                method: 'attendance_manual',
                                args: [
                                    [self.employee_id], self.next_action, '', self.latitude, self.longitude
                                ],
                            })
                            .then(function(result) {
                                if (result.action) {
                                    self.do_action(result.action);
                                } else if (result.warning) {
                                      Dialog.alert(
                                       this,
                                       result.warning,
                                       {
                                           confirm_callback: function(){
                                           }
                                       }
                                    );
                                    self.$('.o_hr_attendance_sign_in_out_icon').removeAttr("disabled");
                                }
                            });
                    } else {
                          Dialog.alert(
                           this,
                           "You are not Allowed to make Attendance entry from This Location!",
                           {
                               confirm_callback: function(){
                               }
                           }
                        );
                    }
                }, 1500);
            },
        }),
    });
});