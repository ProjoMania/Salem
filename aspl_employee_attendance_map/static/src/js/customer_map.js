var key = ''
var record_id = false;
var new_rpc = false;

$.ajax({
	type: "GET",
	dataType: 'json',
	url: '/get_api_key',
	data: {},
	async: false,
	success: function(success) {
		if (success){
			key = success.key;
		}
	},
});

document.write('<script type="text/javascript" async defer src="https://maps.googleapis.com/maps/api/js?libraries=drawing,geometry,places&key='+key+'"></script>');
var script = '<script type="text/javascript" src="/aspl_employee_attendance_map/static/src/js/markerclusterer';
if (document.location.search.indexOf('compiled') !== -1) {
	script += '_compiled';
}
script += '.js"><' + '/script>';
document.write(script);

function initialize_gmap(lat_long) {
	var map;
	var bounds = new google.maps.LatLngBounds();
	var mapOptions = {
		mapTypeId: 'roadmap',
		streetViewControl: true,
		fullscreenControl: true
	};
	// Display a map on the page
	map = new google.maps.Map(document.getElementById("map"), mapOptions);
	map.setTilt(45);

	markers = lat_long
	var infoWindow = new google.maps.InfoWindow(), marker, i;
	for( i = 0; i < markers.length; i++ ) {
		var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
		bounds.extend(position);
		marker = new google.maps.Marker({
			position: position,
			map: map,
		});
		marker.setAnimation(google.maps.Animation.DROP);
		google.maps.event.addListener(marker, 'click', (function(marker, i) {
			return function() {
				infoWindow.setContent("<b>"+lat_long[i][0]+"</b>");
				infoWindow.open(map, marker);
			}
		})(marker, i));
		map.fitBounds(bounds);
	}

	// Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
	var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
		this.setZoom(13);
		google.maps.event.removeListener(boundsListener);
	});
}

function initialize_maps(lat_lng, id, rpc) {
	record_id = id;
	new_rpc = rpc;
	var latitude = 11.2541738,longitude = 75.8370729;

	setTimeout(function(){
		var map;
		var bounds = new google.maps.LatLngBounds();
		var initial = new google.maps.LatLng(latitude, longitude);
		var mapOptions = {
			mapTypeId: 'roadmap',
			streetViewControl: true,
			fullscreenControl: true,
			zoom: 5,
			center: initial,
		};
		// Display a map on the page
		map = new google.maps.Map(document.getElementById("employee_map"), mapOptions);
		initialLocation = new google.maps.LatLng(latitude, longitude);
		navigator.geolocation.getCurrentPosition(function(position) {
			initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            map.setCenter(initialLocation);
            map.setZoom(13);
		});
		var arr = new Array();
		var markers = {};
		if(lat_lng){
			$.each(lat_lng, function( key, value ) {
				arr = [];
				$.each(value, function( k, v ) {
					arr.push( new google.maps.LatLng(
						parseFloat(v.latitude),
						parseFloat(v.longitude)
					));
				});
				var id = value[0].id;
				var poly = new google.maps.Polygon({
					id: id,
					paths: arr,
					strokeColor: '#FF0000',
					strokeOpacity: 0.8,
					strokeWeight: 2,
					fillColor: '#FF0000',
					fillOpacity: 0.35,
					clickable: true,
					editable: true,
					draggable: true,
					zIndex: 1,
				});
				poly.setMap(map)
				markers[id] = poly;
				google.maps.event.addListener(poly, 'rightclick', function (event) {
					var r = confirm("Are you sure you want to delete this record ?");
					if (r == true) {
						var emp_lat_id = this.id
						if(emp_lat_id && record_id && new_rpc){
							new_rpc.query({
								model: 'hr.employee',
								method: 'delete_lat_lng',
								args: [record_id, emp_lat_id],
							}, {
								async: false
							})
							.then(function(res) {
								if (res) {
									delMarker(emp_lat_id);
								}
							});
						}
					}
				});
			});
		}

		var delMarker = function(id) {
			var marker = markers[id];
			if (marker){
				marker.setMap(null);
			}
		}
		var drawingManager = new google.maps.drawing.DrawingManager({
			drawingMode: google.maps.drawing.OverlayType.POLYGON,
			drawingControl: true,
			drawingControlOptions: {
				position: google.maps.ControlPosition.TOP_CENTER,
				drawingModes: [google.maps.drawing.OverlayType.POLYGON]
			},
		});
		drawingManager.setMap(map);
		drawingManager.setDrawingMode(null);
		google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
			var polyArray = []
			for (var i = 0; i < e.overlay.getPath().getLength(); i++) {
				polyArray.push({
					'lat':e.overlay.getPath().getAt(i).lat(),
					'lng':e.overlay.getPath().getAt(i).lng()
				})
			}
			if (polyArray){
				new_rpc.query({
					model: 'hr.employee',
					method: 'store_lat_lng',
					args: [record_id, polyArray],
				}, {
					async: false
				})
				.then(function(res) {
					if (res) {
						window.location.reload();
					}
				});
			}
			drawingManager.setDrawingMode(null);
		});
	},1500);
}

