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
			
			obj["childs"] = "";
			
			//	Childs verification
			if(attrs.childs[1] == null || attrs.childs[1].length == 0)
				obj["childs"] += "· Organization must have at least one Organization Name\n";
			
			if(attrs.childs[2] == null || attrs.childs[2].length == 0)
				obj["childs"] += "· Organization must have at least one Organization Display Name\n";

			if(attrs.childs[3] == null || attrs.childs[3].length == 0)
				obj["childs"] += "· Organization must have at least one Organization URL\n";

			return obj;
		},
		addChild : function(type){

			var node = null;
			
			switch (type) { 
			  case "md:Extensions":
			    break;
			  case "md:OrganizationName":
				node = new OrganizationName({parent : this});
				this.get("childs")[1].push(node);
			    break;
			  case "md:OrganizationDisplayName":
				node = new OrganizationDisplayName({parent : this});
				this.get("childs")[2].push(node);
			    break;
			  case "md:OrganizationURL":
				node = new OrganizationURL({parent : this});
				this.get("childs")[3].push(node);
			    break;
			  default: 
				console.log("EntitiesDescriptor.addChild ==> Bad Child Type");
			    break;
			}			
			
			return node;
		},
		removeChild : function(childNode){
			switch (childNode.get("tag")) { 
			  case "md:Extensions":
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
				console.log("EntitiesDescriptor.addChild ==> Bad Child Type");
			    break;
			}			
		},
		getParent : function(){
			return this.parent;
		}
	});
	
	return Organization;
});