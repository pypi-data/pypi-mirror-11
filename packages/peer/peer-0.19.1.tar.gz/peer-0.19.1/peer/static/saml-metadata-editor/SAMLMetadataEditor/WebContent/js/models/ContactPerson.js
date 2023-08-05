define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/Company',
	'models/GivenName',
	'models/SurName',
	'models/EmailAddress',
	'models/TelephoneNumber'
], 
function($, _, Backbone, Company, GivenName, SurName, EmailAddress, TelephoneNumber) {

	var contactType = [
		{value:"administrative", name:"Administrative"},
		{value:"technical", name:"Technical"},
		{value:"support", name:"Support"},
		{value:"billing", name:"Billing"},
		{value:"other", name:"Other"}
   ];           	

	var ContactPerson = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:ContactPerson",
				name : "Contact Person",
				text : null,
				xml : null,
				childs : [null, null, null, null, [],[]],
				options : [
		          {value:"md:Extensions", name:"Extensions", disabled : false},
		          {value:"md:Company", name:"Company", disabled : false},
		          {value:"md:GivenName", name:"Given Name", disabled : false},
		          {value:"md:SurName", name:"SurName", disabled : false},
		          {value:"md:EmailAddress", name:"Email Address", disabled : false},
		          {value:"md:TelephoneNumber", name:"Telephone Number", disabled : false}
				],
				attributes : {
				  contactType : {name : "Contact Type", options : contactType,  value : contactType[0], required : true}
				}
			};
		},
		addChild : function(type){

			var node = null;
			
			switch (type) { 
			  case "md:Extensions":
				  	break;
			  case "md:Company":
				  	var node = new Company({parent : this});
					this.get("childs")[1] = node;
					this.get("options")[1].disabled = true;
					
					break;
			  case "md:GivenName":
				  	var node = new GivenName({parent : this});
					this.get("childs")[2] = node;
					this.get("options")[2].disabled = true;
					
				    break;
			  case "md:SurName":
				  	var node = new SurName({parent : this});
					this.get("childs")[3] = node;
					this.get("options")[3].disabled = true;

					break;
			  case "md:EmailAddress":
					node = new EmailAddress({parent : this});
					this.get("childs")[4].push(node);

					break;
			  case "md:TelephoneNumber":
					node = new TelephoneNumber({parent : this});
					this.get("childs")[5].push(node);

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
			  case "md:Company":
					this.get("childs")[1] = null;
					this.get("options")[1].disabled = false;
					
					break;
			  case "md:GivenName":
					this.get("childs")[2] = null;
					this.get("options")[2].disabled = false;
					
					break;
			  case "md:SurName":
					this.get("childs")[3] = null;
					this.get("options")[3].disabled = false;

					break;
			  case "md:EmailAddress":
					var collection = new Backbone.Collection(this.get("childs")[4]);
					collection.remove(childNode);
					break;
			  case "md:TelephoneNumber":
					var collection = new Backbone.Collection(this.get("childs")[5]);
					collection.remove(childNode);
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
	
	return ContactPerson;
});