$(document).ready(function() {

		function table_draw_todo(uid, wf_event) {
			if (uid != null & wf_event != null){
				link = "@@todo-table?uid=" + uid + "&wf_event=" + wf_event;
			}
			else {
				link = "@@todo-table";
			}

  	      	var table_creating_todo = $('#todo-table').dataTable( {
					"bProcessing": true,
					"bDestroy": true,
					"sAjaxSource": link,
					"aaSorting": [[5, "desc"]],
					"aoColumnDefs": [
    					{ "sClass": "sender_id",
                          "bSortable": false,       "aTargets": [0] },					
    					{ "sClass": "sender",       "aTargets": [1] },
                        { "sClass": "url",          "aTargets": [2],
                           "fnRender": function(obj) {
                                var url   = obj.aData[2].url;
                                var task  = obj.aData[2].task;
                                return  '<b><a href="'+url+'">' + task + '</a></b>';
                           }
                        },    					
    					{ "sClass": "description",  "aTargets": [3] },
    					{ "sClass": "update",       "aTargets": [4] },
    					//{ "sClass": "deadline",     "aTargets": [5] },
    					
                        { "sClass": "state",        "aTargets": [5],
                           "fnRender": function(obj) {
                                var options = obj.aData[5][0].options;
                                var review_state = obj.aData[5][1];
                                var form_select = '<select name = "available_states" class = "available_states">#OPTIONS</select>';
                                var form_options = '<option value="do_nothing"> --- </option>';
                                                                 
                                for (var i in options) {
                                    form_options = form_options + '<option value="' + options[i].id + '">' + options[i].title + '</option>';
                                };                                
                                form = form_select.replace("#OPTIONS",form_options);
                                return  review_state + "\n" + form;
                           }
                        },
        				{ "sClass": "uid",          "aTargets": [6] },                        
        				//{ "sClass": "priority",     "aTargets": [8] }
                        
    				],
    				
					"bAutoWidth": false,
					"oLanguage": {
						"sProcessing":   '<img src="/spinner.gif" alt="">',
						"sLengthMenu":   "_MENU_ Einträge anzeigen",
						"sZeroRecords":  "Keine Einträge vorhanden.",
						"sInfo":         "_START_ bis _END_ von _TOTAL_ Einträgen",
						"sInfoEmpty":    "0 bis 0 von 0 Einträgen",
						"sInfoFiltered": "(gefiltert von _MAX_  Einträgen)",
						"sInfoPostFix":  "",
						"sSearch":       "Suchen",
						"oPaginate": {
							"sFirst":    "Erster",
							"sPrevious": "Zurück",
							"sNext":     "Nächster",
							"sLast":     "Letzter"
						}
					},
					"fnDrawCallback" : 	function() {
						$(".priority").each(function() {
							$(this).addClass("prio" + $(this).html());
							$(this).contents().wrap("<div class='prio' />")
						});

						$(".available_states").change(function(event) {
						    event.preventDefault();
						    var uid       = $(this).parent().parent().find(".uid").html();
						    var wf_event  = $(this).val();
						    table_draw_todo(uid, wf_event);
						})
					}
			})	
			table_creating_todo.fnDraw();
		};
		
		table_draw_todo(uid = null, wf_event = null);
} )
