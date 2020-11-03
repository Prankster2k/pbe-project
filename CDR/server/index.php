<?php

switch(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH)){
    case "/login":
        login();
        break;
    case "/tasks": 
        returnTasks();
        break;
    case "/timetables":
        returnTimetables();
        break;
    case "/marks":
        returnMarks();
        break;
    default:
        echo "ERROR404";    
}

# Hace echo del nombre del uid asociado o false si no hay ninguno
function login(){
    # Si se ha enviado un uid
    if(isset($_GET["uid"])) {
        $uid = valueOfArg("uid");

        # Nos conectamos a la base de datos course-manager
        $conn = new mysqli("127.0.0.1", "root", "password123", "course-manager");
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } 
        # Hacemos la peticion de un nombre asociado al uid
        $sql = "SELECT name FROM users WHERE student_uid = '{$uid}'";
        $result = $conn->query($sql);
        $row = $result->fetch_assoc();

        # Si tenemos una respuesta quiere decir que el login es valido
        if($row > 0){
            echo $row['name'];
        } else {
            echo "false";
        }
    }
}

function returnTasks(){
    # Definimos los argumentos (de momento no estamos usando dates)
    $date = valueOfArg("dates");
    $subject = valueOfArg("subject");
    $name = valueOfArg("name");

    # Hacemos la consexión con la base de datos mySQL
    $conn = new mysqli("127.0.0.1", "root", "password123", "course-manager");
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    # Creamos una string con la consulta que vamos a hacer la base de datos
    $sql = "SELECT *
            FROM tasks
            WHERE (DATE(date) >= NOW())
            AND (subject LIKE '{$subject}%')
            AND (name LIKE '{$name}%')
            ORDER BY date
    ";

    # Obtenemos la tabla enviando la consulta al servidor
    $result = $conn->query($sql);
    # Pasamos la tabla SQL a JSON para enviarla
    $tableJSON = tableToJSON($result);
    echo $tableJSON;
}

function returnTimetables(){
    # Definimos los argumentos (de momento no estamos usando dates)
    $day = valueOfArg("day");
    $hour = valueOfArg("hour");
    $subject = valueOfArg("subject");
    $room = valueOfArg("room");

    # Hacemos la consexión con la base de datos mySQL
    $conn = new mysqli("127.0.0.1", "root", "password123", "course-manager");
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    # Creamos una string con la consulta que vamos a hacer la base de datos
    # Primero pedimos las clases desde hoy al final de la semana
    $sql = "SELECT *
            FROM timetables
            WHERE (day >= DAYOFWEEK(NOW()))
            ORDER BY day, hour ASC;
    ";

    # Obtenemos la primera tabla enviando la consulta al servidor
    $result = $conn->query($sql);
    # Pasamos la primera tabla SQL a JSON
    $tableJSON1 = tableToJSON($result);

    # Creamos una string con la consulta que vamos a hacer la base de datos
    # Ahora pedimos las clases restantes
    $sql = "SELECT *
            FROM timetables
            WHERE (day < DAYOFWEEK(NOW()))
            ORDER BY day, hour ASC;
    ";
    # Obtenemos la segunda tabla enviando la consulta al servidor
    $result = $conn->query($sql);
    # Pasamos la segunda tabla SQL a JSON
    $tableJSON2 = tableToJSON($result);

    # Fusionamos las dos tablas para conseguir el resultado que buscamos
    $tableJSON = $tableJSON1 . $tableJSON2;
    echo $tableJSON;
}


function returnMarks(){
    # Definimos los argumentos
    $uid = valueOfArg("uid");
    $subject = valueOfArg("subject");
    $name = valueOfArg("name");
    $mark = valueOfArg("mark");

    # Hacemos la consexión con la base de datos mySQL
    $conn = new mysqli("127.0.0.1", "root", "password123", "course-manager");
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    # Creamos una string con la consulta que vamos a hacer la base de datos
    $sql = "SELECT * 
            FROM marks
            WHERE (student_uid = '{$uid}')
            AND (subject LIKE '{$subject}%')
            AND (name LIKE '{$name}%')
            AND (mark LIKE '{$mark}%')
            ORDER BY subject
            ";
    # Obtenemos la tabla enviando la consulta al servidor
    $result = $conn->query($sql);
    # Pasamos la tabla SQL a JSON para enviarla
    $tableJSON = tableToJSON($result);
    echo $tableJSON;
}


#   Función encargada de transformar una tabla SQL en un objeto JSON
#       $table: tabla SQL que queremos pasar a JSON
#
#   Retorna la tabla en tipo JSON
function tableToJSON($table){
    $array = array();
    # Metemos la tabla SQL en una array
    while($row = mysqli_fetch_assoc($table))
    {
        $array[] = $row;
    }
    # Pasamos de array a JSON y lo devolvemos
    return json_encode($array);
}


#   Función encargada de obtener el valor de un argumento de una petición GET
#       $argument: argumento del que queremos obtener el valor
#
#   Returna el valor del argumento si existe y si no retorna "" (String vacio)
function valueOfArg($argument){
    if(isset($_GET["{$argument}"])){
        return $_GET["{$argument}"];
    } else {
        return "";
    }
}
?>