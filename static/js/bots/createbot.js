

















function create_bot(){

    var form = document.getElementById("create_bot");
    var name = form.elements[0].value;
    var type = form.elements[1].value;
    var player = form.elements[2].value;

    $.get(
    "somepage.php",
    {'name' : name,
    'type' : type,
    'player': player,
    },

    function(data) {
       location.reload(true);
       // reload the page with updated info from the server
    }
);



}