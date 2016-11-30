$(document).ready(function() {

    $.get("/niftyfifty", function(data){
        console.log(data);
    });
});
