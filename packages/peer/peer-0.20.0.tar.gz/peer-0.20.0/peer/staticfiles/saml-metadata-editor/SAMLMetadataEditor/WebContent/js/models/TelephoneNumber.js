define(
[ 
	'jquery', 
	'underscore', 
	'backbone'
], 
function($, _, Backbone) {

	var TelephoneNumber = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:TelephoneNumber",
				name : "Telephone Number",
				text : "",
				xml : null,
				childs : [],
				options : [],
				attributes : {}
			};
		},
		getParent : function(){
			return this.parent;
		}
	});
	
	return TelephoneNumber;
});