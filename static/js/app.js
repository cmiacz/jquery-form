function getFormData() {
    var data = {};
    $("tr.time-entry").each(function() {
        var date = $(this).find("input[name='date']").val();
        var timeFrom = $(this).find("input[name='time-from']").val();
        var timeTo = $(this).find("input[name='time-to']").val();
        data[date] = {"from": timeFrom, "to": timeTo}
        console.log(date);
    });
    return data;
}


$(document).ready(function() {
    $("form").submit(function(e){
        var form = $(this);
        $.ajax({ 
            url   : form.attr("action"),
            type  : form.attr("method"),
            contentType: 'application/json;charset=UTF-8',
            data  : JSON.stringify(getFormData()), 
            success: function(response){
                alert(response);
            }
        });
        return false;
     });
});

