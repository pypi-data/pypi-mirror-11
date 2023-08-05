define(
[ 
	'jquery', 
	'underscore', 
	'backbone'
], 
function($, _, Backbone) {

	var AdditionalMetadataLocation = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:AdditionalMetadataLocation",
				name : "Additional Metadata Location",
				text : "",
				xml : null,
				childs : [],
				options : [],
				attributes : {
					namespace : {name : "Namespace", options : null,  value : "", required : true}
				}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};
			
			//	Attribute validation
			var urlRegex = new RegExp("(^|\\s)((https?:\/\/)?[\\w-]+(\\.[\\w-]+)+\.?(:\\d+)?(\/\\S*)?)", "i");
			if(attrs.attributes.namespace.value == "")
				obj["namespace"] = "This field is required";
			else
				if(!urlRegex.test(attrs.attributes.namespace.value))
					obj["namespace"] = "This field must be a URL";

			// Text content Validation
			if(	attrs.text != "" && !urlRegex.test(attrs.text))
				obj["text"] = "The text content must be a URL";
			
			return obj;
		},
		getParent : function(){
			return this.parent;
		}
	});
	
	return AdditionalMetadataLocation;
});