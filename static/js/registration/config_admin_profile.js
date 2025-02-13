// Configuração JS admin profile
function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie('csrftoken');
        const searchValue = document.getElementById('id_email_existent'); //Id do email do usuário existente
        const alert = document.querySelector('.alert-information');
        const modal_existent_user = document.querySelector('#modal_add_existent_user');
        const error_messages = document.querySelector('#error-messages');
        const success_messages = document.querySelector('#success-messages');

        function ajax_user_modal() {
            error_messages.style.display = "none";
            success_messages.style.display = "none";
            fetch('/settings/admin/team_existent_user_register/', {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: searchValue.value,
                })
            }).then(function (response) {
                return response.json();
            })
                .then(function (data) {
                    if (data['status'] === 'error'){
                        error_messages.style.display = "block";
                        success_messages.style.display = "none";
                    }else{
                        success_messages.style.display = "block";
                        error_messages.style.display = "none";
                    }

                })
                .catch(function (err) {
                })

        }

    function clen_messages(){
        error_messages.style.display = "none";
        success_messages.style.display = "none";
    }