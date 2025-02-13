// Configuração JS Base
window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-8ZJMG87M3S');



                /**
                 *  Function will call AJAX function to load the login modal.
                 */
            function ajax_logout()
            {
                var url = '/logout';

                $.ajax( url, {
                       data: {
                       'csrfmiddlewaretoken': '{{ csrf_token }}',
                       },
                       type: 'post',
                       success: function(result) {
                       // success code execution here
                       window.location = 'landpage';
                       },
                       error: function(xhr,status,error) {
                       // error code here
                       },
                       complete: function(xhr,status) {
                       // completion code here
                       }
                       });
            }