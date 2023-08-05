define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/EntityDescriptor'
], 
function($, _, Backbone, EntityDescriptor) {

	var EntitiesDescriptor = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:EntitiesDescriptor",
				name : "Entities Descriptor",
				text : null,
				xml : null,
				childs : [null, null, []],
				options : [
		          {value:"md:Extensions", name:"Extensions", disabled : false},
		          {value:"md:EntitiesDescriptor", name:"Entities Descriptor", disabled : false},
		          {value:"md:EntityDescriptor", name:"Entity Descriptor", disabled : false}
				],
				attributes : {
		          Name : {name : "Name", options : null,  value : "", required : true},
		          validUntil : {name : "Valid Until", options : null, value : "", required : false},
		          cacheDuration : {name : "Cache Duration", options : null, value : "", required : false},
		          ID : {name : "ID", options : null, value : "", required : false}
				}
			};
		},
		addChild : function(type){

			var node = null;
			
			switch (type) { 
			  case "md:Extensions":
			    break;
			  case "md:EntitiesDescriptor":
				node = new EntitiesDescriptor({parent : this});
				this.get("childs")[2].push(node);
			    break;
			  case "md:EntityDescriptor":
				node = new EntityDescriptor({parent : this});
				this.get("childs")[2].push(node);
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
				this.get("childs")[1] = null;
			    break;
			  case "md:EntitiesDescriptor":
			  case "md:EntityDescriptor":
				var collection = new Backbone.Collection(this.get("childs")[2]);
				collection.remove(childNode);
				
				this.get("childs")[2] = collection.models;

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
	
	return EntitiesDescriptor;
});