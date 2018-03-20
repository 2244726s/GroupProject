$(document).ready(event => {
	
	$("#menu").hide();
	$("#bots-wins").hide();
	$("#bots-value").hide();
	$("#all-bots").show();
	
	$("#wins").on("click", event => {
		
	$("#bots-wins").show();
	$("#bots-value").hide();
	$("#all-bots").hide();
		
	})
	
	$("#value").on("click", event => {
		
	$("#bots-value").show();		
	$("#bots-wins").hide();	
	$("#all-bots").hide();
	})
	
	$("#play").on("mouseenter", event => {
		
	$("#menu").toggle();
	})
	
	$("#menu").on("mouseleave", event => {
		$("#menu").hide();		
	})
	
	$("#all").on("click", event => {
		
	$("#bots-value").hide();		
	$("#bots-wins").hide();	
	$("#all-bots").show();
	
	})

	
	
	
});