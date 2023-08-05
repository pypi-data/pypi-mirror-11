define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'service/CollectionFactory'
], 
function($, _, Backbone, CollectionFactory) {
	
	var nameFormat = CollectionFactory.create("nameFormat");

	var NameIDFormat = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:NameIDFormat",
				name : "Name ID Format",
				xml : null,
				text : {options : nameFormat,  value : nameFormat[0].value},
				childs : [],
				options : [],
				attributes : {}
			};
		},
		getParent : function(){
			return this.parent;
		},
		setParent : function(parent){
			this.parent = parent;
		}
	});
	
	return NameIDFormat;
});