define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'text!templates/AppTemplate.html'
], 
function($, _, Backbone, AppTemplate) {
	var AppView = Backbone.View.extend({
		initialize : function(options){
			this.root = (options == null || options.root == null) ? null: options.root;
		},
		render : function(){
			var compiledTemplate = _.template(AppTemplate);
			this.$el.html(compiledTemplate());
	        return this;
		},
		events : {
			"click .tabs a#toXML" : "toXML",
			"click .tabs a#toTree" : "toTree"
		},
		toXML : function(){
			var xmlcontent = this.$el.find("#xmlcontent");
			
			xmlcontent.empty();
			xmlcontent.text(toXML(0, this.root));
		},
		toTree : function(){
			
		}
	});
	
	return AppView;
});

function toXML(tab, node){
	
	// Casos base nodo nulo
	if(node == null)
		return "";
	
	//	Verificamos que el nodo sea correcto
	node.isValid();	
	
	//	Numero de tabulaciones
	var tabText = "";
	for(var i = 0; i < tab; i++)
		tabText += "\t";
	
	// Generacion del tag y attributos
	var openTagText = "";
	openTagText = tabText + "<" + node.get("tag") + " ";
	
	var attributes = node.get("attributes");
	for(var key in attributes){
		var attr = attributes[key];
		
		if(attr.value.length != 0)
			openTagText += key + "='" + attr.value + "' ";
	}
	openTagText = openTagText.slice(0, - 1);
	openTagText +=">";
	
	var closeTagText = "</"+ node.get("tag") + ">\n";
	
	var text = "";
	
	// Caso base sin hijos
	if(node.get("childs").length == 0){
		
		if(node.get("text") != null)
			text += node.get("text");
			
		if(node.get("xml") != null)
			text += "\n" + tabText + node.get("xml") + "\n" + tabText;

		return openTagText + text + closeTagText;
	}
	
	//	Caso recursivo de tener hijos
	var childs = node.get("childs");
	for(var i = 0; i < childs.length; i++){
		var child = node.get("childs")[i];
		
		if(Array.isArray(child)){
			for(var j = 0; j < child.length; j++)
				text += toXML(tab + 1, child[j]);
				
		}else{
			text += toXML(tab + 1, child);
		}
	}
	
	return openTagText + "\n" + text + tabText + closeTagText;
};
