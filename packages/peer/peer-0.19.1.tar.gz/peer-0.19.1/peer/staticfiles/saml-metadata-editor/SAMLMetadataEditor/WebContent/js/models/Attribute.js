define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/AttributeValue'
], 
function($, _, Backbone, AttributeValue) {

	var Attribute = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "saml:Attribute",
				name : "Attribute",
				xml : null,
				text : null,
				childs : [null],
				options : [
				    {value:"saml:AttributeValue", name:"AttributeValue", disabled : false}
				],
				attributes : {
					Name : {name : "Name", options : null,  value : "", required : true},
					NameFormat: {name : "NameFormat", options : null, value : "", required : false},
					FriendlyName : {name : "Friendly Name", options : null, value : "", required : false}
				}
			};
		},
		addChild : function(type){

			var node = null;
			
			switch (type) { 
			  case "saml:AttributeValue":
				node = new AttributeValue({parent : this});
				this.get("childs")[0] = node;
				this.get("options")[0].disabled = false;

				break;
			  default: 
				console.log("EntitiesDescriptor.addChild ==> Bad Child Type");
			    break;
			}			
			
			return node;
		},
		removeChild : function(childNode){
			switch (childNode.get("tag")) { 
			  case "saml:AttributeValue":
				this.get("childs")[0] = null;
				this.get("options")[0].disabled = false;

				break;
			  default: 
				console.log("EntitiesDescriptor.addChild ==> Bad Child Type");
			    break;
			}			
		},
		getParent : function(){
			return this.parent;
		}
	});
	
	return Attribute;
});