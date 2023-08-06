(function ( $ ) {

    var pluginName = "{{plugin_name}}",
        defaults = {

        };

    function {{plugin_name_cc}} ( element, options ) {
        this.element = element;
        this.settings = $.extend( {}, defaults, options );
        this._defaults = defaults;
        this._name = pluginName;
        this.init();
    }

    $.extend({{plugin_name_cc}}.prototype, {
        init: function () {

        }
    });

    $.fn[ pluginName ] = function ( options ) {
        this.each(function() {
            if (!$.data(this, "plugin_" + pluginName)) {
                $.data(this, "plugin_" + pluginName, new {{plugin_name_cc}}(this, options));
            }
        });
        return this;
    };
}( jQuery ));
