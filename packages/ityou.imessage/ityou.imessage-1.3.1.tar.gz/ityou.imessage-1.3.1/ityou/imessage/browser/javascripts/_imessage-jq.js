/* #LM Warum ist das ausgeschaltet worden ?
 * #MR es werden die javascripte aus dem esi.theme für imessage benutzt

$(document).ready(function () {
    	
    	var ESI_ROOT = $("#ESI_ROOT").text()
    	var ajax_messages = ESI_ROOT  + '/@@ajax-messages'

    	var anchor = document.location.hash;

		var NOTIFY_MESSAGES_REPEAT = parseInt($("#IMESSAGE_DELAY").text());
		var KEYCODE_ESC = 27;
		var KEYCODE_ENTER = 13;
    	var message_partner_id = $("#message-partner-id").attr('title');

    	
		function message_delete(mid) {
			//var ajax_messages = httpGet + '/@@ajax-messages'
			$.post(ajax_messages, {
				'action':	'message_delete',
				'mid':		mid,
				}, function(){} );	
		}
		
		function message_read(mid,state) {
			//var ajax_messages = httpGet + '/@@ajax-messages'
			$.post(ajax_messages, {
				'action':	state,
				'mid':		mid,
				}, function(){} );	
		}

		function message_control(context) {
		
			$("#message-partner-id").children().each(function() {
				if ( $("#message-partner-id").attr('title') == $(this).attr('title') ) {
					$(this).addClass('his-message')
				}			
			});
			
			$(".message-portrait").each(function() {
				if ( $("#message-partner-id").attr('title') != $(this).parent().parent().attr('title') ) {
					$(this).parent().parent().addClass("send")
				}			
			});
			
			$(".messages-all-button").click(function(e){
				e.preventDefault();
				$(this).hide();
				$(".messages-hideall-button").show();
				$(".messages-previous-button").show();
				$("#message-stream").find(".latest-messages").slideDown(999);
			})
			$(".messages-hideall-button").click(function(e){
				e.preventDefault();
				$(this).hide();
				$(".messages-previous-button").hide();
				$(".messages-all-button").show();    		
				$("#message-stream").find(".latest-messages").slideUp();
			})
			
			context.find(".message-hide-button").click(function (e) {
				e.preventDefault();
		    	$(this).parent().parent().slideUp();
		    	context.find('.messages-all-button').show();
		    });
		
			context.find(".message-read-button").click(function (e) {
				e.preventDefault();
				var message = $(this).parent().parent();
				var mid = message.attr("id");
				if ( message.hasClass("send") ) {
					var is_read = message_read(mid,"message_hidden_by_sender");
				} else {
					var is_read = message_read(mid,"message_read_by_receiver");
				};
		
				var message = $(this).parent().parent(); 
			    message.addClass('read-ok');
				message.delay(200).fadeOut(600);				
		
		    });
			
			context.find(".message-all-button").click(function (e) {
				e.preventDefault();
				$(this).hide();
				
		    	$(this).parent().prev().children().each(function() {
		    		$(this).slideDown(999);
		    	});
		    	$(this).parent().find(".message-hideall-button").show();
		    });
			
			context.find(".message-hideall-button").click(function (e) {
				e.preventDefault();
				$(this).hide();
		    	$(this).parent().prev().children().each(function() {
		    		$(this).slideUp();
		    	});
				$(this).parent().find(".message-all-button").show();
		    });
		
			context.find(".message-save-button").click(function (e) {
				e.preventDefault();
				var minput		= $(this).parent().find(".message-input-field");
		    	var message 	= minput.find(".nicEdit-main").html();
		
		    	var message_partner_id = $("#message-partner-id").attr('title');
		    	
		    	if(message_partner_id == '') {
		    	    message_partner_id = $('input#w_user_id').val();
		    	}
		
		    	var last_message = $(".latest-messages").find("li:last")
		    	var last_message_hash = last_message.attr('id');
		    	
		    	if (message) {
		    		//var ajax_messages = httpGet + '/@@ajax-messages'
		        	$.getJSON(ajax_messages, {
		    			'action':       'post_message',
		    			'message':		message, 
		    			'receiver_id': 	message_partner_id,
		    			'hash':			last_message_hash,
		    			},
		        		function(data) {
		        			if (data != '') {
	        			        
		        			    $('#message-partner-id').attr('title', data.receiver_id);
		        			    
		        			    if($('form[name="message_receiver"]').length > 0) {
		        			        $('form[name="message_receiver"]').hide();
		        			        
		        			        intervalImessage();
		        			        
		        			        context.find('.messages-previous-button').show();
		        			        context.find('.messages-hideall-button').show();
		        			        
		        			        context.find(".messages-previous-button").trigger('click');
	        			        }
		        			
		        				minput.find(".nicEdit-main").html("");
		        				if (data.hash != last_message_hash) {	        				
			        				var messages = $(".latest-messages");
		//        						.addClass('new-message')	        				
		        					$( "#message-tmpl" ).tmpl(data)
		        						.appendTo(messages)
		        						.slideDown(1000);
		        				} else {
		//        						.addClass('new-message')        					
		        					last_message.find(".message-text")
		        						.append('<div id="' + data.hash + '" >' + data.message + "</div>")
		        						.slideDown(1000);
		        					last_message.show();
		        		        	var last_message_timestamp_tag = last_message.find(".timestamp");	        					
									last_message_timestamp_tag.attr('id', data.timestamp);
									last_message_timestamp_tag.html(data.timestr);
		        				};
		        				
		        				$(".message-portrait").each(function() {
		        					if ( $("#message-partner-id").attr('title') != $(this).parent().parent().attr('title') ) {
		        						$(this).parent().parent().addClass("send")
		        					}			
		        				});
		        		    	context.find(".message-hide-button").click(function (e) {
		        					e.preventDefault();
		        		        	$(this).parent().parent().slideUp();
		        		    	});
		        		    	context.find(".message-delete-button").click(function (e) {
		        					e.preventDefault();
		        					var mid = $(this).parent().parent().attr("id");
		        					var is_deleted = message_delete(mid);
		        					$(this).parent().parent().fadeOut(1000);
		        		        });
		        		    	context.find(".message-read-button").click(function (e) {
		        					e.preventDefault();
		        					var mid = $(this).parent().parent().attr("id");
		        					var is_read = message_read(mid);
		        					$(this).parent().parent().fadeOut(1000);
		        		        });
		        		    	
		        		    	
		        			    //setTimeout(function() {
		        			    //    $('html,body').animate({scrollTop: $('ul.latest-messages').find('li').last().offset().top}, 'slow');
		        			    //}, 100);
		        					        				
		        			};
		        			
		    				//$(".message-input-field").find("textarea:last").focus();
							
		    			});
		    	};
		    });
		
			var portrait_link = $("#who-is-online").find(".bar-wrapper");
			var message_partner_id = $("#message-partner-id").attr('title');
			
	    	context.find(".messages-previous-button").click(function (e) {
				e.preventDefault();
	        	var oldest_message      = $("#message-partner-id").find("li:first");
	        	var timestamp			= oldest_message.find('.timestamp:first').attr('id');
	        	
	        	//ajax_messages = httpGet + '/@@ajax-messages'
	        	$.getJSON(ajax_messages, {
	        			'action':       'get_dialog',
	        			'sender_id': 	message_partner_id,
	        			'receiver_id':  'Me (DUMMY)',
	        			'timestamp':	timestamp
	        			},
	        		function(data) {
	        			if (data != '') {
	        				var messages = $(".latest-messages");
	    					$( "#message-tmpl" ).tmpl(data)
	    						.prependTo( messages )
								.attr('class','message jq-render jq-more-messages')
								.slideDown(500);
	    					    					
	    			    	$(".message-hide-button").click(function (e) {
	    						e.preventDefault();
	    			        	$(this).parent().parent().slideUp();
	    			    	});
	        		    	$(".message-delete-button").click(function (e) {
	        					e.preventDefault();
	        					var mid = $(this).parent().parent().attr("id");
	        					var is_deleted = message_delete(mid);
	        					$(this).parent().parent().fadeOut(1000);
	        		        });
	        		    	$(".message-read-button").click(function (e) {
	        					e.preventDefault();
	        					var mid = $(this).parent().parent().attr("id");
	        					var is_read = message_read(mid);
	        					$(this).parent().parent().fadeOut(1000);
	        		        });
	    			    	
	    					$("#message-partner-id").children().each(function() {
	    						if ( $("#message-partner-id").attr('title') == $(this).attr('title') ) {
	    							//$(this).css({'background-color':'#eaeae3'})
	    							//$(this).addClass('new-message')
	    						}			
	    					});
	    					
	    					
	        			};
	        			
	        			
	    				$(".message-portrait").each(function() {
	    					if ( $("#message-partner-id").attr('title') != $(this).parent().parent().attr('title') ) {
	    						$(this).parent().parent().addClass("send")
	    					}			
	    				});
	        			
	        			
	        	});
	        	        			         			
	        });
	
	    	context.find(".message-more-hide-button").click(function (e) {
					e.preventDefault();
	    			$(".previous-messages").slideUp("fast").slideDown(999);
	    			$(".previous-messages").children().remove();	
	    			$(".message-more-hide-button").hide();
	          });
	          
            if(message_partner_id != "") {
                context.find(".messages-hideall-button").show();
				context.find(".messages-previous-button").show();
			} else {
				context.find(".messages-hideall-button").hide();
				context.find(".messages-previous-button").hide();
			};
			
		}

    	    	
    	message_control($(this));


        function intervalImessage() {
            setInterval(function () {
				var ctimestamps = [];     
			    $(".timestamp").each(function() {
			        ctimestamps.push($(this).attr('id'));
		        });
			    latest_message_timestamp = ctimestamps.sort().reverse()[0];
	
	        	var last_message = $(".latest-messages").find("li:last");
	        	var last_message_hash = last_message.attr('id');
	        	var last_message_timestamp_tag = last_message.find(".timestamp");

	        	//ajax_messages = httpGet + '/@@ajax-messages'
				$.getJSON(ajax_messages, {
						'action'	:'get_messages',
						'sender_id' : message_partner_id,
						'timestamp'	: latest_message_timestamp,
						'newer'		: true
						},
					function(data) {
						if(data != '') {
							$.each(data, function(index,value) {
								if (value.hash != last_message_hash) {	 
									var messages = $(".latest-messages");
									//										.addClass('new-message')
									$( "#message-tmpl" ).tmpl(value)
										.appendTo(messages)
										.slideDown(1000);
								} else {
									last_message_timestamp_tag.attr('id', value.timestamp);
									last_message_timestamp_tag.html(value.timestr);
									last_message.find(".message")
										.replaceWith('<div class="message" >' + value.message + "</div>")
										.slideDown(1000);      					
								};
							});
							message_control( $(this ));
						};
					
				});       
				
			}, NOTIFY_MESSAGES_REPEAT);
        }


    	if (message_partner_id != "") {
    		intervalImessage();
    	};
        
        $(this).keypress(function(e) {
        	var form = $("#new-message-box > form");
        	
            if (e.which == KEYCODE_ESC) {
            	$("#new-message-box, #new-message-box-shadow").fadeOut();
            	form.find("#receiver-id, #new-message-textarea").val('');
            }
        });
        if (!anchor) {
        	$(".message-input-field").find("textarea:last").focus();
        }
        
        
        
        // === Multiple Receiver ========================
        
        var delayKeyUp = (function() {
            var timer = 0;
            return function(callback, ms) {
                clearTimeout(timer);
                time = setTimeout(callback, ms);
            };
        })();
        
        function imessageRemoveExistingUsers(arr, needle_arr) {
            if(needle_arr.length === 0 || arr.length === 0) {
                return arr;
            }

            var a = -1;
            $.each(arr, function(i, val) {
                if(needle_arr[0] === val.id) {
                    a = i;
                    return;
                }
            });

            if(a === -1) {
                needle_arr.splice(0, 1);
                return imessageRemoveExistingUsers(arr, needle_arr);
            } else {
                arr.splice(a, 1);
                needle_arr.splice(0, 1);
                return imessageRemoveExistingUsers(arr, needle_arr);
            }
        }
        
        
        $(document).delegate('input#w_user_name', 'keyup', function(e) {
            var obj = $(this)
                value = obj.val();
        
            if(value.length >= 2) {
                
                delayKeyUp(function() {
                    if(value.length >= 2) {
                        $.getJSON('@@ajax-imessage-users', {action:'query', q:value, l:5}, function(response) {
                            if(response.length > 0) {
                                var receiver_list = $('input#w_user_id').val().split(',');
                                response = imessageRemoveExistingUsers(response, receiver_list);
                            
                                // if input isnt focused, hide search popup
                                if($('input#w_user_name').is(':focus') === false) {
                                    $('form[name="message_receiver"] .input_holder').find('.usersearch').hide();
                                } else {
                                    $('form[name="message_receiver"] .input_holder').find('.usersearch').fadeIn('fast');
                                }
                                
                                $('form[name="message_receiver"] .input_holder').find('.usersearch > ul').empty();
                                
                                $('#imessage-dialog-usersearch-tmpl').tmpl(response).appendTo('form[name="message_receiver"] .input_holder > .usersearch > ul');
                                
                                // simulate click on the name if theres only one name and the input is the same as this name
                                if(response.length === 1 && $('#w_user_name').val().toLowerCase() == response[0].name.toLowerCase()) {
                                    $('form[name="message_receiver"] .input_holder > .usersearch li a').trigger('click');
                                }
                            }
                        });
                    } else {
                        $('form[name="message_receiver"] .input_holder > .usersearch').fadeOut('fast');
                        $('form[name="message_receiver"] .input_holder > .usersearch > ul').empty();
                    }
                }, 300);
                
            } else {
                $('form[name="message_receiver"] .input_holder > .usersearch').fadeOut('fast');
                $('form[name="message_receiver"] .input_holder > .usersearch > ul').empty();
            }
        
        });
        
        $(document).delegate('input#w_user_name', 'keydown', function(event) {
            if(event.keyCode === 13) {
                if($(this).val().length >= 2) {
                    $('form[name="message_receiver"] .input_holder > .usersearch ul').find('li').first().find('a').trigger('click');
                    $(this).trigger('blur');
                }
            }
        });
        
        $(document).delegate('input#w_user_name', 'focus', function() {
            if($(this).val().lengt >= 2) {
                $('form[name="message_receiver"] .input_holder > .usersearch').fadeIn('fast');
            }
        });
        
        $(document).delegate('input#w_user_name', 'blur', function() {
            $('form[name="message_receiver"] .input_holder > .usersearch').fadeOut('slow');
        });
        
        $(document).delegate('input#w_user_name', 'click', function() {
            if($(this).val().length >= 2) {
                $(this).trigger('keyup');
            }
        });
        
        $(document).delegate('form[name="message_receiver"] .input_holder > .usersearch li a', 'click', function(e) {
            e.preventDefault();
            
            var receiver_list = $('input#w_user_id').val().split(',');
            
            if($.inArray($(this).attr('title'), receiver_list) == -1) {
                var top_elem = $('form[name="message_receiver"] #receiver_list'),
                    img_elem = $(this).find('img'),
                    receiver_list_length = $('input#w_user_id').val().length,
                    data = {
                        portrait_url: img_elem.attr('src'),
                        portrait_width: img_elem.attr('width'),
                        prtrait_height: img_elem.attr('height'),
                        portrait_alt: img_elem.attr('alt'),
                        portrait_title: img_elem.attr('title'),
                        id: $(this).attr('title')
                    };
                    
                $('#imessage-basic-form-receiver-tmpl').tmpl(data).appendTo('form[name="message_receiver"] #receiver_list ul');
                
                if(receiver_list_length == 0) {
                    $('input#w_user_id').val($(this).attr('title'));
                } else {
                    $('input#w_user_id').val($('input#w_user_id').val()+','+$(this).attr('title'));
                }
            }
        });
        
        $(document).delegate('#receiver_list li .remove', 'click', function() {
            var user_id = $(this).parent().attr('id').split('imrcv-')[1],
                receiver_list = $('input#w_user_id').val().split(',');
            $.each(receiver_list, function(i, val) {
                if(val == user_id) {
                    receiver_list.splice(i, 1);
                }
            });
            
            receiver_list = receiver_list.join(',');
            
            $('input#w_user_id').val(receiver_list);
            $(this).parent().remove();
        });
        
        
    }
); 
  bkLib.onDomLoaded(function() {
        new nicEditor().panelInstance('message-textarea');
  });
*/
