function clickUpgrade() {
	// vars holding info for the stat increase
		var botId;
		var stat;
		// extract data from button
		bot_name= $(this).attr("data-botid");
		stat = $(this).attr("data-stat");
		// make get request to /bots/upgrade encoding the data


		$.ajax({
		    type: "GET",

		    url: '/bots/upgrade/',
		    data:{'bot_name': bot_name, 'stat':stat},

		    success: function(data) {
			    // update robot table
			    $('#bot_table').html(data);
    			// reassign click listener
	    		$('.stat-increase').on('click',clickUpgrade);
	    		// end of ajax function
		    },



        });



        /*
		$.get('/bots/upgrade/', {bot_id : botId, stat:stat}, function(data) {
			// update robot table
			$('#bot_table').html(data);
			// reassign click listener
			$('.stat-increase').click(clickUpgrade);

			// end of ajax function
		});
		*/
	// end of click listener
}
$(document).ready(function() {

	// assign click listener for stat increase buttons
	$('.stat-increase').on('click',clickUpgrade);

 $('.select_bot').on('change',displayBot);
    displayBot();
// end of ready
});


function displayBot(){

    var name = $('#select_bot').find(':selected').text();
    /*$.get('/bots/get_bot/', {'bot_name': name}, function(data){

        $('#bot_table').html(data);
        $('.stat-increase').on('click',clickUpgrade);
    });
    */

    $.ajax({
        type: "GET",
        url: "/bots/get_bot/",
        data: {'bot_name': name},
        success: function(data){

            $('#bot_table').html(data);
            $('.stat-increase').on('click',clickUpgrade);
        },


    });
}
