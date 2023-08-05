define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/ServiceName',
	'models/ServiceDescription',
	'models/RequestedAttribute'
], 
function($, _, Backbone, ServiceName, ServiceDescription, RequestedAttribute) {

	var options = [
       	{value:"true", name:"True"},
       	{value:"false", name:"False"}
   	];

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
					isDefault: {name : "Is Default", options : options, value : "", required : false}
				}
			};
		},
		addChild : function(type){

			var node = null;
			
			switch (type) { 
			  case "md:ServiceName":
				node = new ServiceName({parent : this});
				this.get("childs")[0].push(node);

				break;
			  case "md:ServiceDescription":
				node = new ServiceDescription({parent : this});
				this.get("childs")[1].push(node);

				break;
			  case "md:RequestedAttribute":
				node = new RequestedAttribute({parent : this});
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
				console.log("EntitiesDescriptor.addChild ==> Bad Child Type");
			    break;
			}			
		},
		getParent : function(){
			return this.parent;
		}
	});
	
	return AttributeConsumingService;
});