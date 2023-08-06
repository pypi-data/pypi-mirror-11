$(document).ready(function() {

    // --- ANFANG --------------------------------------------------------------


	//var ESI_ROOT = $("#ESI_ROOT").text()
	var ESI_ROOT = $('#ESI_DATA').data('ityou-portal-url');
	var ajax_crop_portrait  = '/@@crop-portrait'
	var ajax_personal_images = ESI_ROOT + '/@@ajax-personal-images'
	
	$('#user-fullname').html($('#acadtitle').text() + '<br>' + $('#firstname').text() + ' ' + $('#lastname').text());

    // vollständigen namen anzeigen 
    /*
     * ausgelagert in userprofile-editable-jq.js
     * 
    $('#user-fullname').html(  $('#acadtitle').text() + '<br />' + $('#firstname').text() + ' ' + $('#lastname').text()  )

    $('#acadtitle').on('change', 'input', function() {
        $('#user-fullname').html(  $('#acadtitle > input').val() + '<br />' + $('#firstname').text() + ' ' + $('#lastname').text()  )
    })
    $('#firstname').on('change', 'input', function() {
        $('#user-fullname').html(  $('#acadtitle').text() + '<br />' + $('#firstname > input').val() + ' ' + $('#lastname').text()  )
    })
    $('#lastname').on('change', 'input', function() {
        $('#user-fullname').html(  $('#acadtitle').text() + '<br />' + $('#firstname').text() + ' ' + $('#lastname > input').val()  )
    })*/
    

    


	/*function crop_portrait(str) {
		param_str = str;
	    str_to_remove = str.split("/").splice(-1, 1);
	    $.i18n.setDictionary(eval("userprofile_language_" + i18n_language));
	    
	    console.log("crop portrait");
	    
	    $(".crop_portrait").dialog({
		    modal: true,
		    title: $.i18n._('crop_image'),
		    width: "auto",
		    height: "auto",
		    position: {
	    		my: "center",
	    		at: "center"
		    },
		    open: function(event, ui){
			    d = $(this);

			    $(this).load(str.replace(str_to_remove, "") + ajax_crop_portrait, function() {
			        $("#save").click(function() {
				    	$("#save").hide();
				    	$(".crop_portrait").append($("#kss-spinner").html());
				    });
			    });
		    },
		    close: function() {
		    	//$(".crop_portrait").dialog("destroy");
				$(".thumb").click(function() {
				    crop_portrait(param_str);
			    });
		    }
	    });
	}*/
	


	/*$("#portrait.True").click(function() {
		
		console.log("click");
		
	    $.getJSON(ajax_personal_images, function(data) {
			
			$('#upload-image-wrapper a').prepOverlay({
			    subtype: 'ajax',
			    filter: '#content > *',
			    formselector: 'form',
			    closeselector: '[name="form.button.cancel"]',
			    afterpost: function(e, overlay) {
			        var imgSrc;
			        
		            var imgFound = setInterval(function() {
		                imgSrc = overlay.find('#content-core').find('img').attr('src');
		                
		                if(imgSrc != undefined && imgSrc != '') {
		                    $('#thumb-tmpl').tmpl({url: (imgSrc.replace(imgSrc.split("/").splice(-1, 1), ""))}).appendTo('.window');
		                
		                    overlay.find('.close').find('a').trigger('click');
		                    crop_portrait(imgSrc);
		                    
		                    clearInterval(imgFound);
	                    }
		            }, 1);
			    }
			});
			
	    	$(".thumb").detach();
		    $( "#thumb-tmpl" ).tmpl(data).appendTo(".window");
		    $(".thumb").click(function(){crop_portrait($(this).find("img").attr("src"));});
		    
		    $.i18n.setDictionary(eval("userprofile_language_" + i18n_language));

		    $(".window").dialog({
				width: 592,
				title: $.i18n._('choose_image'),
				close: function(){
					$(".window").dialog("destroy");
				}
	    	});

		});
	});*/
	
	$(document).on('click', '#portrait.True', function() {
		var c = $('#eup-thumbnail-modal').find('.modal-body');
		
		$('#eup-thumbnail-modal').modal({
			backdrop: true
		});
		
		$.getJSON(ajax_personal_images, function(response) {
			if(response.length > 0) {
				$('#no-images-uploaded').hide();
			}
			
			$('#upload-image-wrapper a').prepOverlay({
				subtype: 'ajax',
				filter: '#content > *',
				formselector: 'form',
				closeselector: '[name="form.button.cancel"]',
				afterpost: function(e, overlay) {
					var imgSrc;
					
					var imgFound = setTimeout(function() {
						imgSrc = overlay.find('#content-core').find('img').attr('src');
						
						if(imgSrc != undefined && imgSrc != '') {
							$($('#thumbnails-tmpl').render({url: (imgSrc.replace(imgSrc.split("/").splice(-1, 1), ""))})).appendTo(c);
							
							overlay.find('.close').find('a').trigger('click');
							crop_portrait(imgSrc);
						}
					}, 50);
				}
			});
			
			c.find('.thumb').detach();
			$($('#thumbnails-tmpl').render(response)).appendTo(c);
		});
	});
	
	$('#eup-thumbnail-modal').on('click', '.thumb', function() {
		crop_portrait($(this).find('img').attr('src'));
	});
	
	$('#eup-crop-modal').on('click', '.modal-footer #save-crop', function() {
		var text = $('#save-crop').text();
		
		$('#save-crop').html('<i class="fa fa-spinner fa-spin"></i>').prop('disabled', true);
	});
	
	function crop_portrait(str) {
		param_str = str;
	    str_to_remove = str.split("/").splice(-1, 1);
	    //$.i18n.setDictionary(eval("userprofile_language_" + i18n_language));
	    
	    $('#eup-crop-modal').modal({
	    	backdrop: true
	    });
	    
	    $('#eup-crop-modal').on('shown.bs.modal', function(e) {
	    	var t = $(this).find('.modal-body');
	    	
	    	t.load(str.replace(str_to_remove, "") + ajax_crop_portrait, function() {});
	    });
	    
	    $('#eup-crop-modal').on('hidden.bs.modal', function(e) {
	    	$(this).find('.modal-body').empty();
	    });
	}
    
    
    // ----- ENDE --------------------------------------------------------------
	
	//console.log(window.innerWidth > 0 ? window.innerWidth : screen.width);
});


