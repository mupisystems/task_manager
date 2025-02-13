// Configuração JS da view em settings
function ajax_update_password()
{
    $('#update_password_btn').prop("disabled", true); // Lock button
    $.ajax( 'update_password', {
        data: {
           'csrfmiddlewaretoken': '{{ csrf_token }}',
           'password': $('#password').val(),
           'repeat_password': $('#repeat_password').val(),
           'old_password': $('#old_password').val(),
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
                reset_message_boxes();
                print_success(result.message);
                setTimeout(() => {
                    window.location = "/profile";
                }, 1000);
           }
        },
        error: function(xhr,status,error) {
           // error code here
        },
        complete: function(xhr,status) {
           // completion code here
           $('#update_password_btn').prop("disabled", false); // Unlock button
        }
    });
}

/**
* Prints a error box with the contents of the errors received from the server.
*/
function print_error(message)
{
$('#error_box').prop("hidden", false); // Display error box.

// Iterate through the JSON array of arrays and generate an error string.
var message = "<b>Error(s):</b><hr/>" + "<p>" + message + "</p>";

// Replace the error string with the contents of the error box.
$('#error_box').html(message);
}

function print_success(message)
{
$('#success_box').prop("hidden", false); // Display success box.

var message = "<p>" + message + "</p>";

$('#success_box').html(message);
}

function reset_message_boxes() {
$('#error_box').prop("hidden", true);
$('#success_box').prop("hidden", true);
}
