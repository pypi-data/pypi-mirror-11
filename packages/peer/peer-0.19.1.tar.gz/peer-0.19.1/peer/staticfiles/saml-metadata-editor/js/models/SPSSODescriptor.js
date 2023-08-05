define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/KeyDescriptor',
	'models/Organization',
	'models/ContactPerson',
	'models/ArtifactResolutionService',
	'models/SingleLogoutService',
	'models/ManageNameIDService',
	'models/NameIDFormat',
	'models/AssertionConsumerService',
	'models/AttributeConsumingService',
	'service/CollectionFactory'
], 
function($, _, Backbone, KeyDescriptor, Organization, ContactPerson, ArtifactResolutionService, SingleLogoutService, ManageNameIDService, NameIDFormat, AssertionConsumerService, AttributeConsumingService, CollectionFactory) {

	var boolean = CollectionFactory.create("boolean");
	
	var SPSSODescriptor = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:SPSSODescriptor",
				name : "SPS SO Descriptor",
				text : null,
				xml : null,
				childs : [null, [], null, [], [], [], [], [], [], []],
				options : [
		          {value:"md:Extensions", name:"Extensions", disabled : false},
		          {value:"md:KeyDescriptor", name:"Key Descriptor", disabled : false},
		          {value:"md:Organization", name:"Organization", disabled : false},
		          {value:"md:ContactPerson", name:"ContactPerson", disabled : false},
		          {value:"md:ArtifactResolutionService", name:"Artifact Resolution Service", disabled : false},
		          {value:"md:SingleLogoutService", name:"Single Logout Service", disabled : false},
		          {value:"md:ManageNameIDService", name:"Manage Name ID Service", disabled : false},
		          {value:"md:NameIDFormat", name:"Name ID Format", disabled : false},
		          {value:"md:AssertionConsumerService", name:"Assertion Consumer Service", disabled : false},
		          {value:"md:AttributeConsumingService", name:"Attribute Consuming Service", disabled : false}
				],
				attributes : {
				  ID : {name : "ID", options : null,  value : "", required : false},
		          validUntil : {name : "Valid Until", options : null, value : "", required : false},
		          cacheDuration : {name : "Cache Duration", options : null, value : "", required : false},
		          protocolSupportEnumeration : {name : "Protocol Support Enumeration", options : null, value : "urn:oasis:names:tc:SAML:2.0:protocol", required : true},
		          errorURL : {name : "Error URL", options : null, value : "", required : false},
		          AuthnRequestsSigned : {name : "Authn Requests Signed", options : boolean, value : boolean[0].value, required : false},
		          WantAuthnRequestsSigned : {name : "Want Authn Requests Signed", options : boolean, value : boolean[0].value, required : false}
				}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};

			// URL validation
			var listUrlRegex = new RegExp("^(\\s?(https?:\/\/)?[\\w-]+(\\.[\\w-]+)+\.?(:\\d+)?(\/\\S*)?)+$", "i");

			if(attrs.attributes.protocolSupportEnumeration.value == "")
				obj["protocolSupportEnumeration"] = "This field is required";

			// URL validation
			var urlRegex = new RegExp("^\\s?(https?:\/\/)?[\\w-]+(\\.[\\w-]+)+\.?(:\\d+)?(\/\\S*)?$", "i");
			
			if(attrs.attributes.errorURL.value != "" && !urlRegex.test(attrs.attributes.errorURL.value))
				obj["errorURL"] = "This field must be a URL";

			//	UTC validation
			var utcRegex = new RegExp("\\d{4}-[01]\\d-[0-3]\\dT[0-2]\\d:[0-5]\\d:[0-5]\\d(\\.\\d{1,3})?([+-][0-2]\\d:[0-5]\\d|Z)?");
			
			if(	attrs.attributes.validUntil.value != "" && !utcRegex.test(attrs.attributes.validUntil.value))
				obj["validUntil"] = "This field must be a UTC Date";
			
			//	Duration validation
			var durationRegex = new RegExp(
					"^P(\\d{1,4}Y|\\d{1,2}M|\\d{1,2}D)$|"+
					"^P\\d{1,4}Y\\d{1,2}M$|"+
					"^P\\d{1,4}Y\\d{1,2}D$|"+
					"^P\\d{1,2}M\\d{1,2}D$|"+
					"^P\\d{1,4}Y\\d{1,2}M\\d{1,2}D$|"+
					"^PT([0-2]?\\dH|[0-5]?\\dM|[0-5]\\d(.[0-5]\\d)?S)$|"+
					"^PT[0-2]?\\dH[0-5]?\\dM$|"+
					"^PT[0-2]?\\dH[0-5]\\d(.[0-5]\\d)?S$|"+
					"^PT[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$|"+
					"^PT[0-2]?\\dH[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P(\\d{1,4}Y|\\d{1,2}M|\\d{1,2}D)T([0-2]?\\dH|[0-5]?\\dM|[0-5]\\d(.[0-5]\\d)?S)$|"+
					"^P(\\d{1,4}Y|\\d{1,2}M|\\d{1,2}D)T[0-2]?\\dH[0-5]?\\dM$|"+
					"^P(\\d{1,4}Y|\\d{1,2}M|\\d{1,2}D)T[0-2]?\\dH[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P(\\d{1,4}Y|\\d{1,2}M|\\d{1,2}D)T[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P(\\d{1,4}Y|\\d{1,2}M|\\d{1,2}D)T[0-2]?\\dH[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,4}Y\\d{1,2}MT([0-2]?\\dH|[0-5]?\\dM|[0-5]\\d(.[0-5]\\d)?S)$|"+
					"^P\\d{1,4}Y\\d{1,2}MT[0-2]?\\dH[0-5]?\\dM$|"+
					"^P\\d{1,4}Y\\d{1,2}MT[0-2]?\\dH[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,4}Y\\d{1,2}MT[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,4}Y\\d{1,2}MT[0-2]?\\dH[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,4}Y\\d{1,2}DT([0-2]?\\dH|[0-5]?\\dM|[0-5]\\d(.[0-5]\\d)?S)$|"+
					"^P\\d{1,4}Y\\d{1,2}DT[0-2]?\\dH[0-5]?\\dM$|"+
					"^P\\d{1,4}Y\\d{1,2}DT[0-2]?\\dH[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,4}Y\\d{1,2}DT[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,4}Y\\d{1,2}DT[0-2]?\\dH[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,2}M\\d{1,2}DT([0-2]?\\dH|[0-5]?\\dM|[0-5]\\d(.[0-5]\\d)?S)$|"+
					"^P\\d{1,2}M\\d{1,2}DT[0-2]?\\dH[0-5]?\\dM$|"+
					"^P\\d{1,2}M\\d{1,2}DT[0-2]?\\dH[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,2}M\\d{1,2}DT[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,2}M\\d{1,2}DT[0-2]?\\dH[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,4}Y\\d{1,2}M\\d{1,2}DT([0-2]?\\dH|[0-5]?\\dM|[0-5]\\d(.[0-5]\\d)?S)$|"+
					"^P\\d{1,4}Y\\d{1,2}M\\d{1,2}DT[0-2]?\\dH[0-5]?\\dM$|"+
					"^P\\d{1,4}Y\\d{1,2}M\\d{1,2}DT[0-2]?\\dH[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,4}Y\\d{1,2}M\\d{1,2}DT[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$|"+
					"^P\\d{1,4}Y\\d{1,2}M\\d{1,2}DT[0-2]?\\dH[0-5]?\\dM[0-5]\\d(.[0-5]\\d)?S$");
			
			if(	attrs.attributes.cacheDuration.value != "" && !durationRegex.test(attrs.attributes.cacheDuration.value))
					obj["cacheDuration"] = "This field must be a duration type";
			
			var childs = [];
			
			//	Childs verification
			if(attrs.childs[8] == null || attrs.childs[8].length == 0)
				childs.push("SP SSO Descriptor must have at least one Assertion Consumer Service\n");

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
			  case "md:KeyDescriptor":
				  	childNode.setParent(this);
					this.get("childs")[1].push(childNode);
				    break;
				    
			  case "md:Organization":
				  	childNode.setParent(this);
					this.get("childs")[2] = childNode;
					this.get("options")[2].disabled = true;					
				    break;
				    
			  case "md:ContactPerson":
				  	childNode.setParent(this);
					this.get("childs")[3].push(childNode);
				    break;
				    
			  case "md:ArtifactResolutionService":
				  	childNode.setParent(this);
					this.get("childs")[4].push(childNode);
				    break;
				    
			  case "md:SingleLogoutService":
				  	childNode.setParent(this);
					this.get("childs")[5].push(childNode);
				    break;
				    
			  case "md:ManageNameIDService":
				  	childNode.setParent(this);
					this.get("childs")[6].push(childNode);
				    break;
				    
			  case "md:NameIDFormat":
				  	childNode.setParent(this);
					this.get("childs")[7].push(childNode);
				    break;
				    
			  case "md:AssertionConsumerService":
				  	childNode.setParent(this);
					this.get("childs")[8].push(childNode);
				    break;
				    
			  case "md:AttributeConsumingService":
				  	childNode.setParent(this);
					this.get("childs")[9].push(childNode);
				    break;
				    
			  default: 
				console.log("EntitiesDescriptor.addChild ==> Bad Child Type");
			    break;
			}			
		},
		removeChild : function(childNode){
			switch (childNode.get("tag")) { 
			  case "md:Extensions":
					this.get("childs")[0] = null;
					this.get("options")[0].disabled = false;
					
				    break;
			  case "md:KeyDescriptor":
				var collection = new Backbone.Collection(this.get("childs")[1]);
				collection.remove(childNode);
				
				this.get("childs")[1] = collection.models;
			  case "md:Organization":
				this.get("childs")[2] = null;
				this.get("options")[2].disabled = false;
				
			    break;
			  case "md:ContactPerson":
				var collection = new Backbone.Collection(this.get("childs")[3]);
				collection.remove(childNode);
				
				this.get("childs")[3] = collection.models;
				
			    break;
			  case "md:ArtifactResolutionService":
				var collection = new Backbone.Collection(this.get("childs")[4]);
				collection.remove(childNode);
				
				this.get("childs")[4] = collection.models;
				
			    break;
			  case "md:SingleLogoutService":
				var collection = new Backbone.Collection(this.get("childs")[5]);
				collection.remove(childNode);
				
				this.get("childs")[5] = collection.models;
				
			    break;
			  case "md:ManageNameIDService":
				var collection = new Backbone.Collection(this.get("childs")[6]);
				collection.remove(childNode);
				
				this.get("childs")[6] = collection.models;
				
			    break;
			  case "md:NameIDFormat":
				var collection = new Backbone.Collection(this.get("childs")[7]);
				collection.remove(childNode);
				
				this.get("childs")[7] = collection.models;
				
			    break;
			  case "md:AssertionConsumerService":
				var collection = new Backbone.Collection(this.get("childs")[8]);
				collection.remove(childNode);
				
				this.get("childs")[8] = collection.models;
			    break;
			  case "md:AttributeConsumingService":
				var collection = new Backbone.Collection(this.get("childs")[9]);
				collection.remove(childNode);
				
				this.get("childs")[9] = collection.models;
			    break;
			  default: 
				throw "EntitiesDescriptor.addChild ==> Bad Child Type";
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
	
	return SPSSODescriptor;
});