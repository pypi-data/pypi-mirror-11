// --- jquery masked input (edited) -> mask = masked
(function(e){function t(){var e=document.createElement("input"),t="onpaste";return e.setAttribute(t,""),"function"==typeof e[t]?"paste":"input"}var n,a=t()+".masked",r=navigator.userAgent,i=/iphone/i.test(r),o=/android/i.test(r);e.masked={definitions:{9:"[0-9]",a:"[A-Za-z]","*":"[A-Za-z0-9]"},dataName:"rawmaskedFn",placeholder:"_"},e.fn.extend({caret:function(e,t){var n;if(0!==this.length&&!this.is(":hidden"))return"number"==typeof e?(t="number"==typeof t?t:e,this.each(function(){this.setSelectionRange?this.setSelectionRange(e,t):this.createTextRange&&(n=this.createTextRange(),n.collapse(!0),n.moveEnd("character",t),n.moveStart("character",e),n.select())})):(this[0].setSelectionRange?(e=this[0].selectionStart,t=this[0].selectionEnd):document.selection&&document.selection.createRange&&(n=document.selection.createRange(),e=0-n.duplicate().moveStart("character",-1e5),t=e+n.text.length),{begin:e,end:t})},unmasked:function(){return this.trigger("unmasked")},masked:function(t,r){var c,l,s,u,f,h;return!t&&this.length>0?(c=e(this[0]),c.data(e.masked.dataName)()):(r=e.extend({placeholder:e.masked.placeholder,completed:null},r),l=e.masked.definitions,s=[],u=h=t.length,f=null,e.each(t.split(""),function(e,t){"?"==t?(h--,u=e):l[t]?(s.push(RegExp(l[t])),null===f&&(f=s.length-1)):s.push(null)}),this.trigger("unmasked").each(function(){function c(e){for(;h>++e&&!s[e];);return e}function d(e){for(;--e>=0&&!s[e];);return e}function m(e,t){var n,a;if(!(0>e)){for(n=e,a=c(t);h>n;n++)if(s[n]){if(!(h>a&&s[n].test(R[a])))break;R[n]=R[a],R[a]=r.placeholder,a=c(a)}b(),x.caret(Math.max(f,e))}}function p(e){var t,n,a,i;for(t=e,n=r.placeholder;h>t;t++)if(s[t]){if(a=c(t),i=R[t],R[t]=n,!(h>a&&s[a].test(i)))break;n=i}}function g(e){var t,n,a,r=e.which;8===r||46===r||i&&127===r?(t=x.caret(),n=t.begin,a=t.end,0===a-n&&(n=46!==r?d(n):a=c(n-1),a=46===r?c(a):a),k(n,a),m(n,a-1),e.preventDefault()):27==r&&(x.val(S),x.caret(0,y()),e.preventDefault())}function v(t){var n,a,i,l=t.which,u=x.caret();t.ctrlKey||t.altKey||t.metaKey||32>l||l&&(0!==u.end-u.begin&&(k(u.begin,u.end),m(u.begin,u.end-1)),n=c(u.begin-1),h>n&&(a=String.fromCharCode(l),s[n].test(a)&&(p(n),R[n]=a,b(),i=c(n),o?setTimeout(e.proxy(e.fn.caret,x,i),0):x.caret(i),r.completed&&i>=h&&r.completed.call(x))),t.preventDefault())}function k(e,t){var n;for(n=e;t>n&&h>n;n++)s[n]&&(R[n]=r.placeholder)}function b(){x.val(R.join(""))}function y(e){var t,n,a=x.val(),i=-1;for(t=0,pos=0;h>t;t++)if(s[t]){for(R[t]=r.placeholder;pos++<a.length;)if(n=a.charAt(pos-1),s[t].test(n)){R[t]=n,i=t;break}if(pos>a.length)break}else R[t]===a.charAt(pos)&&t!==u&&(pos++,i=t);return e?b():u>i+1?(x.val(""),k(0,h)):(b(),x.val(x.val().substring(0,i+1))),u?t:f}var x=e(this),R=e.map(t.split(""),function(e){return"?"!=e?l[e]?r.placeholder:e:void 0}),S=x.val();x.data(e.masked.dataName,function(){return e.map(R,function(e,t){return s[t]&&e!=r.placeholder?e:null}).join("")}),x.attr("readonly")||x.one("unmasked",function(){x.unbind(".masked").removeData(e.masked.dataName)}).bind("focus.masked",function(){clearTimeout(n);var e;S=x.val(),e=y(),n=setTimeout(function(){b(),e==t.length?x.caret(0,e):x.caret(e)},10)}).bind("blur.masked",function(){y(),x.val()!=S&&x.change()}).bind("keydown.masked",g).bind("keypress.masked",v).bind(a,function(){setTimeout(function(){var e=y(!0);x.caret(e),r.completed&&e==x.val().length&&r.completed.call(x)},0)}),y()}))}})})(jQuery);



