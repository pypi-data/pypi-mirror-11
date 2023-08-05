define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/KeySize',
	'models/OAEPparams'
], 
function($, _, Backbone, KeySize, OAEPparams) {

	var EncryptionMethod = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "ds:EncryptionMethod",
				name : "Encryption Method",
				xml : "",
				text : "",
				childs : [null, null],
				options : [
		          {value:"xenc:KeySize", name:"Key Size", disabled : false},
		          {value:"xenc:OAEPparams", name:"OAEP params", disabled : false}
				],
				attributes : {
				  Algorithm : {name : "Algorithm", options : null,  value : "", required : true}
				}
			};
		},
		addChild : function(type){

			var node = null;
			
			switch (type) { 
			  case "xenc:KeySize":
				node = new KeySize({parent : this});
				this.get("childs")[0] = node;
				this.get("options")[0].disabled = true;
				  
			    break;
			  case "xenc:OAEPparams":
				node = new OAEPparams({parent : this});
				this.get("childs")[1] = node;
				this.get("options")[1].disabled = true;

				break;
			  default: 
				console.log("EntitiesDescriptor.addChild ==> Bad Child Type");
			    break;
			}			
			
			return node;
		},
		removeChild : function(childNode){
			switch (childNode.get("tag")) { 
			  case "xenc:KeySize":
				this.get("childs")[0] = null;
				this.get("options")[0].disabled = false;
			    break;
			  case "xenc:OAEPparams":
				this.get("childs")[1] = null;
				this.get("options")[1].disabled = false;
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
	
	return EncryptionMethod;
});