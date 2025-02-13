// Configuração JS index menu em service
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

  var firebaseConfig = {
    apiKey: "AIzaSyC1Zc4pQe-oASQW1mYvCbc3nIR39ACLXUQ",
    authDomain: "notificaclientes-1959a.firebaseapp.com",
    projectId: "notificaclientes-1959a",
    storageBucket: "notificaclientes-1959a.appspot.com",
    messagingSenderId: "620362868560",
    appId: "1:620362868560:web:ebc9b34193ec981c42ae55",
    measurementId: "G-5XHN9KJEXD"
  };
  // Initialize Firebase

    firebase.initializeApp(firebaseConfig);
    firebase.analytics();

    const messaging =  firebase.messaging();

messaging.requestPermission().then(function(){
    return messaging.getToken();
}).then(function(token){
    ajax_func(token);
}).catch(function(err){
    ajax_func('');
});


function ajax_func(token){
fetch('ajax_device_token', {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: token,
        })
    }).then(function (response) {
        return response.json();
    })
        .then(function (data) {
            console.log(data);
        })
        .catch(function (err) {
        })

    }
messaging.onMessage(function(payload){
    console.log('onMessage: ', payload)
});