define(
[ 
	'jquery', 
	'underscore', 
	'backbone'
], 
function($, _, Backbone) {

	var options = [
       	{value:"true", name:"True"},
       	{value:"false", name:"False"}
   	];

	var AssertionConsumerService = Backbone.Model.extend({
		initialize : function(options){
	        this.parent = (options == null || options.parent == null) ? null : options.parent;
		},
		defaults : function(){
			
			//	 To create a new instace of objects use the return command
			return {
				tag : "md:AssertionConsumerService",
				name : "Assertion Consumer Service",
				xml : "",
				text : null,
				childs : [],
				options : [],
				attributes : {
					Binding : {name : "Binding", options : null,  value : "", required : true},
					Location: {name : "Location", options : null, value : "", required : true},
					ResponseLocation : {name : "Response Location", options : null, value : "", required : false},
					index : {name : "Index", options : null, value : "", required : true},		
					isDefault : {name : "Is Default", options : options, value : "", required : false}				
				}
			};
		},
		getParent : function(){
			return this.parent;
		}
	});
	
	return AssertionConsumerService;
});