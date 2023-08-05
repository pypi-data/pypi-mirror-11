define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/AttributeValue',
	'service/CollectionFactory'
], 
function($, _, Backbone, AttributeValue, CollectionFactory) {

	var boolean = CollectionFactory.create("boolean");
	var attributeFormat =  CollectionFactory.create("attributeFormat");
	var attributes = CollectionFactory.create("attributes");
	
	var RequestedAttribute = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:RequestedAttribute",
				name : "Requested Attribute",
				xml : null,
				text : null,
				childs : [[]],
				options : [
				    {value:"saml:AttributeValue", name:"AttributeValue", disabled : false}
				],
				attributes : {
					Name : {name : "Name", options : attributes,  value : attributes[0].value, required : true},
					NameFormat: {name : "NameFormat", options : attributeFormat, value : attributeFormat[0].value, required : false},
					FriendlyName : {name : "Friendly Name", options : null, value : "", required : false},
					isRequired : {name : "Is required", options : boolean, value : boolean[0].value, required : false}
				}
			};
		},
		addChild : function(childNode){

			var type = childNode.get("tag");
			switch (type) { 
			  case "saml:AttributeValue":
				  	childNode.setParent(this);
					this.get("childs")[0].push(childNode);
				    break;

			  default: 
				throw "EntitiesDescriptor.addChild ==> Bad Child Type";
			    break;
			}			
		},
		removeChild : function(childNode){
			switch (childNode.get("tag")) { 
			  case "saml:AttributeValue":
					var collection = new Backbone.Collection(this.get("childs")[0]);
					collection.remove(childNode);
					
					this.get("childs")[0] = collection.models;
					break;
					
			  default: 
				throw "EntitiesDescriptor.removeChild ==> Bad Child Type";
			    break;
			}			
		},
		getParent : function(){
			return this.parent;
		},
		setParent : function(parent){
			this.parent = parent;
		}
	});
	
	return RequestedAttribute;
});