










$(document).ready(function(){

    $('#CreateBot').on('submit',create_bot);


});




function create_bot(){

    event.preventDefault();
    var form = document.getElementById("CreateBot");
    var name = form.elements[0].value;
    var type = form.elements[1].value;
    var player = form.elements[2].value;






    $.ajax({

        type: 'POST',
        url: "/bots/create_bot/",
        dataType:"json",
        data: {
        'name':name,
        'type':type,
        },
        success: function(data) {
        $('#create_bot').html(data.msg);
        if( $('#create_bot').html() == 'valid'){
            //location.reload(true);
            // reload the page with updated info from the server
        }

    },

    });
}