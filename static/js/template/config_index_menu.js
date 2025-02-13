// Configuração JS index menu
const searchField = document.querySelector("#searchField");
const btnSearch = document.querySelector("#btnSearch");
const initialDate = document.querySelector("#initialDate");
const finalDate = document.querySelector("#finalDate");
const appTable = document.querySelector(".app-table")
const tableOutput = document.querySelector(".table-output")
const tbody = document.querySelector(".table-body")


function get_date(date){
    var date = new Date(date);
    var day = date.getDate();
    var month = date.getMonth();
    var year = date.getFullYear();
    return day + "-" + month + "-" + year;
}

tableOutput.style.display = "none";

searchField.addEventListener("keyup",(e)=>{
	const searchValue = e.target.value;
	if(searchValue.trim().length > 3){
		fetch("/ajax_search_service", {
		body: JSON.stringify({ searchText: searchValue}),
		method:"POST",
		})
		.then((res) => res.json())
		.then((data) => {
            tbody.innerHTML=""
            tableOutput.style.display = "none";
			appTable.style.display = "none";
			tableOutput.style.display = "block";
			if (data.length === []){
				tableOutput.innerHTML = "Nenhum resultado localizado.";
			} else{
				data.forEach(item=>{
                if (item.date_current_status){
                var date = item.date_current_status
                 var format_date = date.substr(0, 10);
                }
				tbody.innerHTML+=`
    <tr>
        <td>${ item.type } - ${ item.number }</td>
        <td>${ item.current_status }</td>
        <td>${ format_date }</td>
	    <td><a href="/adm/detalhar/${ item.uuid }">Ver detalhes</a></td>
    </tr>`

 });
			}
		});
	}else{
		appTable.style.display = "block";
		tableOutput.style.display = "none";
	}
})
btnSearch.onclick  = function() {
    if(searchField.value){
	const searchValue = searchField.value
	if(searchValue.trim().length > 0){
        tbody.innerHTML=""
		fetch("/ajax_search_service", {
		body: JSON.stringify({
            searchText: searchValue,
            initialDate: initialDate.value,
            finalDate: finalDate.value
        }),
		method:"POST",
		})
		.then((res) => res.json())
		.then((data) => {
            tableOutput.style.display = "none";
			appTable.style.display = "none";
			tableOutput.style.display = "block";
			if (data.length === []){
				tableOutput.innerHTML = "Nenhum resultado localizado.";
			} else{
				data.forEach(item=>{
                    if (item.date_current_status){
                var date = item.date_current_status
                 var format_date = date.substr(0, 10);
                }
				tbody.innerHTML+=`
    <tr>
        <td>${ item.type } - ${ item.number }</td>
        <td>${ item.current_status }</td>
        <td>${ format_date }</td>
	    <td><a href="/adm/detalhar/${ item.uuid }">Ver detalhes</a></td>
    </tr>`
    });
			}
		});
	}else{
		appTable.style.display = "block";
		tableOutput.style.display = "none";
	}
}else{
	if(initialDate.value){
        tbody.innerHTML=""
        initialDateValue = String(get_date(initialDate.value))
        finalDateValue = String(get_date(finalDate.value))
		fetch("/ajax_search_service", {
		body: JSON.stringify({
            "initialDate": initialDate.value,
            "finalDate": finalDate.value
        }),
		method:"POST",
		})
		.then((res) => res.json())
		.then((data) => {
            tableOutput.style.display = "none";
			appTable.style.display = "none";
			tableOutput.style.display = "block";
			if (data.length === []){
				tableOutput.innerHTML = "Nenhum resultado localizado.";
			} else{
				data.forEach(item=>{
                    if (item.date_current_status){
                var date = item.date_current_status
                 var format_date = date.substr(0, 10);
                }
				tbody.innerHTML+=`
    <tr>
        <td>${ item.type } - ${ item.number }</td>
        <td>${ item.current_status }</td>
        <td>${ format_date }</td>
        <td><a href="/adm/detalhar/${ item.uuid }">Ver detalhes</a></td>
    </tr>`
    });
			}
		});
	}else{
		appTable.style.display = "block";
		tableOutput.style.display = "none";
	}
}
};
