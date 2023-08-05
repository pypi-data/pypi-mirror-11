define(
[ 
	'jquery', 
	'underscore', 
	'backbone'
], 
function($, _, Backbone) {

	var AttributeService = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:AttributeService",
				name : "Attribute Service",
				xml : "",
				text : null,
				childs : [],
				options : [],
				attributes : {
					Binding : {name : "Binding", options : null,  value : "", required : true},
					Location: {name : "Location", options : null, value : "", required : true},
					ResponseLocation : {name : "Response Location", options : null, value : "", required : false}
				}
			};
		},
		getParent : function(){
			return this.parent;
		}
	});
	
	return AttributeService;
});