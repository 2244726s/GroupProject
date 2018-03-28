










$(document).ready(function(){
    $('#new_bot_name').on('change', validate_bot);
    $('#create_bot').on('click',create_bot);
    validate_bot();


});


function validate_bot(){
    // whenever a new name is entered, send it to the validate view, then render the response underneath the text box
    var name = $('#new_bot_name').val();
    if(name){

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
    // creates a new robot given a name and type.
    event.preventDefault();
    // stops a form automatically submitting
    var name = $('#new_bot_name').val();
    var type = $('#type_selector').find(':selected').val();

    $.get(
        '/bots/create_bot/',
        {
            'name':name,
            'type':type,
        },
        function(data){
            alert('new robot created, please refresh the page');
            $('create_bot_err').html(data);


        });


}