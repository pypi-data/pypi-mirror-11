define(
[ 
	'jquery', 
	'underscore', 
	'backbone'
], 
function($, _, Backbone) {

	var KeyInfo = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "ds:KeyInfo",
				name : "Key Info",
				xml : "",
				text : "",
				childs : [],
				options : [],
				attributes : {}
			};
		},
		getParent : function(){
			return this.parent;
		}
	});
	
	return KeyInfo;
});