define(
[ 
	'jquery', 
	'underscore', 
	'backbone'
], 
function($, _, Backbone) {

	var OAEPparams = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "xenc:OAEPparams",
				name : "OAEP params",
				xml : null,
				text : {options : null,  value : ""},
				childs : [],
				options : [],
				attributes : {}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};
			
			var numbreRegex = new RegExp("^[a-zA-Z/+=\\s\\d]+$");
			if(attrs.text != null && attrs.text.value != "" && !numbreRegex.test(attrs.text.value))
				obj["text"] = "The text content must be a base 64";
			
			var aux = attrs.text.value.replace(" ","");			
			
			if(aux.length % 4 != 0)
				obj["text"] = "The number of non-whitespace characters must be divisible by 4";
			
			return obj;
		},
		getParent : function(){
			return this.parent;
		},
		setParent : function(parent){
			this.parent = parent;
		}
	});
	
	return OAEPparams;
});