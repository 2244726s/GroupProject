function clickUpgrade() {
	// vars holding info for the stat increase
		var botId;
		var stat;
		// extract data from button
		botId= $(this).attr("data-botid");
		stat = $(this).attr("data-stat");
		// make get request to /bots/upgrade encoding the data
		$.get('/bots/upgrade/', {bot_id : botId, stat:stat}, function(data) {
			// update robot table
			$('#bot-table').html(data);
			// reassign click listener
				$('.stat-increase').click(clickUpgrade);

			// end of ajax function
		});
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

    var id = $('option:selected', this).val();
    $.get('/bots/get_bot/', {bot_id : id}, function(data){

        $('#bot_table').html(data);
        $('.stat-increase').click(clickUpgrade);
    });
}