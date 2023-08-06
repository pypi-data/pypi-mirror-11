/*$(document).ready(function () {

	var jcrop_api;
	var options = {
		minSize: [150, 200],
		maxSize: [600, 800],
		aspectRatio: 0.75,
		setSelect: [ 100, 100, 250, 300 ]
    };
				  
    $('#target').Jcrop(options,function() {
        jcrop_api = this;
        
        console.log(this);
        
        $("#save").show();
        $("#save").click(function() {
	        c = jcrop_api.tellSelect();
	        img_url = $(".jcrop-holder").find("img").attr("src");
	        $.getJSON(img_url + "/@@crop-portrait", {'action':'crop', 'x':c.x, 'y':c.y, 'w':c.w, 'h':c.h},
		        function(data) {
		            location.reload(true);
		        }
	        );
        });
    });

});
*/


$(function() {
	var ratio = 768 / 200;
	var jcrop_api,
		options = {
			/*minSize: [150, 200],
			maxSize: [600, 800],*/
			aspectRatio: 0.75,
			setSelect: [10, 10, 150, 150]
		};
	
	$('#target').Jcrop(options, function() {
		jcrop_api = this;
		
		$('#save-crop').click(function() {
			var c = jcrop_api.tellSelect();
			
			var d = {
					action: 'crop',
					x: c.x,
					y: c.y,
					w: c.w,
					h: c.h
				};
			
			img_url = $('.jcrop-holder').find('img').attr('src');
			img_url = img_url.replace(img_url.split("/").splice(-1, 1), "image_large")
			
			$.getJSON(img_url + "/@@crop-portrait", d, function(response) {
				location.reload(true);
			});
		});
	});
});