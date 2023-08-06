$(document).ready(
	function () {
        // === ANFANG =======================================

        // ---------------------------------------------------------------------
        // Voting
        // uid: obj uid
        // sid: browser session id
        // ---------------------------------------------------------------------


        $('.fa-thumbs-o-up').off('click').on('click', function(){
            var voting_container = $(this).parent().parent()
            var uid = voting_container.attr('data-ityou-uid')
            var sid = voting_container.attr('data-ityou-sid') // $('#browser-session-id').text()
            $.post(
                '/voting', 
                {
                    'action':   'vote',
                    'vote':	    '1', 
                    'uid':	    uid,
                    'sid':      sid
                }, 
                function(counts_json) {
                    var counts = JSON.parse(counts_json)
                    voting_container.find('.vote-top').html(counts['top'])                    
                    voting_container.find('.vote-flop').html(counts['flop']) 
	            }
	        )	
        });

        $('.fa-thumbs-o-down').off('click').on('click', function(){
            var voting_container = $(this).parent().parent()
            var uid = voting_container.attr('data-ityou-uid')
            var sid = voting_container.attr('data-ityou-sid') // $('#browser-session-id').text()
            $.post(
                '/voting', 
                {
                    'action':   'vote',
                    'vote':	    '-1', 
                    'uid':	    uid,
                    'sid':      sid
                }, 
                function(counts_json) {
                    var counts = JSON.parse(counts_json)
                    voting_container.find('.vote-top').html(counts['top'])                    
                    voting_container.find('.vote-flop').html(counts['flop']) 
	            }
	        )	
        });
        
        // first loading
        
        //var voting_container = $('#voting-uid')
        $('.voting-container').each( function() {
            var voting_container = $(this) 
            $.post('/voting',
                {   
                    'action': 'get_votes',
                    'uid': voting_container.attr('data-ityou-uid')
                },
                function(counts_json) {
                    var counts = JSON.parse(counts_json)
                    voting_container.find('.vote-top').html(counts['top'])                    
                    voting_container.find('.vote-flop').html(counts['flop']) 
                }
            )


        })

		$("#follow-viewlet").find("a").click(function follow(e){
                e.preventDefault();
				$(this).append($("#kss-spinner").html());
				if($("#follow").is(":visible"))
				{
					add_or_remove = "false";
				}
				else if($("#unfollow").is(":visible"))
				{
					add_or_remove = "true";
				}
		        	$.getJSON("@@ajax-follow", {'action':"set_following", 'fid': $("#author_id").text(), remove : add_or_remove},
		        		function(data) {
		        			if (data) {
		        				$("#follow").toggle();
		        				$("#unfollow").toggle();
		        				$("#follow-viewlet").find("img").detach();
		        			};
		        	});
		});



        // === END ======================================
    }
); 



