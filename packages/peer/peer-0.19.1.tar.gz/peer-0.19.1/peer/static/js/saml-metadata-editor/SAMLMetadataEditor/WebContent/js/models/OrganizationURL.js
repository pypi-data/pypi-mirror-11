define(
[ 
	'jquery', 
	'underscore', 
	'backbone'
], 
function($, _, Backbone) {

	var lang = [	
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
	
	var OrganizationURL = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:OrganizationURL",
				name : "Organization URL",
				text : "",
				xml : null,
				childs : [],
				options : [],
				attributes : {
				  "xml:lang" : {name : "Lang", options : lang,  value : lang[0].value}
				}
			};
		},
		validate: function(attrs, options) {
			
			var obj = {};
			
			// URL validation
			var urlRegex = new RegExp("(^|\\s)((https?:\/\/)?[\\w-]+(\\.[\\w-]+)+\.?(:\\d+)?(\/\\S*)?)", "i");
			if(	attrs.text != "" && !urlRegex.test(attrs.text))
				obj["text"] = "The text content must be a URL";
			
			return obj;
		},
		getParent : function(){
			return this.parent;
		}
	});
	
	return OrganizationURL;
});