define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'service/CollectionFactory'
], 
function($, _, Backbone, CollectionFactory) {

	var lang = CollectionFactory.create("lang");
	
	var OrganizationURL = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:OrganizationURL",
				name : "Organization URL",
				text : {options : null,  value : ""},
				xml : null,
				childs : [],
				options : [],
				attributes : {
				  "xml:lang" : {name : "Lang", options : lang,  value : lang[0].value}
				}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};
			
			// URL validation
			var urlRegex = new RegExp("^\\s?(https?:\/\/)?[\\w-]+(\\.[\\w-]+)+\.?(:\\d+)?(\/\\S*)?$", "i");
			if(attrs.text != null && attrs.text.value != "" && !urlRegex.test(attrs.text.value))
				obj["text"] = "The text content must be a URL";
			
			return obj;
		},
		getParent : function(){
			return this.parent;
		},
		setParent : function(parent){
			this.parent = parent;
		}
	});
	
	return OrganizationURL;
});