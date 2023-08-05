define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'service/CollectionFactory'
], 
function($, _, Backbone, CollectionFactory) {

	var bindings = CollectionFactory.create("bindings");

	var ManageNameIDService = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:ManageNameIDService",
				name : "Manage Name ID Service",
				xml : "",
				text : null,
				childs : [],
				options : [],
				attributes : {
					Binding : {name : "Binding", options : bindings,  value : bindings[0].value, required : true},
					Location: {name : "Location", options : null, value : "", required : true},
					ResponseLocation : {name : "Response Location", options : null, value : "", required : false}
				}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};

			// URL validation
			var urlRegex = new RegExp("^\\s?(https?:\/\/)?[\\w-]+(\\.[\\w-]+)+\.?(:\\d+)?(\/\\S*)?$", "i");

			if(attrs.attributes.Location.value == "")
				obj["Location"] = "This field is required";
			else
				if(!urlRegex.test(attrs.attributes.Location.value))
					obj["Location"] = "This field must be a URL";

			if(attrs.attributes.ResponseLocation.value != "" && !urlRegex.test(attrs.attributes.ResponseLocation.value))
				obj["ResponseLocation"] = "This field must be a URL";
			
			return obj;
		},
		getParent : function(){
			return this.parent;
		},
		setParent : function(parent){
			this.parent = parent;
		}
	});
	
	return ManageNameIDService;
});