(function(c){c.fn.autogrow=function(h){return this.filter("textarea").each(function(){var e=this,a=c(e),g=a.height(),f=a.hasClass("autogrow-short")?0:parseInt(a.css("lineHeight"))||0,d=c("<div></div>").css({position:"absolute",top:-1E4,left:-1E4,width:a.width(),fontSize:a.css("fontSize"),fontFamily:a.css("fontFamily"),fontWeight:a.css("fontWeight"),lineHeight:a.css("lineHeight"),resize:"none","word-wrap":"break-word"}).appendTo(document.body),b=function(b){var c=e.value.replace(/</g,"&lt;").replace(/>/g,
"&gt;").replace(/&/g,"&amp;").replace(/\n$/,"<br/>&nbsp;").replace(/\n/g,"<br/>").replace(/ {2,}/g,function(a){for(var b=0,c="";b<a.length-1;b++)c+="&nbsp;";return c+" "});b&&b.data&&"keydown"===b.data.event&&13===b.keyCode&&(c+="<br />");d.css("width",a.width());d.html(c+(0===f?"...":""));a.height(Math.max(d.height()+f,g))};a.change(b).keyup(b).keydown({event:"keydown"},b);c(window).resize(b);b()})}})(jQuery);



$(function () {
	
	// asco specific
	if($('#mobile').length > 0) {
		if($('#mobile').text().length === 0) {
			$('label.mobile').html($('label.mobile').text() + ' (z.B. +49 ...)');
		}
	}
	
	

    // --- ANFANG --------------------------------------------------------------
	//var ESI_ROOT = $("#ESI_ROOT").text();
	var ESI_ROOT = $('#ESI_DATA').data('ityou-portal-url');
	var ajax_user_property = ESI_ROOT + '/@@ajax-user-property';
	var ajax_personal_images = ESI_ROOT + '/@@ajax-personal-images';
	
	
	var icon_save = '<i class="fa fa-save save-user-property"></i>',
	    enterKey = 13,
	    escKey = 27;
	    
    var openedElement;
    
    
    var input_group = '<div class="input-group"></div>';
    var button_save = '<span class="input-group-btn"><button class="btn btn-default save-user-property" type="submit"><i class="fa fa-save"></i></button></span>';
    
    
    
    var $current;

	
	$(document).on('click', '.property:not(.state-active)', function(e) {
	    var el = $(this),
	        container = el.find('.pfield'),
	        label = el.find('label'),
	        val = container.text();
	        
        el.removeClass('state-hover');
	        
        if(container.hasClass('TextLine')) {
            el.addClass('state-active');
            container
                .html('')
                .append(input_group);
            container
            	.find('.input-group')
            	.css({
            		width: '100%'
            	})
            	.append('<input type="text" name="value" data-oldvalue="' + val + '" value="" autocomplete="off" class="form-control" />')
            	.append(button_save);
            container
            	.find('input')
            	.focus()
            	.val(val);
            
        } else if(container.hasClass('CheckBox')) {
        	if(container.find('i.fa').hasClass('fa-check-square-o')) {
        		val = true;
        	} else {
        		val = false;
        	}
        	
        	el.addClass('state-active');
        	container
        		.html('')
        		.append(input_group);
        	container
        		.find('.input-group')
        		.css({
        			width: '100%',
        			textAlign: 'left'
        		})
        		.append('<input type="checkbox" name="value" data-oldvalue="' + val + '" ' + (val ? 'checked' : '') + '>');
			container.find('input').focus();
        } else if(container.hasClass('Text')) {
        	el.addClass('state-active');
            container
                .html('')
                .append(input_group);
            container
            	.find('.input-group')
            	.css({
            		width: '100%'
            	})
            	.append('<textarea name="value" data-oldvalue="' + val + '" class="form-control"></textarea>')
            	.append(button_save);
            el.find('textarea')
            	.autogrow()
            	.focus()
            	.val(val);
                //.html('<textarea name="value" data-oldvalue="'+val+'"></textarea>')
                //.html('<div class="input-group"><textarea class="form-control" name="value" data-oldvalue="' + val + '"></textarea></div>')
                //.append(icon_save);
            //el.find('textarea').autogrow().focus().val(val);
        } else {
            // Date
            if(container.hasClass('Date')) {
                el.addClass('state-active');
                container
                    .html('')
                    .append(input_group);
                container
                	.find('.input-group')
                	.css({
                		width: '100%'
                	})
                	.append('<input type="text" name="value" data-oldvalue="' + val + '" value="" autocomplete="off" class="form-control" />')
                	.append(button_save);
                    //.html('<div class="input-group"><input type="text" name="value" data-oldvalue="'+val+'" value="" autocomplete="off" /></div>')
                    //.append(icon_save);
                
                container
                    .find('input')
                    .masked('99.99.9999')
                    .focus().val(val);
            }
        }
        
        $current = $(this);
        
        //el.find('input, textarea').focus();
	});
	
	// highlight lines under mouse cursor
	$(document).on({
	    mouseover: function(e) {
	        var regex = new RegExp($('#ESI_DATA').data('ityou-uid'), 'i');
	        if(document.location.pathname.search(regex) !== -1) {
	            $(this).addClass('state-hover');
            }
	    },
	    mouseout: function(e) {
	        $(this).removeClass('state-hover');
	    }
    }, '.property:not(.state-active)');
	
	
	$(document).on('click', '.property .save-user-property', function(e) {
        saveProperty($(this).parents('.property').find('.form-control'), ajax_user_property);
	});
	
	
	$(document).on('change', '.pfield.CheckBox input[type="checkbox"]', function(e) {
		saveProperty($(this), ajax_user_property);
	});
	
	
	$(document).on('keydown', '.pfield.TextLine input, .pfield.Date input', function(e) {
	    //e.preventDefault();
	    
	    var keyCode = typeof e.which === 'number' ? e.which : e.keyCode;
	
	    if(keyCode == 27) { // esc
	        //removeTextEdit($(this).parent().parent(), $(this).attr('data-oldvalue'));
	    } else if(keyCode == 13) { // enter
	        saveProperty($(this), ajax_user_property);
	    }
	    
	    //return false;
	});
	
	var shiftPressed = false;
	$(document).on('keydown', '.pfield input, .pfield textarea', function(e) {
	    var keyCode = typeof e.which === 'number' ? e.which : e.keyCode;

	    if(keyCode == 9) { // TAB
	        e.preventDefault();
	        
	        $current = $(this).parents('.property');
	        
	        if(shiftPressed) { // shift
	        	var $prev = $current.prev('.property');
	        	
	        	if($prev.length === 0) {
	        		$prev = $current.prevUntil('.property').prev('.property');
	        		
	        		if($prev.length === 0 && $current.parents('.left-column').length > 0) {
	        			$prev = $('#userprofile-wrapper').find('.right-column').find('.property').last();
	        		} else if($prev.length === 0 && $current.parents('.right-column').length > 0) {
	        			$prev = $('#userprofile-wrapper').find('.left-column').find('.property').last();
	        		}
	        	}
	        	
	        	saveProperty($(this), ajax_user_property);
	        	
	        	$prev.trigger('click');
	        	$current = $prev;
	        	
	        	return false;
	        } else {
	            var $next = $current.next('.property');
		            
	            if($next.length === 0) {
	                $next = $current.nextUntil('.property').next('.property');
	                
	                if($next.length === 0 && $current.parents('.left-column').length > 0) {
	                    $next = $('#userprofile-wrapper').find('.right-column').find('.property').first();
	                } else if($next.length === 0 && $current.parents('.right-column').length > 0) {
	                    $next = $('#userprofile-wrapper').find('.left-column').find('.property').first();
	                }
	            }
            
	            // save
	            saveProperty($(this), ajax_user_property);
	            
	            // trigger next line
	            $next.trigger('click');
	            $current = $next;
	            
	            return false;
	        }
	    } else if(keyCode == 27) {
	        removeTextEdit($(this).parent().parent(), $(this).attr('data-oldvalue'));
	    }
	});
	
	$(document).on('keydown', function(e) {
	    var keyCode = typeof e.which === 'number' ? e.which : e.keyCode;
	    
	    if(keyCode == 9) { // tab
	        e.preventDefault();
	        
	        if(shiftPressed) {
        		var $prev = $current.prev('.property');
        		
        		if($prev.length === 0) {
        			$prev = $current.prevUntil('.property').prev('.property');
        			
        			if($prev.length === 0 && $current.parents('.left-column').length > 0) {
        				$prev = $('#userprofile-wrapper').find('.right-column').find('.property').last();
        			} else if($prev.length === 0 && $current.parents('.right-column').length > 0) {
        				$prev = $('#userprofile-wrapper').find('.left-column').find('.property').last();
        			}
        		}
        		
        		$prev.trigger('click');
        		$current = $prev;
        		
        		return false;
	        } else {
		        var $next = $current.next('.property');
	            
	            if($next.length === 0) {
	                $next = $current.nextUntil('.property').next('.property');
	                
	                if($next.length === 0 && $current.parents('.left-column').length > 0) {
	                    $next = $('#userprofile-wrapper').find('.right-column').find('.property').first();
	                } else if($next.length === 0 && $current.parents('.right-column').length > 0) {
	                    $next = $('#userprofile-wrapper').find('.left-column').find('.property').first();
	                }
	            }
	            
	            $next.trigger('click');
	            $current = $next;
	            
	            return false;
	        }
	    }
	});
	
	$(document).on({
		keydown: function(e) {
			var keyCode = typeof e.which === 'number' ? e.which : e.keyCode;
			
			if(keyCode == 16) {
				shiftPressed = true;
			}
		},
		keyup: function(e) {
			var keyCode = typeof e.which === 'number' ? e.which : e.keyCode;
			
			if(keyCode == 16) {
				shiftPressed = false;
			}
		}
	});
	
	
    var tclicked;
    //$(document).mousedown(function(e) {
    $(document).on('mousedown', function(e) {
	    tclicked = $(e.target);
	    
	    var parents = $(e.target).parents('.property'),
	        self = $(e.target).hasClass('property');
	        
        var fieldId = self ? $(e.target).find('.pfield').attr('id') : (parents.length > 0 ? parents.find('.pfield').attr('id') : false);
	    
	    if(!fieldId) {
	        removeTextEdit($('.property.state-active'), $('.property.state-active').find('input').data('oldvalue'));
	        return;
	    }
	    
	    if($('.property.state-active').length > 0 && fieldId !== $('.property.state-active').find('.pfield').attr('id')) {
	        removeTextEdit($('.property.state-active'), $('.property.state-active').find('input').data('oldvalue'));
	    }
	});
	
});
		
		
function removeTextEdit(obj, value, success) {
	if(obj.find('.pfield.CheckBox').length > 0) {
		if(undefined === success) {
			obj
				.removeClass('state-active')
				.find('.pfield')
				.html('')
				.html('<i class="fa ' + (value == true ? 'fa-check-square-o' : 'fa-square-o') + '"></i>');
		} else if(success === true) {
			obj
				.addClass('state-hover state-success')
				.removeClass('state-active')
				.find('.pfield')
				.html('')
				.html('<i class="fa ' + (value == true ? 'fa-check-square-o' : 'fa-square-o') + '"></i>');
			setTimeout(function() {
				obj.removeClass('state-hover state-success');
			}, 1000);
		} else if(success === false) {
			obj
				.addClass('state-hover state-failure')
				.removeClass('state-active')
				.find('.pfield')
				.html('')
				.html('<i class="fa ' + (value == true ? 'fa-check-square-o' : 'fa-square-o') + '"></i>');
			setTimeout(function() {
				obj.removeClass('state-hover state-failure');
			}, 1000);
		}
	} else {
	    if(success == undefined) {
	        obj
	            .removeClass('state-active')
	            .find('.pfield')
	            .html('')
	            .text(value);
	        
	        changeFullname();
	    } else if(success == true) {
	        obj
	            .addClass('state-hover state-success')
	            .removeClass('state-active')
	            .find('.pfield')
	            .html('')
	            .text(value);
	        setTimeout(function() {
	            obj.removeClass('state-hover state-success');
	        }, 1000);
	        
	        changeFullname();
	    } else if(success == false) {
	        obj
	            .addClass('state-hover state-failure')
	            .removeClass('state-active')
	            .find('.pfield')
	            .html('')
	            .text(value);
	        setTimeout(function() {
	            obj.removeClass('state-hover state-failure');
	        }, 1000);
	        
	        changeFullname();
	    }
	}
}


