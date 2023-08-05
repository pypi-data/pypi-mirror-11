var OPAL = {};
if(undefined === version){ var version = 'test'}; 

OPAL.module = function(namespace, dependencies){
    if(undefined === dependencies){ dependencies = []; };
    dependencies.push('angular-growl');
    dependencies.push('mentio');
    if(undefined === OPAL_ANGULAR_DEPS) { var OPAL_ANGULAR_DEPS = [] }
    _.each(OPAL_ANGULAR_DEPS, function(d){ dependencies.push(d) });            
    var mod = angular.module(namespace, dependencies);
    // See http://stackoverflow.com/questions/8302928/angularjs-with-django-conflicting-template-tags
    mod.config(function($interpolateProvider) {
	    $interpolateProvider.startSymbol('[[');
	    $interpolateProvider.endSymbol(']]');
    });

    mod.config(['growlProvider', function(growlProvider) {
        growlProvider.globalTimeToLive(5000);
    }]);

    // IE8 compatability mode! 
    mod.config(function($sceProvider){$sceProvider.enabled(false)});

    return mod;
};

OPAL.run = function(app){
    app.run(['$rootScope', 'ngProgressLite', '$modal', OPAL._run])
}

OPAL._run = function($rootScope, ngProgressLite, $modal) {

    // Let's allow people to know what version they're running
    $rootScope.OPAL_VERSION = version;
    
    // When route started to change.
    $rootScope.$on('$routeChangeStart', function() {
        ngProgressLite.set(0);
        ngProgressLite.start();
    });

    // When route successfully changed.
    $rootScope.$on('$routeChangeSuccess', function() {
        ngProgressLite.done();
    });

    // When some error occured.
    $rootScope.$on('$routeChangeError', function() {
        ngProgressLite.set(0);
    });

    $rootScope.open_modal = function(controller, template, size, resolves){
        resolve = {}
        _.each(_.keys(resolves), function(key){
            resolve[key] = function(){ return resolves[key] };
        })
        return $modal.open({
            controller : controller,
            templateUrl: template,
            size       : size,
            resolve    : resolve
        });
    }
    
};


// From http://stackoverflow.com/questions/3629183/why-doesnt-indexof-work-on-an-array-ie8
if (!Array.prototype.indexOf) {
	Array.prototype.indexOf = function(elt /*, from*/)
	{
		var len = this.length >>> 0;
		var from = Number(arguments[1]) || 0;
		from = (from < 0)
		    ? Math.ceil(from)
		    : Math.floor(from);
		if (from < 0)
			from += len;

		for (; from < len; from++)
		{
			if (from in this &&
			    this[from] === elt)
				return from;
		}
		return -1;
	};
}

function clone(obj) {
	if (typeof obj == 'object') {
		return $.extend(true, {}, obj);
	} else {
		return obj;
	}
};

// From http://stackoverflow.com/a/3937924/2463201
jQuery.support.placeholder = (function(){
	var i = document.createElement('input');
	return 'placeholder' in i;
})();


// Fuck you Internet Explorer 8
if (typeof String.prototype.trim !== 'function') {
	String.prototype.trim = function() {
		return this.replace(/^\s+|\s+$/g, '');
	}
}



// // From http://stackoverflow.com/a/2897510/2463201
// jQuery.fn.getCursorPosition = function() {
//     var self = this;
// 	var input = self.get(0);
// 	if (!input) return; // No (input) element found
// 	if ('selectionStart' in input) {
// 		// Standard-compliant browsers
// 		return input.selectionStart;
// 	} else if (document.selection) {
// 		// IE
// 		input.focus();
// 		var sel = document.selection.createRange();
// 		var selLen = document.selection.createRange().text.length;
// 		sel.moveStart('character', -input.value.length);
// 		return sel.text.length - selLen;
// 	}
// }
