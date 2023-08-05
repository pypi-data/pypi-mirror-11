define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'service/CollectionFactory'
], 
function($, _, Backbone, CollectionFactory) {

	var lang = CollectionFactory.create("lang");
	
	var OrganizationDisplayName = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:OrganizationDisplayName",
				name : "Organization Display Name",
				text : {options : null,  value : ""},
				xml : null,
				childs : [],
				options : [],
				attributes : {
				  "xml:lang" : {name : "Lang", options : lang,  value : lang[0].value}
				}
			};
		},
		getParent : function(){
			return this.parent;
		},
		setParent : function(parent){
			this.parent = parent;
		}
	});
	
	return OrganizationDisplayName;
});