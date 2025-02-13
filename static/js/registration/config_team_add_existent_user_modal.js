// Configuração JS team add existent user modal
 $(document).ready(function() {
        $('#add_existent_user_modal').on('hidden.bs.modal', function (e){
        $('#ajax_user_modal').html('');
        });
    });

    function ajax_register(user_id)
    {
        // Only fetch the information on the register modal.
        var $form = $('#register_form');

        // Send registration AJAX call to the server.
        var url = '/team_existent_user_register';
        const email = document.getElementById('id_email');
        if (email.value === ''){
            email.style.borderColor = "red";
            return null;
        }
        $.ajax( url, {
            data: {
               'email': $form.find('input[name="email"]').val(),
               'selected_organization': user_id,
               'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            type: 'POST',
            success: function(json_result) {
               // success code execution here
               if (json_result.status == "success")
               {
                    // Send the username & password now that it's in the
                    // registery and then login.
                   $('#add_existent_user_modal').modal('hide');
                   location.reload(true);
               }
               else
               {
                    //refresh_captcha();
                    // Make the hidden error box appear and display error.
                    print_error(json_result);
               }
            },
            error: function(xhr,status,error) {
                 const message_error = document.getElementById("error_box");
                 message_error.style.display = "block"
            },
            complete: function(xhr,status) {
               // completion code here
            }
        });
    }
