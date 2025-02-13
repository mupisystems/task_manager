//Configuração JS da view em profile
function ajax_update_user()
{
    $('#update_user_btn').prop("disabled", true); // Lock button
    $.ajax( 'update_user', {
        data: {
           'csrfmiddlewaretoken': '{{ csrf_token }}',
           'full_name': $('#id_full_name').val(),
           //'last_name': $('#id_last_name').val(),
           'email': $('#id_email').val(),
           'selected_organization': $('#id_selected_organization').val()
        },
        type: 'post',
        success: function(result) {
           // success code execution here
           if (result.status != 'success')
           {
                print_error(result.message);
           }
           else
           {
                window.location = "";
           }
        },
        error: function(xhr,status,error) {
           // error code here
        },
        complete: function(xhr,status) {
           // completion code here
           $('#update_user_btn').prop("disabled", false); // Unlock button
        }
    });
}

/**
* Prints a error box with the contents of the errors received from the server.
*/
function print_error(json_result)
{
$('#error_box').prop("hidden", false); // Display error box.

// Iterate through the JSON array of arrays and generate an error string.
var message = "<b>Error(s):</b><hr/>";
var data = $.parseJSON(json_result)
for (var key in data) {
    if (data.hasOwnProperty(key)) { // this will check if key is owned by data object and not by any of it's ancestors
        message += "<p>" + key + ": " + data[key] + "<p>";
    }
}

// Replace the error string with the contents of the error box.
$('#error_box').html(message);
}
