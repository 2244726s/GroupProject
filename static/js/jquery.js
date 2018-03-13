$(document).ready(event => {
	
	$("#menu").hide();
	$("#bots-wins").hide();
	$("#bots-value").hide();
	$("#robots").hide();
	
	$("#wins").on("click", event => {
		
	$("#bots-wins").show();
	$("#bots-value").hide();
	$("#robots").hide();
		
	})
	
	$("#value").on("click", event => {
		
	$("#bots-value").show();		
	$("#bots-wins").hide();	
	$("#robots").hide();
	})
	
	$("#play").on("mouseenter", event => {
		
	$("#menu").toggle();
	})
	
	$("#menu").on("mouseleave", event => {
		$("#menu").hide();		
	})
	
	$("#see-all-bots").on("click", event => {
		
	$("#bots-value").hide();		
	$("#bots-wins").hide();	
	$("#robots").show();
	
	})

	
	
	
});