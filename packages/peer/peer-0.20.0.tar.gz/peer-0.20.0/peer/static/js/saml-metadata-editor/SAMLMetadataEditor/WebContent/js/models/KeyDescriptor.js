define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/KeyInfo',
	'models/EncryptionMethod'
], 
function($, _, Backbone, KeyInfo, EncryptionMethod) {

	var types = [
     	{value:"encryption", name:"Encryption"},
    	{value:"signing", name:"Signing"}
	];
	
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
				  use : {name : "Use", options : types,  value : "", required : false}
				}
			};
		},
		addChild : function(type){

			var node = null;
			
			switch (type) { 
			  case "ds:KeyInfo":
					node = new KeyInfo({parent : this});
					this.get("childs")[0] = node;
					this.get("options")[0].disabled = true;

				  	break;
			  case "md:EncryptionMethod":
					node = new EncryptionMethod({parent : this});
					this.get("childs")[1].push(node);

					break;
			  default: 
				console.log("EntitiesDescriptor.addChild ==> Bad Child Type");
			    break;
			}			
			
			return node;
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
				console.log("EntitiesDescriptor.addChild ==> Bad Child Type");
			    break;
			}			
		},
		getParent : function(){
			return this.parent;
		}
	});
	
	return KeyDescriptor;
});