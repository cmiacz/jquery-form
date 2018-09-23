$(document).ready(function() {
    $("form").submit(function(e){
        var form = $(this);
        $.ajax({ 
            url   : form.attr("action"),
            type  : form.attr("method"),
            contentType: 'application/json;charset=UTF-8',
            // TODO: schedule serialization
            data  : JSON.stringify({ 
                "2018-09-01": {
                    "from": "8:00",
                    "to": "16:00"
                },
                "2018-09-02": {
                    "from": "9:00",
                    "to": "17:00"
                },
            }), 
            success: function(response){
                alert(response);
            }
        });
        return false;
     });
});

