define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/AffiliateMember',
	'models/KeyDescriptor'
], 
function($, _, Backbone, AffiliateMember, KeyDescriptor) {

	var AffiliationDescriptor = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:AffiliationDescriptor",
				name : "Affiliation Descriptor",
				text : null,
				xml : null,
				childs : [null, [], []],
				options : [
		          {value:"md:Extensions", name:"Extensions", disabled : false},
		          {value:"md:AffiliateMember", name:"Affiliate Member", disabled : false},
		          {value:"md:KeyDescriptor", name:"Key Descriptor", disabled : false}
				],
				attributes : {	
				  affiliationOwnerID : {name : "Affiliation Owner ID", options : null,  value : "", required : true},
		          validUntil: {name : "Valid Until", options : null, value : "", required : false},
		          cacheDuration : {name : "Cache Duration", options : null, value : "", required : false},
		          ID : {name : "ID", options : null, value : "", required : false}
				}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};
			
			// field Validation
			var urlRegex = new RegExp("(^|\\s)((https?:\/\/)?[\\w-]+(\\.[\\w-]+)+\.?(:\\d+)?(\/\\S*)?)", "i");
			
			if(attrs.attributes.affiliationOwnerID.value == "")
				obj["affiliationOwnerID"] = "This field is required";
			else
				if(!urlRegex.test(attrs.attributes.affiliationOwnerID.value))
					obj["affiliationOwnerID"] = "This field must be a URL";

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
			obj["childs"] = "";
			if(attrs.childs[1] == null || attrs.childs[1].length == 0)
				obj["childs"] += "· Affiliation Descriptor must have at least one Affiliate Member\n";
			
			return obj;
		},
		addChild : function(type){

			var node = null;
			
			switch (type) { 
			  case "md:Extensions":
				  	break;
			  case "md:AffiliateMember":
					node = new AffiliateMember({parent : this});
					this.get("childs")[1].push(node);
				    break;
			  case "md:KeyDescriptor":
					node = new KeyDescriptor({parent : this});
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
				  	break;
			  case "md:AffiliateMember":
					var collection = new Backbone.Collection(this.get("childs")[2]);
					collection.remove(childNode);
					
					this.get("childs")[1] = collection.models;

					break;
			  case "md:KeyDescriptor":
					var collection = new Backbone.Collection(this.get("childs")[3]);
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
	
	return AffiliationDescriptor;
});