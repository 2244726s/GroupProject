










$(document).ready(function(){
    $('#new_bot_name').on('change', validate_bot);
    $('#create_bot').on('click',create_bot);
    validate_bot();


});


function validate_bot(){
    var name = $('#new_bot_name').val();
    if(name.length > 0){

    $.ajax({
        type: 'GET',
        url: "/bots/validate_new_bot/",
        data:{
            'name':name
        },
        success: function(data){

            $('#create_bot_err').html(data);
        },


    });
    }else{
        $('#create_bot_err').html('please enter a name');
    }


}

function create_bot(){

    event.preventDefault();
    var name = $('#new_bot_name').val();
    alert(name)
    var type = $('#type_selector').find(':selected').val();
    alert(type)
    var csrf_token = $('#csrf').val();

    $.get(
        '/bots/create_bot/',
        {
            'name':name,
            'type':type,
        },
        function(data){
        $('create_bot_err').html(data);


        });


    /*
    $.ajax({

        type: 'POST',
        url: "/bots/create_bot/",
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
    */
}