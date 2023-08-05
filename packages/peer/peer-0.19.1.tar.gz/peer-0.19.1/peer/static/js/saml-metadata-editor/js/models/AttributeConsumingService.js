define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/ServiceName',
	'models/ServiceDescription',
	'models/RequestedAttribute',
	'service/CollectionFactory'
], 
function($, _, Backbone, ServiceName, ServiceDescription, RequestedAttribute, CollectionFactory) {

	var boolean = CollectionFactory.create("boolean");

	var AttributeConsumingService = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:AttributeConsumingService",
				name : "Attribute Consuming Service",
				xml : null,
				text : null,
				childs : [[], [], []],
				options : [
				    {value:"md:ServiceName", name:"Service Name", disabled : false},
				    {value:"md:ServiceDescription", name:"Service Description", disabled : false},
				    {value:"md:RequestedAttribute", name:"Requested Attribute", disabled : false}
				],
				attributes : {
					index : {name : "Index", options : null,  value : "", required : true},
					isDefault: {name : "Is Default", options : boolean, value : boolean[0].value, required : false}
				}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};

			var numbreRegex = new RegExp("^\\d+$");
			if(attrs.attributes.index.value == "")
				obj["index"] = "This field is required";
			else
				if(attrs.attributes.index.value != "" && !numbreRegex.test(attrs.attributes.index.value))
					obj["index"] = "The value must be a unsigned short";			

			var childs = [];
			
			//	Childs verification
			if(attrs.childs[0] == null || attrs.childs[0].length == 0)
				childs.push("Attribute Consuming Service must have at least one Service Name\n");
			
			if(attrs.childs[2] == null || attrs.childs[2].length == 0)
				childs.push("Attribute Consuming Service must have at least one Requested Attribute\n");

			if(childs.length != 0)
				obj["childs"] = childs;

			return obj;
		},
		addChild : function(childNode){

			var type = childNode.get("tag");
			switch (type) { 
			  case "md:ServiceName":
				  	childNode.setParent(this);
					this.get("childs")[0].push(childNode);
				    break;

			  case "md:ServiceDescription":
				  	childNode.setParent(this);
					this.get("childs")[1].push(childNode);
				    break;

			  case "md:RequestedAttribute":
				  	childNode.setParent(this);
					this.get("childs")[2].push(childNode);
				    break;

			  default: 
				console.log("EntitiesDescriptor.addChild ==> Bad Child Type");
			    break;
			}			
		},
		removeChild : function(childNode){
			switch (childNode.get("tag")) { 
			  case "md:ServiceName":
				var collection = new Backbone.Collection(this.get("childs")[0]);
				collection.remove(childNode);
				
				this.get("childs")[0] = collection.models;

				break;
			  case "md:ServiceDescription":
				var collection = new Backbone.Collection(this.get("childs")[1]);
				collection.remove(childNode);
				
				this.get("childs")[1] = collection.models;

				break;
			  case "md:RequestedAttribute":
				var collection = new Backbone.Collection(this.get("childs")[2]);
				collection.remove(childNode);
				
				this.get("childs")[2] = collection.models;

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
	
	return AttributeConsumingService;
});