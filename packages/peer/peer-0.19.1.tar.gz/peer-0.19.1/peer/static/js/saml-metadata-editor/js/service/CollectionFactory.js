define(
[ 
	'jquery', 
	'underscore', 
	'backbone'
], 
function($, _, Backbone) {
	
	var create = function(type){
		var collection = null;
		
		switch (type) { 
		  case "bindings":
			  collection = [
	               	{value:"urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect", name:"HTTP Redirect"},
	               	{value:"urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST", name:"HTTP POST"},
	               	{value:"urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Artifact", name:"HTTP Artifact"},
	               	{value:"urn:oasis:names:tc:SAML:2.0:bindings:SOAP", name:"SOAP"},
	               	{value:"urn:oasis:names:tc:SAML:2.0:bindings:PAOS", name:"Reverse SOAP (PAOS)"},
	              	{value:"urn:oasis:names:tc:SAML:2.0:bindings:URI", name:"URI"}			  
			  ];
			  
			  break;
		  case "boolean":
			  collection = [
	               	{value:"true", name:"True"},
	               	{value:"false", name:"False"}
			  ];

		  case "attributeFormat":
			  collection = [
	                {value:"urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified", name:"unspecified"},
	             	{value:"urn:oasis:names:tc:SAML:2.0:attrname-format:uri", name:"uri"},
	             	{value:"urn:oasis:names:tc:SAML:2.0:attrname-format:basic", name:"basic"}
			  ];
			  
			  break;
		  case "attributes":
			  collection = [
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.1-id", name:"​uid​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.10-id", name:"​manager​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.2-id", name:"​textEncodedORAddress​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.20-id", name:"​homePhone​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.22-id", name:"​otherMailbox​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.3-id", name:"​mail​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.39-id", name:"​homePostalAddress​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.40-id", name:"​personalTitle​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.41-id", name:"​mobile​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.42-id", name:"​pager​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.43-id", name:"​co​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.6-id", name:"​roomNumber​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.60-id", name:"​jpegPhoto​"},
	          		{value:"urn:​oid:​0.9.2342.19200300.100.1.7-id", name:"​photo​"},
	          		{value:"urn:​oid:​1.2.840.113549.1.9.1-id", name:"​email​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.2428.90.1.1-id", name:"​norEduOrgUniqueNumber​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.2428.90.1.11-id", name:"​norEduOrgSchemaVersion​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.2428.90.1.12-id", name:"​norEduOrgNIN​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.2428.90.1.2-id", name:"​norEduOrgUnitUniqueNumber​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.2428.90.1.3-id", name:"​norEduPersonBirthDate​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.2428.90.1.4-id", name:"​norEduPersonLIN​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.2428.90.1.5-id", name:"​norEduPersonNIN​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.2428.90.1.6-id", name:"​norEduOrgAcronym​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.2428.90.1.7-id", name:"​norEduOrgUniqueIdentifier​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.2428.90.1.8-id", name:"​norEduOrgUnitUniqueIdentifier​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.2428.90.1.9-id", name:"​federationFeideSchemaVersion​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.250.1.57-id", name:"​labeledURI​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.1.1.1-id", name:"​eduPersonAffiliation​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.1.1.10-id", name:"​eduPersonTargetedID​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.1.1.2-id", name:"​eduPersonNickname​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.1.1.3-id", name:"​eduPersonOrgDN​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.1.1.4-id", name:"​eduPersonOrgUnitDN​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.1.1.5-id", name:"​eduPersonPrimaryAffiliation​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.1.1.6-id", name:"​eduPersonPrincipalName​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.1.1.7-id", name:"​eduPersonEntitlement​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.1.1.8-id", name:"​eduPersonPrimaryOrgUnitDN​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.1.1.9-id", name:"​eduPersonScopedAffiliation​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.2.1.2-id", name:"​eduOrgHomePageURI​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.2.1.3-id", name:"​eduOrgIdentityAuthNPolicyURI​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.2.1.4-id", name:"​eduOrgLegalName​" },
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.2.1.5-id", name:"​eduOrgSuperiorURI​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.2.1.6-id", name:"​eduOrgWhitePagesURI​"},
	          		{value:"urn:​oid:​1.3.6.1.4.1.5923.1.5.1.1-id", name:"​isMemberOf​"},
	          		{value:"urn:​oid:​2.16.840.1.113730.3.1.241-id", name:"​displayName​"},
	          		{value:"urn:​oid:​2.16.840.1.113730.3.1.3-id", name:"​employeeNumber​"},
	          		{value:"urn:​oid:​2.16.840.1.113730.3.1.39-id", name:"​preferredLanguage​"},
	          		{value:"urn:​oid:​2.16.840.1.113730.3.1.4-id", name:"​employeeType​"},
	          		{value:"urn:​oid:​2.16.840.1.113730.3.1.40-id", name:"​userSMIMECertificate​"},
	          		{value:"urn:​oid:​2.5.4.10-id", name:"​o​"},
	          		{value:"urn:​oid:​2.5.4.11-id", name:"​ou​"},
	          		{value:"urn:​oid:​2.5.4.12-id", name:"​title​"},
	          		{value:"urn:​oid:​2.5.4.13-id", name:"​description​"},
	          		{value:"urn:​oid:​2.5.4.16-id", name:"​postalAddress​"},
	          		{value:"urn:​oid:​2.5.4.17-id", name:"​postalCode​"},
	          		{value:"urn:​oid:​2.5.4.18-id", name:"​postOfficeBox​"},
	          		{value:"urn:​oid:​2.5.4.19-id", name:"​physicalDeliveryOfficeName​"},
	          		{value:"urn:​oid:​2.5.4.20-id", name:"​telephoneNumber​"},
	          		{value:"urn:​oid:​2.5.4.21-id", name:"​telexNumber​"},
	          		{value:"urn:​oid:​2.5.4.3-id", name:"​cn​"},
	          		{value:"urn:​oid:​2.5.4.36-id", name:"​userCertificate​"},
	          		{value:"urn:​oid:​2.5.4.4-id", name:"​sn​"},
	          		{value:"urn:​oid:​2.5.4.41-id", name:"​name​"},
	          		{value:"urn:​oid:​2.5.4.42-id", name:"​givenName​"},
	          		{value:"urn:​oid:​2.5.4.7-id", name:"​l​"},
	          		{value:"urn:​oid:​2.5.4.9-id", name:"​street​"}
			  ];
			  
			  break;
		  case "contactTypes":
			  collection = [
	        		{value:"administrative", name:"Administrative"},
	        		{value:"technical", name:"Technical"},
	        		{value:"support", name:"Support"},
	        		{value:"billing", name:"Billing"},
	        		{value:"other", name:"Other"}
			  ];
			  
			  break;

		  case "useTypes":
			  collection = [
	             	{value:"encryption", name:"Encryption"},
	            	{value:"signing", name:"Signing"}
			  ];
			  
			  break;
		  case "nameFormat":
			  collection = [
	             	{value:"urn:oasis:names:tc:SAML:2.0:nameid-format:persistent", name:"persistent"},
	               	{value:"urn:oasis:names:tc:SAML:2.0:nameid-format:transient", name:"transient"},
	               	{value:"urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress", name:"emailAddress"},
	               	{value:"urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified", name:"unspecified"},
	               	{value:"urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName", name:"X509SubjectName"},
	               	{value:"urn:oasis:names:tc:SAML:1.1:nameid-format:WindowsDomainQualifiedName", name:"WindowsDomainQualifiedName"},
	               	{value:"urn:oasis:names:tc:SAML:2.0:nameid-format:kerberos", name:"kerberos"},
	               	{value:"urn:oasis:names:tc:SAML:2.0:nameid-format:entity", name:"entity"}
			  ];
			  
			  break;
		  case "lang":
			  collection = [
		        	{value:"en", name:"English"},
		        	{value:"no", name:"Norwegian (bokmål)"},
		        	{value:"nn", name:"Norwegian (nynorsk)"},
		        	{value:"se", name:"Sámegiella"},
		        	{value:"da", name:"Danish"},
		        	{value:"de", name:"German"},
		        	{value:"sv", name:"Swedish"},
		        	{value:"fi", name:"Finnish"},
		        	{value:"es", name:"Español"},
		        	{value:"fr", name:"Français"},
		        	{value:"it", name:"Italian"},
		        	{value:"nl", name:"Nederlands"},
		        	{value:"lb", name:"Luxembourgish"},
		        	{value:"cs", name:"Czech"},
		        	{value:"sl", name:"Slovenščina"},
		        	{value:"lt", name:"Lietuvių kalba"},
		        	{value:"hr", name:"Hrvatski"},
		        	{value:"hu", name:"Magyar"},
		        	{value:"pl", name:"Język polski"},
		        	{value:"pt", name:"Português"},
		        	{value:"pt-BR", name:"Português brasileiro"},
		        	{value:"tr", name:"Türkçe"},
		        	{value:"el", name:"ελληνικά"},
		        	{value:"ja", name:"Japanese (日本語)"}
			  ];
			  
			  break;
		  default: 
			throw "CollectionFactory.create ==> Bad Collection Type : " + type;
		    break;
		}			
		
		return collection;

	};

	
	return {
		create : create
	};
});