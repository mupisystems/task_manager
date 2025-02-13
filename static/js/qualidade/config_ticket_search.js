// Configuração JS ticket search
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

    const textSearch = document.getElementById("text-search");
    const selectChoices = document.getElementById("select-itens-choices")
    const selectPriority = document.getElementById("select-itens-priority")
    const tbody = document.getElementById("table-body")

    function ajax_func() {
        const textValue = textSearch.value
        const selectValue = selectChoices.value
        const selectPriorityValue = selectPriority.value
        fetch('', {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                searchText: textValue,
                selectValue: selectValue,
                selectPriorityValue: selectPriorityValue,
            })
        }).then(function (response) {

            return response.json();
        })
            .then(function (data) {
                var result = "{{ data|safe  }}"
                tbody.innerHTML = '';
                data.forEach(ticket => {
                    let dateCreated = new Date(ticket.fields['created']).toLocaleDateString()
                    let dueDate = new Date(ticket.fields['due_date']).toLocaleDateString()


                    tbody.innerHTML += `
                    <tr>
                                    <td> ${ticket.fields['queue']} </td>
                                    <td> ${ticket.fields['title']} </td>
                                    <td> ${dateCreated}</td>
                                    <td> ${ticket.fields['priority']}</td>
                                    <td> ${ticket.fields['status']}</td>
                                    <td> ${ticket.fields['assigned_to']}</td>
                                    <td> ${dueDate}</td>

                                    <td><a href="/adm/ticket/${ticket.fields['secret_key']}"><button class="btn btn-outline-secondary">Ver detalhes</button></a></td>
                    </tr>`
                })
            })
            .catch(function (err) {
            })

    }
