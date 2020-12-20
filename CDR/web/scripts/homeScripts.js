var name;
var uid;
var webUrl = "https://atlasserverapp.000webhostapp.com";

var loginForm = document.getElementById("login_form");
loginForm.addEventListener("submit", (event) => {
    event.preventDefault();
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    fetch(`${webUrl}/loginuser?username=${username}&password=${password}`)
        .then(res => res.json()) 
        .then(myJson => {
            name = myJson[0].name;
            uid = myJson[0].student_uid;
            console.log(myJson);
            if(name != "" && uid != ""){
                startApp();
            } else {
                console.log("Vacio");
            }
        })
        .catch(err => {
            console.error(err);
            error("Invalid Login");
        })
});


function logout(){
    name = null;
    uid = null;

    //Cambiamos el tamaño de la ventana
    mainDiv = document.getElementById("main_div");
    mainDiv.style.maxWidth = "500px";
    mainDiv.style.maxHeight = "350px";

    //Cambiamos el texto del Welcome
    let welcomeText = document.getElementById("welcome_text");
    welcomeText.innerHTML = `Welcome to Atlas`;
    welcomeText.style.gridColumn= "1 / 3";
    welcomeText.style.textAlign= "center";
    welcomeText.style.fontSize = "36px";
    welcomeText.style.fontWeight = "bold";
    welcomeText.style.marginBottom = "30px";

    //Borramos el boton de Logout
    let mainHeader = document.getElementById("main_header");
    logoutButton = document.getElementById("logout_button");
    mainHeader.removeChild(logoutButton);
    searchBar = document.getElementById("search_bar");
    mainDiv.removeChild(searchBar);
    dataBox = document.getElementById("data_box");
    mainDiv.removeChild(dataBox);

    //Agregamos el form de login
    mainDiv.appendChild(loginForm);
}


function startApp(){
    console.log(`Name: ${name} UID: ${uid}`)

    //Cambiamos el tamaño de la ventana
    let mainDiv = document.getElementById("main_div");
    mainDiv.style.maxWidth = "1000px";
    mainDiv.style.maxHeight = "1000px";

    //Quitamos el form de login
    let loginForm = document.getElementById("login_form");
    mainDiv.removeChild(loginForm);
    
    //Cambiamos el texto del Welcome
    let welcomeText = document.getElementById("welcome_text");
    welcomeText.innerHTML = `Welcome ${name}`;
    welcomeText.style.gridColumn= "1";
    welcomeText.style.textAlign= "left";
    welcomeText.style.fontSize = "20px";
    welcomeText.style.fontWeight = "300";
    welcomeText.style.marginBottom = "0px";

    //Creamos la search bar, el boton de logout y el div donde se crearan las tablas
    let mainHeader = document.getElementById("main_header");
    mainHeader.innerHTML += `
        <input id="logout_button" class="button" type="button" value="Logout">
    `;
    mainDiv.innerHTML += `
        <input id="search_bar" type="text" autocomplete="off" placeholder="Search...">
        <div id="data_box"></div>
    `;

    // Creamos el evento del boton de logout
    let logoutButton = document.getElementById("logout_button");
    logoutButton.addEventListener("click", logout);

    // Creamos el evento de la search bar
    let searchBar = document.getElementById("search_bar");
    searchBar.addEventListener("keyup", (event) => {
        if(event.keyCode == 13){
            rawQueryToTable(searchBar.value)
        }
    });
}


function rawQueryToTable(query){
    // Si en la query no hay ningun ? lo ponemos para añadir el uid como parametro
    // Si en la query hay un ? añadimos un & delante del uid para concatenar parametros
    var url;
    if(query.includes("?")){
        url = `${webUrl}/${query}&uid=${uid}`;
    } else {
        url = `${webUrl}/${query}?uid=${uid}`;
    }

    console.log(url);

    fetch(url)
    .then(res => res.json()) 
    .then(myJson => {
        console.log(myJson);

        dataBox = document.getElementById("data_box");
        // Creamos la tabla
        let tableHTML;

        tableHTML = `<table id="data_table">`;

        // Añadimos la cabecera de la tabla
        tableHTML += `<thead><tr>`;
        for(let key in myJson[0]){
            tableHTML += `<th>${key}</th>`;
        }
        tableHTML += `</tr></thead>`;

        // Añadimos el cuerpo
        tableHTML += `<tbody>`;
        for(let i = 0; i < myJson.length; i++){
            tableHTML += `<tr>`;
            for(let key in myJson[i]){
                tableHTML += `<td>${myJson[i][key]}</td>`;
            }
            tableHTML += `</tr>`;
        }
        tableHTML += `</tbody>`;
        tableHTML += `</table>`
        console.log(tableHTML);

        // Metemos la tabla en la el div con un =, asi si habia otra tabla anterior se borra
        dataBox.innerHTML = tableHTML;

    })
    .catch(err => {
        console.error(err)
        error("Invalid search")
    })
}


function error(msg){
    document.getElementById("error_box").innerHTML = `Error: ${msg}`;
    document.getElementById("error_box").style.visibility = "visible";
    document.getElementById("error_box").style.opacity = "1";

    setTimeout(function(){
        document.getElementById("error_box").style.opacity = "0";
    }, 3000)
}