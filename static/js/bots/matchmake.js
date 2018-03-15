function setTeam(i){


    return function(){

        //sets a team with i elements
        //uses jquery to retrieve information about the selected team
        //uses ajax to validate the team serverside
        //returns either a list of matches or an error message

        var bots = {}
        for(j = 0; j < i; j++){
            bots['b'+j.toString()] = $('#' + i.toString() +'v' +i.toString() + '_' + j.toString()).find(':selected').html();

        }
        bots['size'] = i;
        bots['name'] = $('#username').html();

        $.ajax({
        type: "GET",
        url: "/bots/matchmake/",
        data: bots,
        success: function(data){

            $('#' + i.toString() +'v' +i.toString() + '_complete').html(data);
            $('#' + i.toString() + 'v' +i.toString() + '_update_team').on('click',updateTeam(i));
            $('#' + i.toString() + 'v' +i.toString() + '_find_game').on('click',setTeam(i));
        },


        });


    }

}


function updateTeam(i){

    return function(){
        //replaces content with i select boxes so that a team can be selected

        var bots = {}
        for(j = 0; j < i; j++){
            bots['b' + j.toString()] = $('#' + i.toString() +'v' +i.toString() + '_' + j.toString()).html();

        }
        bots['size'] = i;
        bots['name'] = $('#username').html;
        $.ajax({
        type: "GET",
        url: "/bots/update_team/",
        data: bots,
        success: function(data){

            $('#' + i.toString() +'v' +i.toString() + '_complete').html(data);
            $('#' + i.toString() + 'v' +i.toString() + '_find_game').on('click',setTeam(i));
            $('#' + i.toString() + 'v' +i.toString() + '_update_team').on('click',updateTeam(i));
        },


        });


    }

}



$(document).ready(function(){

    $.ajax({
       type: 'GET',
       url: "/bots/initialize/",
       data: {
        'size':1,
        'name':$('#username').html(),
       },
       success: function(data){

           $('#1v1_complete').html(data);
           $('#1v1_find_game').on('click',setTeam(1));
           $('#1v1_update_team').on('click',updateTeam(1));
       },


    });

    $.ajax({
       type: 'GET',
       url: "/bots/initialize/",
       data: {
        'size':3,
        'name':$('#username').html(),
       },
       success: function(data){

           $('#3v3_complete').html(data);
           $('#3v3_find_game').on('click',setTeam(3));
           $('#3v3_update_team').on('click',updateTeam(3));
       },


    });

    $.ajax({
       type: 'GET',
       url: "/bots/initialize/",
       data: {
        'size':5,
        'name':$('#username').html(),
       },
       success: function(data){

           $('#5v5_complete').html(data);
           $('#5v5_find_game').on('click',setTeam(5));
           $('#5v5_update_team').on('click',updateTeam(5));
       },


    });

    //document.write($('#username').text());
});