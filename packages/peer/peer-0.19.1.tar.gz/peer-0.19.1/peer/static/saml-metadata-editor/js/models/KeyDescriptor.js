define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/KeyInfo',
	'models/EncryptionMethod',
	'service/CollectionFactory'
], 
function($, _, Backbone, KeyInfo, EncryptionMethod, CollectionFactory) {

	var useTypes = CollectionFactory.create("useTypes");
	
	var KeyDescriptor = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:KeyDescriptor",
				name : "Key Descriptor",
				text : null,
				xml : null,
				childs : [null, []],
				options : [
		          {value:"ds:KeyInfo", name:"Key Info", disabled : false},
		          {value:"md:EncryptionMethod", name:"Encryption Method", disabled : false}
				],
				attributes : {	
				  use : {name : "Use", options : useTypes,  value : useTypes[0].value, required : false}
				}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};
			
			var childs = [];
			
			if(attrs.childs[0] == null || attrs.childs[0].length == 0)
				childs.push("Key Descriptor must have at least one Key Info\n");

			if(childs.length != 0)
				obj["childs"] = childs;
			
			return obj;
		},
		addChild : function(childNode){

			var type = childNode.get("tag");
			switch (type) { 
			  case "ds:KeyInfo":
				  	childNode.setParent(this);
					this.get("childs")[0] = childNode;
					this.get("options")[0].disabled = true;

				  	break;
			  case "md:EncryptionMethod":
				  	childNode.setParent(this);
					this.get("childs")[1].push(childNode);
				    break;
			  default: 
				throw "EntitiesDescriptor.addChild ==> Bad Child Type";
			    break;
			}			
		},
		removeChild : function(childNode){
			switch (childNode.get("tag")) { 
			  case "ds:KeyInfo":
					this.get("childs")[0] = null;
					this.get("options")[0].disabled = false;

					break;
			  case "md:EncryptionMethod":
					var collection = new Backbone.Collection(this.get("childs")[1]);
					collection.remove(childNode);
					
					this.get("childs")[1] = collection.models;
					
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
	
	return KeyDescriptor;
});