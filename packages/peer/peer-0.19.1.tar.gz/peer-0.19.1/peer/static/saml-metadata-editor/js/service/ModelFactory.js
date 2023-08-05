define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'models/AdditionalMetadataLocation',
	'models/AffiliateMember',
	'models/AffiliationDescriptor',
	'models/ArtifactResolutionService',
	'models/AssertionConsumerService',
	'models/AssertionIDRequestService',
	'models/Attribute',
	'models/AttributeAuthorityDescriptor',
	'models/AttributeConsumingService',
	'models/AttributeProfile',
	'models/AttributeService',
	'models/AttributeValue',
	'models/AuthnAuthorityDescriptor',
	'models/AuthnQueryService',
	'models/AuthzService',
	'models/Company',
	'models/ContactPerson',
	'models/EmailAddress',
	'models/EncryptionMethod',
	'models/EntitiesDescriptor',
	'models/EntityDescriptor',
	'models/Extensions',
	'models/GivenName',
	'models/IDPSSODescriptor',
	'models/KeyDescriptor',
	'models/KeyInfo',	
	'models/KeySize',	
	'models/ManageNameIDService',	
	'models/NameIDFormat',	
	'models/NameIDMappingService',	
	'models/OAEPparams',	
	'models/Organization',	
	'models/OrganizationDisplayName',	
	'models/OrganizationName',	
	'models/OrganizationURL',	
	'models/PDPDescriptor',	
	'models/RequestedAttribute',	
	'models/RoleDescriptor',	
	'models/ServiceDescription',	
	'models/ServiceName',	
	'models/SingleLogoutService',	
	'models/SingleSignOnService',	
	'models/SPSSODescriptor',	
	'models/SurName',	
	'models/SPSSODescriptor',	
	'models/TelephoneNumber'	
], 
function($, _, Backbone,
		AdditionalMetadataLocation,	AffiliateMember, AffiliationDescriptor, ArtifactResolutionService, AssertionConsumerService,
		AssertionIDRequestService, Attribute, AttributeAuthorityDescriptor, AttributeConsumingService, AttributeProfile,
		AttributeService, AttributeValue, AuthnAuthorityDescriptor,	AuthnQueryService, AuthzService, Company, ContactPerson,
		EmailAddress, EncryptionMethod, EntitiesDescriptor, EntityDescriptor, Extensions, GivenName, IDPSSODescriptor, KeyDescriptor,
		KeyInfo, KeySize, ManageNameIDService, NameIDFormat, NameIDMappingService, OAEPparams, Organization, OrganizationDisplayName,	
		OrganizationName, OrganizationURL, PDPDescriptor, RequestedAttribute, RoleDescriptor, ServiceDescription, ServiceName,	
		SingleLogoutService, SingleSignOnService, SPSSODescriptor, SurName, SPSSODescriptor, TelephoneNumber) {
	
	var create = function(type){
		var node = null;
		
		switch (type) { 
		  case "md:AdditionalMetadataLocation":
				node = new AdditionalMetadataLocation();
			    break;
		  case "md:AffiliateMember":
				node = new AffiliateMember();
			    break;
		  case "md:AffiliationDescriptor":
				node = new AffiliationDescriptor();
			    break;
		  case "md:ArtifactResolutionService":
				node = new ArtifactResolutionService();
			    break;
		  case "md:AssertionConsumerService":
				node = new AssertionConsumerService();
			    break;
		  case "md:AssertionIDRequestService":
				node = new AssertionIDRequestService();
			    break;
		  case "saml:Attribute":
				node = new Attribute();
			    break;
		  case "md:AttributeAuthorityDescriptor":
				node = new AttributeAuthorityDescriptor();
			    break;
		  case "md:AttributeConsumingService":
				node = new AttributeConsumingService();
			    break;
		  case "md:AttributeProfile":
				node = new AttributeProfile();
			    break;
		  case "md:AttributeService":
				node = new AttributeService();
			    break;
		  case "saml:AttributeValue":
				node = new AttributeValue();
			    break;
		  case "md:AuthnAuthorityDescriptor":
				node = new AuthnAuthorityDescriptor();
			    break;
		  case "md:AuthnQueryService":
				node = new AuthnQueryService();
			    break;
		  case "md:AuthzService":
				node = new AuthzService();
			    break;
		  case "md:Company":
				node = new Company();
			    break;
		  case "md:ContactPerson":
				node = new ContactPerson();
			    break;
		  case "md:EmailAddress":
				node = new EmailAddress();
			    break;
		  case "md:EncryptionMethod":
				node = new EncryptionMethod();
			    break;
		  case "md:EntitiesDescriptor":
				node = new EntitiesDescriptor();
			    break;
		  case "md:EntityDescriptor":
				node = new EntityDescriptor();
			    break;
		  case "md:Extensions":
				node = new Extensions();
			    break;
		  case "md:GivenName":
				node = new GivenName();
			    break;
		  case "md:IDPSSODescriptor":
				node = new IDPSSODescriptor();
			    break;
		  case "md:KeyDescriptor":
				node = new KeyDescriptor();
			    break;
		  case "ds:KeyInfo":
				node = new KeyInfo();
			    break;
		  case "xenc:KeySize":
				node = new KeySize();
			    break;
		  case "md:ManageNameIDService":
				node = new ManageNameIDService();
			    break;
		  case "md:NameIDFormat":
				node = new NameIDFormat();
			    break;
		  case "md:NameIDMappingService":
				node = new NameIDMappingService();
			    break;
		  case "xenc:OAEPparams":
				node = new OAEPparams();
			    break;
		  case "md:Organization":
				node = new Organization();
			    break;
		  case "md:OrganizationDisplayName":
				node = new OrganizationDisplayName();
			    break;
		  case "md:OrganizationName":
				node = new OrganizationName();
			    break;
		  case "md:OrganizationURL":
				node = new OrganizationURL();
			    break;
		  case "md:PDPDescriptor":
				node = new PDPDescriptor();
			    break;
		  case "md:RequestedAttribute":
				node = new RequestedAttribute();
			    break;
		  case "md:RoleDescriptor":
				node = new RoleDescriptor();
			    break;
		  case "md:ServiceDescription":
				node = new ServiceDescription();
			    break;
		  case "md:ServiceName":
				node = new ServiceName();
			    break;
		  case "md:SingleLogoutService":
				node = new SingleLogoutService();
			    break;
		  case "md:SingleSignOnService":
				node = new SingleSignOnService();
			    break;
		  case "md:SPSSODescriptor":
				node = new SPSSODescriptor();
			    break;
		  case "md:SurName":
				node = new SurName();
			    break;
		  case "md:TelephoneNumber":
				node = new TelephoneNumber();
			    break;
		  default: 
			throw "ModelFactory.create ==> Bad Child Type : " + type;
		    break;
		}			
		
		return node;

	};

	
	return {
		create : create
	};
});