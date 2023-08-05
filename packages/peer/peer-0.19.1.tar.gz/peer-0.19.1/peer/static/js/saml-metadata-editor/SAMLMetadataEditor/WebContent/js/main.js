require.config({
	shim : {
		foundation : {
			deps : [ "jquery", "modernizr" ]
		},
		foundationTab : {
			deps : [ "foundation" ]
		},
		foundationAccordion : {
			deps : [ "foundation" ]
		}
	},
	paths : {
		jquery : 'libs/jquery/jquery-2.1.1.min',
		underscore : 'libs/underscore/underscore-min',
		backbone : 'libs/backbone/backbone-min',
		modernizr : 'libs/modernizr/modernizr',
		foundation : 'libs/foundation/foundation',
		foundationTab : 'libs/foundation/foundation.tab',
		foundationAccordion : 'libs/foundation/foundation.accordion'
	}
});

require(
[ 
  'app',
  'jquery',
  'foundation',
  'foundationTab',
  'foundationAccordion'  
], 
function(App) {
	App.initialize();
	$(document).foundation();
	$(window).resize(function() {resizeElements();});
	$(document).ready(function() {resizeElements();});
});


function resizeElements(){
	$("#xmlcontent").height(window.innerHeight - 204);
	$("#tree").height(window.innerHeight - 204);
}