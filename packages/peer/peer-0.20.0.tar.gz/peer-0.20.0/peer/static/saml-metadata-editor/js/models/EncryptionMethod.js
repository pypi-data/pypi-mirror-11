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
				tag : "md:EncryptionMethod",
				name : "Encryption Method",
				xml : "",
				text : {options : null,  value : ""},
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
		validate: function(attrs, options) {
			
			var obj = {};
			
			// URL validation
			var urlRegex = new RegExp("^\\s?(https?:\/\/)?[\\w-]+(\\.[\\w-]+)+\.?(:\\d+)?(\/\\S*)?$", "i");
			
			if(attrs.attributes.Algorithm.value == "")
				obj["Algorithm"] = "This field is required";
			else
				if(!urlRegex.test(attrs.attributes.Algorithm.value))
					obj["Algorithm"] = "This field must be a URL";
			
			return obj;
		},
		addChild : function(childNode){

			var type = childNode.get("tag");
			switch (type) { 
			  case "xenc:KeySize":
				  	childNode.setParent(this);
					this.get("childs")[0] = childNode;
					this.get("options")[0].disabled = true;
					break;
					
			  case "xenc:OAEPparams":
				  	childNode.setParent(this);
					this.get("childs")[1] = childNode;
					this.get("options")[1].disabled = true;
					break;
					
			  default: 
				throw "EntitiesDescriptor.addChild ==> Bad Child Type";
			    break;
			}			
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
	
	return EncryptionMethod;
});