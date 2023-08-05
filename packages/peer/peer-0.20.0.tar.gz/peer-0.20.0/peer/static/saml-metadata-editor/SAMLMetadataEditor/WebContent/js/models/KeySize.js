define(
[ 
	'jquery', 
	'underscore', 
	'backbone'
], 
function($, _, Backbone) {

	var KeySize = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "xenc:KeySize",
				name : "Key Size",
				xml : null,
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
	
	return KeySize;
});