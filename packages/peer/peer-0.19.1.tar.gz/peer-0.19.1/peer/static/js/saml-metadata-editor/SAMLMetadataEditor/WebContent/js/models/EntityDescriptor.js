define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/RoleDescriptor',
	'models/IDPSSODescriptor',
	'models/SPSSODescriptor',
	'models/AuthnAuthorityDescriptor',
	'models/AttributeAuthorityDescriptor',
	'models/PDPDescriptor',
	'models/AffiliationDescriptor',
	'models/Organization',
	'models/ContactPerson',
	'models/AdditionalMetadataLocation'
], 
function($, _, Backbone, RoleDescriptor, IDPSSODescriptor, SPSSODescriptor, AuthnAuthorityDescriptor, AttributeAuthorityDescriptor, PDPDescriptor, AffiliationDescriptor, Organization, ContactPerson, AdditionalMetadataLocation) {

	var EntityDescriptor = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:EntityDescriptor",
				name : "Entity Descriptor",
				text : null,
				xml : null,
				childs : [null, null, null, null, [], []],
				options : [
		          {value:"md:Extensions", name:"Extensions", disabled : false},
		          {value:"md:RoleDescriptor", name:"Role Descriptor", disabled : false},
		          {value:"md:IDPSSODescriptor", name:"IDP SSO Descriptor", disabled : false},
		          {value:"md:SPSSODescriptor", name:"SP SSO Descriptor", disabled : false},
		          {value:"md:AuthnAuthorityDescriptor", name:"Authn Authority Descriptor", disabled : false},
		          {value:"md:AttributeAuthorityDescriptor", name:"Attribute Authority Descriptor", disabled : false},
		          {value:"md:PDPDescriptor", name:"PDP Descriptor", disabled : false},
		          {value:"md:AffiliationDescriptor", name:"Affiliation Descriptor", disabled : false},
		          {value:"md:Organization", name:"Organization", disabled : false},
		          {value:"md:ContactPerson", name:"Contact Person", disabled : false},
		          {value:"md:AdditionalMetadataLocation", name:"Additional Metadata Location", disabled : false}
				],
				attributes : {	
		          entityID : {name : "Entity ID", options : null,  value : ""},
		          validUntil: {name : "Valid Until", options : null, value : ""},
		          cacheDuration : {name : "Cache Duration", options : null, value : ""},
		          ID : {name : "ID", options : null, value : ""}
				}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};
			
			// URL validation
			var urlRegex = new RegExp("(^|\\s)((https?:\/\/)?[\\w-]+(\\.[\\w-]+)+\.?(:\\d+)?(\/\\S*)?)", "i");
			
			if(attrs.attributes.entityID.value == "")
				obj["entityID"] = "This field is required";
			else
				if(!urlRegex.test(attrs.attributes.entityID.value))
					obj["entityID"] = "This field must be a URL";
			
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
			
			
			//	Childs verification
			if(attrs.childs[1] == null || attrs.childs[1].length == 0)
				obj["childs"] = 
					"You must choose an alternative between 'Affiliation Descriptor' or any of these" + 
					"'Role Descriptor', 'IDP SSO Descriptor', 'SP SSO Descriptor', 'Descriptor authn Authority'," + 
					"'Descriptor Attribute Authority' and 'PDP Descriptor'";
								
			return obj;
		},
		addChild : function(type){

			var node = null;
			
			switch (type) { 
			  case "md:Extensions":
				  	break;
			  case "md:RoleDescriptor":
					node = new RoleDescriptor({parent : this});
					
					if(this.get("childs")[1] == null)
						this.get("childs")[1] = [];
					
					this.get("childs")[1].push(node);
					this.get("options")[7].disabled = true;
					
					break;
			  case "md:IDPSSODescriptor":
					node = new IDPSSODescriptor({parent : this});
					
					if(this.get("childs")[1] == null)
						this.get("childs")[1] = [];
					
					this.get("childs")[1].push(node);
					this.get("options")[7].disabled = true;

				    break;
			  case "md:SPSSODescriptor":
					node = new SPSSODescriptor({parent : this});
					
					if(this.get("childs")[1] == null)
						this.get("childs")[1] = [];
					
					this.get("childs")[1].push(node);
					this.get("options")[7].disabled = true;

				    break;
			  case "md:AuthnAuthorityDescriptor":
					node = new AuthnAuthorityDescriptor({parent : this});
					
					if(this.get("childs")[1] == null)
						this.get("childs")[1] = [];
					
					this.get("childs")[1].push(node);
					this.get("options")[7].disabled = true;

				    break;
			  case "md:AttributeAuthorityDescriptor":
					node = new AttributeAuthorityDescriptor({parent : this});
					
					if(this.get("childs")[1] == null)
						this.get("childs")[1] = [];
					
					this.get("childs")[1].push(node);
					this.get("options")[7].disabled = true;

				    break;
			  case "md:PDPDescriptor":
					node = new PDPDescriptor({parent : this});
					
					if(this.get("childs")[1] == null)
						this.get("childs")[1] = [];
					
					this.get("childs")[1].push(node);
					this.get("options")[7].disabled = true;

				    break;
			  case "md:AffiliationDescriptor":
					node = new AffiliationDescriptor({parent : this});
					this.get("childs")[2] = node;
					this.get("options")[1].disabled = true;
					this.get("options")[2].disabled = true;
					this.get("options")[3].disabled = true;
					this.get("options")[4].disabled = true;
					this.get("options")[5].disabled = true;
					this.get("options")[6].disabled = true;
					this.get("options")[7].disabled = true;
					
				    break;
			  case "md:Organization":
					node = new Organization({parent : this});
					this.get("childs")[3] = node;
					this.get("options")[8].disabled = true;
					
				    break;
			  case "md:ContactPerson":
					node = new ContactPerson({parent : this});
					this.get("childs")[4].push(node);
				    break;
			  case "md:AdditionalMetadataLocation":
					node = new AdditionalMetadataLocation({parent : this});
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
			  case "md:RoleDescriptor":
			  case "md:IDPSSODescriptor":
			  case "md:SPSSODescriptor":
			  case "md:AuthnAuthorityDescriptor":
			  case "md:AttributeAuthorityDescriptor":
			  case "md:PDPDescriptor":
					var collection = new Backbone.Collection(this.get("childs")[1]);
					collection.remove(childNode);
					
					if(collection.models.length > 0 ){
						this.get("childs")[1] = collection.models;
					}else{
						this.get("childs")[1] = null;
						this.get("options")[7].disabled = false;
					}

					break;
			  case "md:AffiliationDescriptor":
				  
					this.get("childs")[2] = null;

					this.get("options")[1].disabled = false;
					this.get("options")[2].disabled = false;
					this.get("options")[3].disabled = false;
					this.get("options")[4].disabled = false;
					this.get("options")[5].disabled = false;
					this.get("options")[6].disabled = false;
					this.get("options")[7].disabled = false;
				  
				    break;
			  case "md:Organization":
					this.get("childs")[3] = null;
					this.get("options")[8].disabled = false;
					
				    break;
			  case "md:ContactPerson":
					var collection = new Backbone.Collection(this.get("childs")[4]);
					collection.remove(childNode);
					
					this.get("childs")[4] = collection.models;
				  
				    break;
			  case "md:AdditionalMetadataLocation":
					var collection = new Backbone.Collection(this.get("childs")[5]);
					collection.remove(childNode);
					
					this.get("childs")[5] = collection.models;

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
	
	return EntityDescriptor;
});