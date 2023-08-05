define(
[
 	'jquery', 
 	'underscore', 
 	'backbone',
 	'views/AppView',
 	'views/StructureView',
 	'models/EntityDescriptor'
 ], 
function($, _, Backbone, AppView, StructureView, EntityDescriptor){

	var initialize = function() {
		
		var root = new EntityDescriptor();
		var appView = new AppView({root : root});
		$("body").append(appView.render().el);
		
		var structureView = new StructureView({root : root});
		$("#structure").append(structureView.render().el);
				
		Backbone.history.start();

	};

	return {
		initialize : initialize
	};
});