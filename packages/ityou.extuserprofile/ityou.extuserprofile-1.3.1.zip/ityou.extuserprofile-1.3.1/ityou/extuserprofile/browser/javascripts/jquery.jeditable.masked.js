/*
* date_masked input for Jeditable
*
* Copyright (c) 2007-2008 Mika Tuupola
*
* Licensed under the MIT license:
* http://www.opensource.org/licenses/mit-license.php
*
* Depends on date_masked Input jQuery plugin by Josh Bush:
* http://digitalbush.com/projects/date_masked-input-plugin
*
* Project home:
* http://www.appelsiini.net/projects/jeditable
*
* Revision: $Id$
*
*/
 
$.editable.addInputType('masked', {
    element : function(settings, original) {
        /* Create an input. date_mask it using date_masked input plugin. Settings */
        /* for date_mask can be passed with Jeditable settings hash. */
        var input = $('<input />').masked(settings.mask);
        $(this).append(input);
        return(input);
    }
});