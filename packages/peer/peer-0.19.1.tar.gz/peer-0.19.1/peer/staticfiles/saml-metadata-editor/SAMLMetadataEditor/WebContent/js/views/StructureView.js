define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'text!templates/StructureTemplate.html',

	'models/EntitiesDescriptor',
	'models/EntityDescriptor'
], 
function($, _, Backbone, StructureTemplate, EntitiesDescriptor, EntityDescriptor) {

	var NodeView = Backbone.View.extend({
		initialize : function(options){
			this.structureView = (options == null || options.structureView == null) ? null : options.structureView;
	        this.collapse = false;
	        
	        if(this.model != null)
	        	this.listenTo(this.model, "invalid", this.hasError);	        
		},		
		render : function(){
			this.$el.html(this.template({text : this.model.get("name")}));
			return this;
		},
		template : _.template(
				"<li class = 'listItem'><div class = 'text'> <%=text%>" +
				"<a id = 'remove' href='#' style = 'color : red; margin-left : 0.5rem;' class='hide right'>X</a>" +
				"<span id = 'error' style = 'color : #f04124' class='hide right'>!</span></div></li>" +
				"<ul id = 'childs'></ul>"
		),
		addChild : function(nodeview){
			this.$el.addClass("expand");

			this.$el.find("#childs:first").append(nodeview.render().el);
		},
		hasError: function(){
			if(_.isEmpty(this.model.validationError ))
				this.$el.find("#error").addClass("hide");
			else
				this.$el.find("#error").removeClass("hide");
		},
		
		events : {
			"dblclick div.text" : "toggle",
			"click div.text" : "select",
			"click a#remove" : "remove",
			"mouseover span:first#error" : "showError"
		},
		toggle : function(){
			this.$el.removeClass("expand");
			this.$el.removeClass("collapse");

			if(this.collapse){
				this.collapse = false;
				this.$el.addClass("expand");
				this.$el.find("#childs").show();
			}else{
				this.collapse = true;
				this.$el.addClass("collapse");
				this.$el.find("#childs").hide();
			}
			
			return false;
		},
		select : function(){
			$("#root div.text").removeClass("select");
			$("#root a").addClass("hide");

			this.$el.find(".text:first").addClass("select");
			if(this.$el.parent().attr("id") != "root")
				this.$el.find("#remove:first").removeClass("hide");
			
			if(this.structureView != null)
				this.structureView.selectNode(this, this.model);
			
			return false;
		},
		remove : function(){
			if(this.model != null){
				var parentNode = this.model.getParent();
				
				if(parentNode != null){
					parentNode.removeChild(this.model);
					this.$el.remove();
				}
			}
			
			return false;
		},
		showError : function(){
			this.$el.find("span:first#error").attr("title",this.model.validationError["childs"]);
			
			return false;
		}
	});
	
	var NodeSelectedView = Backbone.View.extend({
		initialize : function(options){
			this.structureView = (options == null || options.structureView == null) ? null : options.structureView;
		},
		template : _.template(
			"<div class = 'row'>" +
			"	<div class='small-3 medium-3 large-3 columns'><label class = 'inline'>Element name: </label></div>" +
			"	<div class='small-9 medium-9 large-9 columns'><label class = 'inline'><%=name%></label></div>" +
			"</div>" +
			"<%if(options.length > 0){%>" +
			"<div class = 'row'>" +
			"	<div class='small-3 medium-3 large-3 columns'><label class = 'inline'>Type of child: </label></div>" +
			"	<div class='small-6 medium-6 large-6 columns'>" +
			"		<select id='options'>" +
			"   	<% _.each(options, function(option) { %>"+
			"       	<option value='<%=option.value%>'<% option.disabled?print('disabled'):print('')%> > <%=option.name%></option>"+
			"   	<% }); %>"+
			"		</select>" +
			"	</div>" +
			"	<div class='small-3 medium-3 large-3 columns'><a href='#' id='add' class='button radius tiny expand'>Add Child</a></div>" +
			"</div>" +
			"<%}%>"
		),
		render : function(){
			this.$el.html(this.template({
				name : (this.model == null)? "" : this.model.get("name"),
				options : (this.model == null)? "" : this.model.get("options")
			}));
			
			return this;
		},
		setNode : function(node){
			this.model = node;
			this.render();
		},
		
		events : {
			"click a#add" : "addChild"
		},
		addChild : function(){
			if(this.structureView != null)
				this.structureView.addChild($("#options").val());
		}	
	});
	
	var NodeDetailsView = Backbone.View.extend({
		initialize : function(options){
			this.structureView = (options == null || options.structureView == null) ? null : options.structureView;
		},
		template : _.template(
				"<% _.each(attributes, function(attribute, id) { %>" +
				"	<div id = 'attributes' class  = 'row collapse'>" +
				"       <div class='small-4 medium-4 large-4 columns'>" +
				"			<span class = 'prefix'><%=attribute.name%></span>" +
				"		</div>" +
				"       <div class='small-8 medium-8 large-8 columns'>" +
				"			<% if(attribute.options == null) {%>" +
				"				<% if(errors != null && errors[id] != null){%>" +
				"					<input class = 'error' type='text' id = '<%=id%>' placeholder='<%=attribute.name%> ...' / value = '<%=attribute.value%>'>" +
				"					<small class = 'error'><%=errors[id]%></small>" +
				"				<%}else{%>" +
				"					<input type='text' id = '<%=id%>' placeholder='<%=attribute.name%> ...' / value = '<%=attribute.value%>'>" +
				"				<%}%>" +
				"			<%}else{%>" +
				"				<select id = '<%=id%>'>" +
				"					<%_.each(attribute.options, function(option){%>" +
				"						<option value='<%=option.value%>' <%if(attribute.value == option.value){print('selected')}%> >" +
				"						<%=option.name%></option>" +
				"					<%})	%>" +
				"				</select>" +
				"			<%}%>" +
				"		</div>" +
				"	</div>"+
				"<% }); %>" +
				"<%if(text != null){%>" +
				"	<div id = 'textContent' class = 'row'>" +
				"		<div class='small-12 medium-12 large-12 columns'>" +
				"			<label>" +
				"				<%if(errors != null && errors['text'] != null){%>" +
				"					Text Content<textarea class = 'error' cols='100%' placeholder='Text content ...'><%=text%></textarea>" +
				"					<small class='error'><%=errors['text']%></small>" +
				"				<%}else{%>" +
				"					Text Content<textarea cols='100%' placeholder='Text content ...'><%=text%></textarea>" +
				"				<%}%>"+
				"			</label>" +
				"		</div>" +
				"	</div>" +
				"<%}%>" +
				"<%if(xml != null){%>" +
				"	<div id = 'xmlElements' class = 'row'>" +
				"		<div class='small-12 medium-12 large-12 columns'>" +
				"			<label>" +
				"				XML Elements<textarea cols='100%' placeholder='<!--any element--> ...'><%=xml%></textarea>" +
				"			</label>" +
				"		</div>" +
				"	</div>" +
				"<%}%>"
			),
		render : function(){
			this.$el.html(this.template({
				attributes : (this.model == null)? {} : this.model.get("attributes"),
				text : (this.model == null)? null : this.model.get("text"),
				xml : (this.model == null)? null : this.model.get("xml"),
				errors : (this.model == null)? {} :this.model.validationError
			}));			
			return this;
		},
		setNode : function(node){
			this.model = node;
			this.render();

			if(this.model != null)
	        	this.listenTo(this.model, "invalid", this.render);	        
		},
		events : {
			"change div#textContent" : "changeContent",
			"change div#attributes" : "changeAttributes",
			"change div#xmlElements" : "changeElements"
		},
		changeContent : function(event){
			if(this.structureView != null)
				this.structureView.changeContent(event.target.value);
		},
		changeElements : function(event){
			if(this.structureView != null)
				this.structureView.changeElements(event.target.value);
		},
		changeAttributes : function(event){
			if(this.structureView != null)
				this.structureView.changeAttributes(event.target.id, event.target.value);
		}
	});
	
	var StructureView = Backbone.View.extend({
		initialize : function(options){
			this.root = (options == null || options.root == null) ? null: options.root;
			
			this.select = null;
			this.selectNodeView = null;
			
			this.rootView = new NodeView({structureView : this, model : this.root});
			this.nodeSelectedView = new NodeSelectedView({structureView : this});			
			this.nodeDetailsView = new NodeDetailsView({structureView : this});
		},
		render : function(){
			var compiledTemplate = _.template(StructureTemplate);
			this.$el.html(compiledTemplate());
			
			this.$el.find("#root").append(this.rootView.render().el);
			this.$el.find("#nodeSelected").append(this.nodeSelectedView.render().el);
			this.$el.find("#nodeDetails").append(this.nodeDetailsView.render().el);
			
	        return this;
		},
		selectNode : function(view, node){
			this.selectNodeView = view;
			this.select = node;
			
			this.nodeSelectedView.setNode(node);
			this.nodeDetailsView.setNode(node);
		},
		addChild : function(type){
			var node = this.select.addChild(type);

			if(node != null)
				this.selectNodeView.addChild(new NodeView({structureView : this, model : node}));
			
			this.nodeSelectedView.setNode(this.select);
		},
		changeAttributes : function(id, value){
			var attributes = this.select.get("attributes");
			attributes[id].value = value;
			this.select.isValid();
		},
		changeContent : function(value){
			this.select.set("text", value);
			this.select.isValid();
		},
		changeElements : function(value){
			this.select.set("xml", value);
			this.select.isValid();
		}
	});
	
	return StructureView;
});
