define(
[
 	'jquery', 
 	'underscore', 
 	'backbone',
 	'views/SAMLMetaEditorView'
 ], 
function($, _, Backbone, SAMLMetaEditorView){
	
	var initialize = function() {
		
		var samlmetaeditorview = new SAMLMetaEditorView();
		$("#samlmetaeditor").html(samlmetaeditorview.render().el);
		
		Backbone.history.start();
	};

	return {
		initialize : initialize
	};
});
