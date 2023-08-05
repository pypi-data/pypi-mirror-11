define(
[ 
	'jquery', 
	'underscore', 
	'backbone',
	'text!templates/StructureTemplate.html',

	'service/ModelFactory'
], 
function($, _, Backbone, StructureTemplate, ModelFactory) {

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
				"<li class = 'listItem'>" +
				"	<div class = 'tab' style = 'float: left; margin-right : 5px; padding: 0px 5px;'>&nbsp;</div>" +
				"	<div class = 'icon hide' style = 'float: left; margin-right : 5px; padding: 0px 5px;'>-</div>" +
				"	<div class = 'text'> <%=text%>" +
				"<a id = 'remove' href='#removeChild' style = 'color : red; margin-left : 0.5rem;' class='hide right'>X</a>" +
				"<span id = 'error' style = 'color : #f04124' class='hide right'>!</span></div></li>" +
				"<ul id = 'childs'></ul>"
		),
		addChild : function(nodeview){
			this.$el.find("#childs:first").append(nodeview.render().el);
			this.$el.find(".icon:first").removeClass("hide");
			this.$el.find(".tab:first").addClass("hide");
		},
		hasError: function(){
			if(_.isEmpty(this.model.validationError ))
				this.$el.find("#error:first").addClass("hide");
			else
				this.$el.find("#error:first").removeClass("hide");
		},
		
		events : {
			"click div.icon" : "toggle",
			"click div.text" : "select",
			"click a#remove" : "remove"
		},
		toggle : function(){
			if(this.collapse){
				this.collapse = false;
				this.$el.find("#childs").show();
				this.$el.find(".icon:first").empty();
				this.$el.find(".icon:first").text("-");
			}else{
				this.collapse = true;
				this.$el.find("#childs").hide();
				this.$el.find(".icon:first").empty();
				this.$el.find(".icon:first").text("+");
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
					
					parentNode.isValid();
				}
			}
			
			if(this.structureView != null)
				this.structureView.selectNode(null, null);

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
			"	<div class='small-3 medium-3 large-3 columns'><a id = 'add' href='#addChild' class='button radius tiny expand'>Add Child</a></div>" +
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
				"			<% if(text.options == null){ %>" +
				"				<label>" +
				"					<%if(errors != null && errors['text'] != null){%>" +
				"						Text Content<textarea class = 'error' cols='100%' placeholder='Text content ...'><%=text.value%></textarea>" +
				"						<small class='error'><%=errors['text']%></small>" +
				"					<%}else{%>" +
				"						Text Content<textarea cols='100%' placeholder='Text content ...'><%=text.value%></textarea>" +
				"					<%}%>"+
				"				</label>" +
				"			<%}else{%>" +
				"				<select>" +
				"					<%_.each(text.options, function(option){%>" +
				"						<option value='<%=option.value%>' <%if(text.value == option.value){print('selected')}%> >" +
				"						<%=option.name%></option>" +
				"					<%})	%>" +
				"				</select>" +
				"			<%}%>" +
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
	
	var NodeErrorsView = Backbone.View.extend({
		initialize : function(options){
			this.structureView = (options == null || options.structureView == null) ? null : options.structureView;
		},		
		template : _.template(
				"<% if(errors != null && errors['childs'] != null){%>" +
				"	<% _.each(errors['childs'], function(error) { %>" +
				"		<div data-alert class='alert-box alert radius'><%=error%></div>" +
				"	<% })%>" +
				"<%}%>"
		),
		render : function(){
			this.$el.html(this.template({
				errors : (this.model == null)? {} :this.model.validationError
			}));			
			return this;
		},
		setNode : function(node){
			this.model = node;
			this.render();

			if(this.model != null)
	        	this.listenTo(this.model, "invalid", this.render);	        
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
			this.nodeErrorsView = new NodeErrorsView({structureView : this});
		},
		render : function(){
			var compiledTemplate = _.template(StructureTemplate);
			this.$el.html(compiledTemplate());
			
			this.$el.find("#root").append(this.rootView.render().el);
			this.$el.find("#nodeSelected").append(this.nodeSelectedView.render().el);
			this.$el.find("#nodeDetails").append(this.nodeDetailsView.render().el);
			this.$el.find("#nodeErrors").append(this.nodeErrorsView.render().el);
			
	        return this;
		},
		selectNode : function(view, node){
			this.selectNodeView = view;
			this.select = node;
			
			if(this.select != null)
				this.select.isValid();
			
			this.nodeSelectedView.setNode(node);
			this.nodeDetailsView.setNode(node);
			this.nodeErrorsView.setNode(node);
		},
		addChild : function(type){
			var node = ModelFactory.create(type);
			this.select.addChild(node);

			if(node != null)
				this.selectNodeView.addChild(new NodeView({structureView : this, model : node}));
			
			this.nodeSelectedView.setNode(this.select);
			this.select.isValid();
			
			return false;
		},
		changeAttributes : function(id, value){
			var attributes = this.select.get("attributes");
			attributes[id].value = value;
			this.select.isValid();
		},
		changeContent : function(value){
			var text = this.select.get("text");
			text.value = value;
			this.select.isValid();
		},
		changeElements : function(value){
			this.select.set("xml", value);
			this.select.isValid();
		},
		setRoot : function(root){
			this.$el.find("#root").empty();

			this.root = root;
			this.rootView = new NodeView({structureView : this, model : this.root});
			this.$el.find("#root").append(this.rootView.render().el);
			
			makeTreeView(this, this.rootView, this.root);
			
			this.$el.find("#tree").height(window.innerHeight - 204);
		}
	});
	
	function makeTreeView(structureView, nodeView, nodeModel){
		
		nodeModel.isValid();
		var childs = nodeModel.get("childs");
		for(var i = 0; i < childs.length; i++){
			var child = childs[i];
			if(child == null)
				continue;
			
			if(Array.isArray(child)){
				for(var j = 0; j < child.length; j++){
					var nodeChildModel = child[j];
					var nodeChildView = new NodeView({structureView : structureView, model : nodeChildModel});
					nodeView.addChild(nodeChildView);
				
					makeTreeView(structureView, nodeChildView, nodeChildModel);
				}
			}else{
				var nodeChildModel = child;
				var nodeChildView = new NodeView({structureView : structureView, model : nodeChildModel});
				nodeView.addChild(nodeChildView);

				makeTreeView(structureView, nodeChildView, nodeChildModel);
			}
		}
	}
	
	return StructureView;
});
