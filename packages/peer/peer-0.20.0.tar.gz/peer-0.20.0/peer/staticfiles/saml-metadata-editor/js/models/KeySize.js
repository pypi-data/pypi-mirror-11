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
				text : {options : null,  value : ""},
				childs : [],
				options : [],
				attributes : {}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};
			
			var numbreRegex = new RegExp("^\\d+$");
			if(attrs.text != null && attrs.text.value != "" && !numbreRegex.test(attrs.text.value))
				obj["text"] = "The text content must be a integer";
			
			return obj;
		},
		getParent : function(){
			return this.parent;
		},
		setParent : function(parent){
			this.parent = parent;
		}
	});
	
	return KeySize;
});