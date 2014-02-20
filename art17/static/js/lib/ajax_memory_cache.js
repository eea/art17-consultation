var ajax_cache = {};

$.ajaxPrefilter(function( options, originalOptions, jqXHR ) {

    if(options.noCache) {
        return;
    }

    var cacheKey = options.cacheKey ||
                   options.url.replace( /jQuery.*/,'' ) + options.type + options.data;

    var value = ajax_cache[cacheKey];

    // prevent multiple calls to the same url
    if(value === null) {
        jqXHR.abort();
    }

    if(value) {

        if(options.dataType.indexOf('json') === 0) {
            value = JSON.parse( value );
        }
        options.success(value);
        jqXHR.abort();

    } else {
        ajax_cache[cacheKey] = null;
        if(options.success) {
            options.realsuccess = options.success;
        }

        options.success = function(data) {
            var strdata = data;
            if(this.dataType.indexOf('json') === 0 ) {
                strdata = JSON.stringify( data );
            }

            ajax_cache[cacheKey] = strdata;
            if (options.realsuccess) {
                options.realsuccess(data);
            }
        };
    }

});
