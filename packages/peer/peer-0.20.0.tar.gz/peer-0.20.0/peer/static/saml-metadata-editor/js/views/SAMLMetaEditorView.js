define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'text!templates/SAMLMetaEditorTemplate.html',
	'views/StructureView',
	'service/ModelFactory'
], 
function($, _, Backbone, SAMLMetaEditorTemplate, StructureView, ModelFactory) {

	var SAMLMetaEditorView = Backbone.View.extend({
		initialize : function(options){
			this.root = ModelFactory.create("md:EntityDescriptor");
			this.structureView = new StructureView({root : this.root});
		},
		render : function(){
			var compiledTemplate = _.template(SAMLMetaEditorTemplate);
			this.$el.html(compiledTemplate());

			this.$el.find("#structureTab").append(this.structureView.render().el);
			
			return this;
		},
		
		events : {
			"click a#toTree" : "toTree",
			"click a#toXML" : "toXML"
		},
		toTree : function(){
			var xml = this.$el.find("#xmlcontent").val().replace(/\n/g,"").replace(/\t+/g," ").trim();
			if(xml == null || xml.length == 0)
				return false;
				
			var node = jQuery.parseXML(xml);
			node = node.children.item();
			
			this.root = toStructure(node);
			this.structureView.setRoot(this.root);
		},
		toXML : function(){
	    	var xml = toXML(0, this.root);
	    	this.$el.find("#xmlcontent").val(xml);
		}
	});
	
	function toXML(tab, node){
		
		// Casos base nodo nulo
		if(node == null)
			return "";
			
		//	Numero de tabulaciones
		var tabText = "";
		for(var i = 0; i < tab; i++)
			tabText += "\t";
		
		// Generacion del tag y attributos
		var openTagText = "";
		openTagText = tabText + "<" + node.get("tag") + " ";
		
		//	Espacios de nombres
		if(node.get("xmlns") != null)
			openTagText += "\t";
			
		for(var key in node.get("xmlns")){
			openTagText += "xmlns:" + key + "='" + node.get("xmlns")[key] + "'\n" + tabText + "\t\t\t\t\t";
		}
		
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
				text += node.get("text").value;
				
			if(node.get("xml") != null)
				text += "\n" + tabText + "\t" + node.get("xml") + "\n" + tabText;

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

	function toStructure(nodeXML){
				
		var name = nodeXML.nodeName;
		var nodeSAML = ModelFactory.create(name);
		
		// agregamos los atributos al nodo
		for(var attr in nodeSAML.get("attributes")){
			
			var value = nodeXML.getAttribute(attr);
			if(value != null)
				nodeSAML.get("attributes")[attr].value = value;
		}
		
		//	Agregamos el texto que contenga el nodo
		if(nodeXML.firstChild != null && nodeXML.firstChild.textContent != null && nodeXML.firstChild.textContent != "" && nodeSAML.get("text") != null)
			nodeSAML.get("text").value = nodeXML.firstChild.textContent.trim();
		
		// posibles hijos
		var options = [];
		for(var j = 0; j < nodeSAML.get("options").length; j++){
			options.push(nodeSAML.get("options")[j].value);
		}

		var xml_serializer = new XMLSerializer();

		// inspeccionamos los hijos
		for(var i = 0; i < nodeXML.children.length; i++){
			var child = nodeXML.children[i];
			var tagName = child.tagName;

			var xml = "";
			if(options.indexOf(tagName) != -1){
				var node = toStructure(child);
				nodeSAML.addChild(node);					
			}else{
				xml += xml_serializer.serializeToString(child);
			}
			
			if(nodeSAML.get("xml") != null && xml != ""){
				nodeSAML.set("xml", xml);
			}
		}
		
		return nodeSAML;
	};	
	
	return SAMLMetaEditorView;
});