function initialize_map_readonly(lat_lng) {
	var latitude = 11.2541738,longitude = 75.8370729;

	setTimeout(function(){
		var map;
		var bounds = new google.maps.LatLngBounds();
		var initial = new google.maps.LatLng(latitude, longitude);
		var mapOptions = {
			mapTypeId: 'roadmap',
			streetViewControl: true,
			fullscreenControl: true,
			zoom: 5,
			center: initial,
		};
		// Display a map on the page
		map = new google.maps.Map(document.getElementById("employee_map"), mapOptions);
		initialLocation = new google.maps.LatLng(latitude, longitude);
		navigator.geolocation.getCurrentPosition(function(position) {
			initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            map.setCenter(initialLocation);
            map.setZoom(13);
		});
		var arr = new Array();
		var markers = {};
		if(lat_lng){
			$.each(lat_lng, function( key, value ) {
				arr = [];
				$.each(value, function( k, v ) {
					arr.push( new google.maps.LatLng(
						parseFloat(v.latitude),
						parseFloat(v.longitude)
					));
				});
				var id = value[0].id;
				var poly = new google.maps.Polygon({
					id: id,
					paths: arr,
					strokeColor: '#FF0000',
					strokeOpacity: 0.8,
					strokeWeight: 2,
					fillColor: '#FF0000',
					fillOpacity: 0.35,
					clickable: true,
					editable: true,
					draggable: true,
					zIndex: 1,
				});
				poly.setMap(map)
				markers[id] = poly;
			});
		}

	},1500);
}

odoo.define('aspl_employee_attendance_map.customer_map', function (require) {
"use strict";
	var FormRenderer = require('web.FormRenderer');

	FormRenderer.include({
		_renderView: function () {
			var self = this;

			// render the form and evaluate the modifiers
			var defs = [];
			this.defs = defs;
			this.inactiveNotebooks = [];
			var $form = this._renderNode(this.arch).addClass(this.className);
			delete this.defs;

			if (self.state.model && self.state.model == 'hr.employee' && self.state.res_id && self.mode == 'edit'){
				setTimeout(function (){
					var rpc = require('web.rpc');
					var lat_lng = [];
					rpc.query({
						model: 'hr.employee',
						method: 'search_lat_lng',
						args: [self.state.res_id],
					}, {
						async: false
					})
					.then(function(res) {
						if (res) {
							lat_lng = res;
							initialize_maps(lat_lng, self.state.res_id, rpc)
						}
					});
					initialize_maps(lat_lng, self.state.res_id, rpc)
				},100);
			}
			else if(self.state.model && self.state.model == 'hr.employee' && self.mode != 'edit'){
				setTimeout(function (){
					var rpc = require('web.rpc');
					var lat_lng = [];
					rpc.query({
						model: 'hr.employee',
						method: 'search_lat_lng',
						args: [self.state.res_id],
					}, {
						async: false
					})
					.then(function(res) {
						if (res) {
							lat_lng = res;
							initialize_map_readonly(lat_lng)
						}
					});
					initialize_map_readonly(lat_lng)
				},100);
			}

			return Promise.all(defs).then(() => this.__renderView()).then(function () {
            self._postProcessLabels();
            self._updateView($form.contents());
            self.manuallyDisabledButtons.clear();
            if (self.state.res_id in self.alertFields) {
                self.displayTranslationAlert();
            }
        }).then(function(){
            if (self.lastActivatedFieldIndex >= 0) {
                self._activateNextFieldWidget(self.state, self.lastActivatedFieldIndex);
            }
        }).guardedCatch(function () {
            $form.remove();
        });
		},
	});
});