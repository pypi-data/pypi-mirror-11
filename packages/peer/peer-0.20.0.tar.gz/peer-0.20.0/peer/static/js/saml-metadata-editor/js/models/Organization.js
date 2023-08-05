define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/OrganizationName',
	'models/OrganizationDisplayName',
	'models/OrganizationURL'
], 
function($, _, Backbone, OrganizationName, OrganizationDisplayName, OrganizationURL) {

	var Organization = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:Organization",
				name : "Organization",
				text : null,
				xml : null,
				childs : [null, [], [], []],
				options : [
		          {value:"md:Extensions", name:"Extensions", disabled : false},
		          {value:"md:OrganizationName", name:"Organization Name", disabled : false},
		          {value:"md:OrganizationDisplayName", name:"Organization Display Name", disabled : false},
		          {value:"md:OrganizationURL", name:"Organization URL", disabled : false}
				],
				attributes : {}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};
			
			var childs = [];
			
			//	Childs verification
			if(attrs.childs[1] == null || attrs.childs[1].length == 0)
				childs.push("Organization must have at least one Organization Name\n");
			
			if(attrs.childs[2] == null || attrs.childs[2].length == 0)
				childs.push("Organization must have at least one Organization Display Name\n");

			if(attrs.childs[3] == null || attrs.childs[3].length == 0)
				childs.push("Organization must have at least one Organization URL\n");

			if(childs.length != 0)
				obj["childs"] = childs;
			
			return obj;
		},
		addChild : function(childNode){

			var type = childNode.get("tag");
			switch (type) { 
			  case "md:Extensions":
				  	childNode.setParent(this);
					this.get("childs")[0] = childNode;
					this.get("options")[0].disabled = true;
					
				    break;
			  case "md:OrganizationName":
				  	childNode.setParent(this);
					this.get("childs")[1].push(childNode);
				    break;
				    
			  case "md:OrganizationDisplayName":
				  	childNode.setParent(this);
					this.get("childs")[2].push(childNode);
				    break;
				    
			  case "md:OrganizationURL":
				  	childNode.setParent(this);
					this.get("childs")[3].push(childNode);
				    break;
				    
			  default: 
				throw "EntitiesDescriptor.addChild ==> Bad Child Type";
			    break;
			}			
		},
		removeChild : function(childNode){
			switch (childNode.get("tag")) { 
			  case "md:Extensions":
					this.get("childs")[0] = null;
					this.get("options")[0].disabled = false;
					
				    break;
			  case "md:OrganizationName":
				var collection = new Backbone.Collection(this.get("childs")[1]);
				collection.remove(childNode);
				
				this.get("childs")[1] = collection.models;
			    break;
			  case "md:OrganizationDisplayName":
				var collection = new Backbone.Collection(this.get("childs")[2]);
				collection.remove(childNode);
				
				this.get("childs")[2] = collection.models;
			    break;
			  case "md:OrganizationURL":
				var collection = new Backbone.Collection(this.get("childs")[3]);
				collection.remove(childNode);
				
				this.get("childs")[3] = collection.models;
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
	
	return Organization;
});