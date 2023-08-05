define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'service/CollectionFactory'
], 
function($, _, Backbone, CollectionFactory) {

	var boolean = CollectionFactory.create("boolean");
	var bindings = CollectionFactory.create("bindings");;

	var AssertionConsumerService = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:AssertionConsumerService",
				name : "Assertion Consumer Service",
				xml : "",
				text : null,
				childs : [],
				options : [],
				attributes : {
					Binding : {name : "Binding", options : bindings,  value : bindings[0].value, required : true},
					Location: {name : "Location", options : null, value : "", required : true},
					ResponseLocation : {name : "Response Location", options : null, value : "", required : false},
					index : {name : "Index", options : null, value : "", required : true},		
					isDefault : {name : "Is Default", options : boolean, value : boolean[0].value, required : false}				
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
			
			var numbreRegex = new RegExp("^\\d+$");
			if(attrs.attributes.index.value == "")
				obj["index"] = "This field is required";
			else
				if(attrs.attributes.index.value != "" && !numbreRegex.test(attrs.attributes.index.value))
					obj["index"] = "The value must be a unsigned short";			

			return obj;
		},
		getParent : function(){
			return this.parent;
		},
		setParent : function(parent){
			this.parent = parent;
		}
	});
	
	return AssertionConsumerService;
});