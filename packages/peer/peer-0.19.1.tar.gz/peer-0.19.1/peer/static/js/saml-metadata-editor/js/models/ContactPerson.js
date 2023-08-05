define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/Company',
	'models/GivenName',
	'models/SurName',
	'models/EmailAddress',
	'models/TelephoneNumber',
	'service/CollectionFactory'
], 
function($, _, Backbone, Company, GivenName, SurName, EmailAddress, TelephoneNumber, CollectionFactory) {

	var contactType = CollectionFactory.create("contactTypes");           	

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
				  contactType : {name : "Contact Type", options : contactType,  value : contactType[0].value, required : true}
				}
			};
		},
		addChild : function(childNode){

			var type = childNode.get("tag");
			switch (type) { 
			  case "md:Extensions":
				  	childNode.setParent(this);
					this.get("childs")[0] = childNode;
					this.get("options")[0].disabled = true;
					
				    break;
			  case "md:Company":
				  	childNode.setParent(this);
					this.get("childs")[1] = childNode;
					this.get("options")[1].disabled = true;
					
					break;
			  case "md:GivenName":
				  	childNode.setParent(this);
					this.get("childs")[2] = childNode;
					this.get("options")[2].disabled = true;
					
				    break;
			  case "md:SurName":
				  	childNode.setParent(this);
					this.get("childs")[3] = childNode;
					this.get("options")[3].disabled = true;

					break;
			  case "md:EmailAddress":
				  	childNode.setParent(this);
					this.get("childs")[4].push(childNode);
				    break;

			  case "md:TelephoneNumber":
				  	childNode.setParent(this);
					this.get("childs")[5].push(childNode);
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
	
	return ContactPerson;
});