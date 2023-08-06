// =============== ANFANG ================================
$(document).ready(
    function () { 

    	var timer = 0;
    	var IMESSAGE_DELAY = parseInt($("#IMESSAGE_DELAY").text());
    	//var IMESSAGE_DELAY = 6000 // Initialwert, wird während der Laufzeit durch $("#IMESSAGE_DELAY") ersetzt

    	var ESI_ROOT = $("#ESI_ROOT").text()
    	var ajax_messages  = ESI_ROOT  + '/@@ajax-messages'
    	var imessages_ajax = '@@imessage-ajax'
		
		function show_message_portlet() { 
		    // empty box: 35	
			if (    $(".portlet").find("#imessage-sender").length    ) {
			    if ( $("#imessage-sender").html().length > 40  ) {
			        $("#imessage-sender").parent().parent().fadeIn();
			    } else {
			        $("#imessage-sender").parent().parent().hide();
			    }
			}
		}
		
		function imessagesender(e) {
		
		    function message_read(mid,state) {
		        $.post(ajax_messages, {
			        'action':	state,
			        'mid':		mid
			        },function(){} );
			}
			// hoverintent ---	
		    var config = {                   
		        over: function() {
				//-------------------------------------------
		            // stop ajax requests
		            if(timer) {
		                clearTimeout(timer);
		                timer = null
		                };                  
		            $(this).find(".imessage-sender-box, #imessage-sender .arrow-top").fadeIn(200);
		
			        // reset    
		            $(this).find(".read-ok").each( function() {
						$(this).removeClass("read-ok");
						$(this).parent().parent().find(".message").removeClass('read-ok');
						$(this).parent().parent().show();
						$(this).parent().find(".read").show();
					})			        
					
					// mark as read
		            $(".imessage-sender-box").find(".read").click( function(e) {
						e.preventDefault();
		                var mid = $(this).parent().parent().attr("id");
						//message_read() is defind in imessage.js
		                var is_read = message_read(mid,'message_read_by_receiver');		
								
					    $(this).addClass('read-ok');
					    $(this).parent().parent().find(".message").addClass('read-ok');
						$(this).parent().parent().delay(400).fadeOut(1000);				
		            });
								
					// goto message
					$(".imessage-sender-box").find(".message").click( function() {
						var message_partner_id  = $(this).parent().parent().parent().attr("id");
						var message_id          = $(this).parent().parent().children(":first-child").attr("id");
				        var anchor              = self.document.location.hash;       
		
						var url = "@@messages?sid=" + message_partner_id  + "#" + message_id;
						
						$(window).attr("location",url);
					});
					
		        },
		        out: function() {
				//-------------------------------------------
		            timer = setInterval(function () {
				        imessagesender();
		            }, IMESSAGE_DELAY);
		             $(this).find(".imessage-sender-box, #imessage-sender .arrow-top").fadeOut(200);
		        },               
		        timeout: 400, // number = milliseconds delay before onMouseOut
		        interval: 200,
		        sensitivity:10    
		    };
		    	
		    // ---- imessagesender -----------
            // Wird das noch gebraucht ?
/*            
		    $.ajax({
		        url: imessages_ajax,
		        type: 'POST',
		        dataType: 'html',     
		        timeout: 1000,
		        error: function(){
		            $("#debug-imessage").html("IMessage-DB not readable").show();
		        },
		        success: function(imessage_sender_response){
		        	// 	--- xml in box anzeigen
		        	imessage_sender = imessage_sender_response;
		            if (imessage_sender.length > 10 ) { // > 0 fails because plone sents white space !!!
		            	$(".portletInstantMessages").slideDown(300, function() {
		               		$("#imessage-sender").html( imessage_sender ).fadeIn(800)
		            	});
		            } else {
		            	$(".portletInstantMessages").hide();
		            };
								
					$("#imessage-sender").find(".portrait").hoverIntent(config);
					show_message_portlet();
					
		        }
		    });	    
*/		        
		}
		// --- end notify -------------------            



                        
        // === BEGIN ====================================
    	
        
        imessagesender();
        
    	// --- imessage-sender ----------
  	    if ( $("#imessage-sender").length > 0  ) { 
            timer = setInterval(function() {
                imessagesender();
            }, IMESSAGE_DELAY) // refresh every X000 milliseconds
        };
        //show_message_portlet();
				
        // --- /imessage-sender ---------

        
        
        // === END ======================================
    }
); 