function saveProperty(el, baseURI) {
    var oldValue = el.attr('data-oldvalue'),
        id = el.parents('.pfield').attr('id');
    
    if(el.attr('type') === 'checkbox') {
    	oldValue = oldValue == "true" ? true : false;
    	
    	if(el.prop('checked') === true) {
    		newValue = true;
    	} else {
    		newValue = false;
    	}
    } else {
    	newValue = el.val();
    }

    if(oldValue !== newValue) {
        $.getJSON(baseURI + '?action=set-property', {id: id, value: newValue}, function(response) {
            if(response == newValue) {
                removeTextEdit(el.parents('.property'), response, true);
            } else {
                removeTextEdit(el.parents('.property'), oldValue, false);
            }
        });
    } else {
        removeTextEdit(el.parents('.property'), oldValue);
    }
}


function changeFullname() {
	setTimeout(function() {
		$('#user-fullname').html($('#acadtitle').text() + '<br>' + $('#firstname').text() + ' ' + $('#lastname').text());
	}, 50);
}





        /*$.editable.addInputType('autogrow', {
            element : function(settings, original) {
                var textarea = $('<textarea />');
                if (settings.rows) {
                    textarea.attr('rows', settings.rows);
                } else {
                    textarea.height(settings.height);
                }
                if (settings.cols) {
                    textarea.attr('cols', settings.cols);
                } else {
                    textarea.width(settings.width);
                }
                $(this).append(textarea);
                return(textarea);
            },
            plugin : function(settings, original) {
                $('textarea', this).autogrow(settings.autogrow);
            }
        });
		$.i18n.setDictionary(eval("userprofile_language_" + i18n_language));
         var spinner = '<img src="'+ESI_ROOT+'/spinner.gif">';
         
         $('.pfield.TextLine, .pfield.ASCIILine').editable(function(value, settings) {
            $.getJSON(ajax_user_property+'?action=set-property', {id: $(this).attr('id'), value: value});
            
            return value;
         }, {
             type      : 'text', 
             indicator : spinner,
             tooltip   : $.i18n._('click_to_edit'),
             event: 'click',
             placeholder: "__________"
         });
         
         $('.pfield.Date').editable(function(value, settings) {
            $.getJSON(ajax_user_property+'?action=set-property', {id: $(this).attr('id'), value: value});
            
            return value;
         }, {
             type      : 'masked', 
             indicator : spinner,
             mask	   : '99.99.9999',
             tooltip   : $.i18n._('click_to_edit'),
             event: 'click',
             placeholder: "__.__.____"
         });
         
         $('.pfield.Text').editable(function(value, settings) {
            $.getJSON(ajax_user_property+'?action=set-property', {id: $(this).attr('id'), value: value});
            
            return value;
         }, {
             type      : 'textarea',
             indicator : spinner,
             tooltip   : $.i18n._('click_to_edit'),
             submit    : 'save',
             cancel    : 'cancel',
             event: 'click',
             placeholder: "__________"
         });
         
         $('.edit_area').editable(ajax_user_property, { 
             type      : 'textarea',
             cancel    : 'Cancel',
             submit    : 'OK',
             indicator : spinner,
             tooltip   : $.i18n._('click_to_edit'),
             placeholder: "__________"
         });*/
         
         
    // ----- ENDE --------------------------------------------------------------
//});


