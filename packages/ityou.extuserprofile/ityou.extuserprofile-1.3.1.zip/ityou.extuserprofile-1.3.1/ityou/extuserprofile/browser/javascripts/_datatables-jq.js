$(document).ready(function () {
	// --- ANFANG --------------------------------------------------------------
	var ESI_ROOT = $("#ESI_ROOT").text()
	var ajax_users_datatable = ESI_ROOT + '/@@ajax-users-datatable'

    function table_draw(group_id) {    
		var link = ajax_users_datatable + "?g=" + group_id;
      	var user_table = $('#user-table');
      	/*var table_creating = user_table.dataTable({
      		"bProcessing": true,
      		"bDestroy": true,
      		"sAjaxSource": link,
      		"aoColumnDefs": [{
      			"bSortable": false,
      			"aTargets": [0]
      		}, {
      			"sClass": "portrait",
      			"aTargets": [0],
      			"fnRender": function(obj) {
      				var url   = "/author/" + obj.aData[6];
                    var img = obj.aData[0];
                    return '<span title=""><a href="' + ESI_ROOT + url + '" class="user-portrait" data-uid="' + obj.aData[6] + '">' + img + '</a></span>';
               }
      		}],
            "aaSorting": [[1, "asc"]],
            "bAutoWidth": false,
            "oLanguage": eval("lang_" + $('html').attr("lang").slice(0,2))
        });
        table_creating.fnClearTable(true);
        */
      	
      	$.ajax({
            url: '@@ajax-whoisonline',
            data: {
                time_client: (new Date()).getTime() / 1000
            },
            dataType: 'json',
            timeout: 30000,
            // event handler success
            success: function(response) {
            	var table_creating = user_table.dataTable({
              		"bProcessing"	: true,
              		"bDestroy"		: true,
              		"sAjaxSource"	: link,
              		"aoColumnDefs"	: [{
              			"sClass"	: "recent_time hidden",
              			"aTargets"	: [0],
              			"fnRender"	: function(obj) {
              				return inResponse(response, obj.aData[8]);
              			}
              		}, {
              			"bSortable"	: false,
              			"sClass"	: "portrait", 
          				"aTargets"	: [1],
          				"fnRender"	: function(obj) {
          					var url = "/author/" + obj.aData[8];
          					var img = obj.aData[1];
          					return '<span title=""><a href="' + ESI_ROOT + url + '" class="user-portrait" data-uid="' + obj.aData[8] + '">' + img + '</a></span>';
          				}
              		}, {
              			"aTargets"	: [2],
              			"sClass"	: "fullname"
              		}, {
              			"aTargets"	: [3],
              			"bSortable"	: false,
              			"sClass"	: 'send-message',
              			"fnRender"	: function(obj) {
              				return '<a href="' + ESI_ROOT + '/@@messages?sid=' + obj.aData[8] + '" class="btn btn-default"><i class="fa fa-envelope-o"></i></a>';
              			}
              		}, {
              			"aTargets"	: [4],
              			"sClass"	: "position"
              		}, {
              			"aTargets"	: [5],
              			"sClass"	: "mobile"
              		}, {
              			"aTargets"	: [6],
              			"sClass"	: "location"
              		}, {
              			"aTargets"	: [7],
              			"sClass"	: "lastlogin",
              			"fnRender"	: function(obj) {
              				var t = new ClientTimezone();
              				return '<span class="hiddenStructure">' + obj.aData[7][1] + '</span><span>' + t.convertTime(obj.aData[7][0]) + '</span>';
              			}
              		}],
              		"aaSorting"		: [[0, "desc"]],
              		"bAutoWidth"	: false,
              		"oLanguage"		: eval("lang_" + $('html').attr("lang").slice(0,2)),
              		"iDisplayLength" : 50,
              	});
            	
            	table_creating.fnClearTable(true);
            }
        });
    }

    table_draw("");

    $("#group-portlet").find(".group").click(function () {
        if ($(this).hasClass('active') ) {
	        $(this).removeClass('active');
   		    table_draw("");
        } else {
            $("#group-portlet").find(".group").removeClass('active');
            $(this).toggleClass('active');
   		    table_draw( $(this).attr("id"));
        };
    });

// ----- ENDE --------------------------------------------------------------

}); 


function inResponse(data, val) {
	var x = 0;
	
	if($('#ESI_DATA').data('ityou-uid') == val) {
		x = parseInt((new Date()).getTime()/1000);
	} else {
		$.each(data, function(k, v) {
			if(v.id === val) {
				x = v.recent_time;
				return ;
			}/* else if($('#ESI_DATA').data('ityou-uid') === val) {
				x = parseInt((new Date()).getTime()/1000);
				return ;
			}*/
		});
	}

	return x;
}