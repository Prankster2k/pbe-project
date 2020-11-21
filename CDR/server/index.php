<?php
# Definimos los parametros de la base de datos
$db_hostname = "127.0.0.1";
$db_username = "root";
$db_password = "password123";
$db_name = "course-manager";

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
        global $$db_hostname, $db_username, $db_password, $db_name;
        
        $conn = new mysqli($db_hostname, $db_username, $db_password, $db_name);
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        # Hacemos la peticion de un nombre asociado al uid
        $sql = "SELECT name 
                FROM users 
                WHERE student_uid = '{$uid}'
                ";

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


# Hace echo de los tasks en formato JSON
function returnTasks(){
    # Definimos los argumentos
    $date = valueOfArg("date");
    $subject = valueOfArg("subject");
    $name = valueOfArg("name");

    # Si hay una fecha especifica
    if($date != ""){
        # Creamos una string con la consulta que vamos a hacer la base de datos
        $sql = "SELECT *
                FROM tasks
                WHERE (DATE(date) LIKE '%{$date}%')
                AND (subject LIKE '{$subject}%')
                AND (name LIKE '{$name}%')
                ORDER BY date
                ";
    } else {
        # Creamos una string con la consulta que vamos a hacer la base de datos
        $sql = "SELECT *
                FROM tasks
                WHERE (DATE(date) >= NOW())
                AND (subject LIKE '{$subject}%')
                AND (name LIKE '{$name}%')
                ORDER BY date
                ";
    }

    # Obtenemos la tabla como array haciendo una consulta a la base de datos
    $tableArray = obtainTableArray($sql);

    # Codificamos la array como JSON y la enviamos
    echo json_encode($tableArray);
}


# Hace echo de los timetables en formato JSON
function returnTimetables(){
    # Definimos los argumentos
    $day = valueOfArg("day");
    $hour = valueOfArg("hour");
    $subject = valueOfArg("subject");
    $room = valueOfArg("room");

    # Si tenemos un dia especifico enviamos unicamente los horarios de ese dia
    if($day != ""){
        # Creamos una string con la consulta que vamos a hacer la base de datos
        $sql = "SELECT
                    CASE day
                        WHEN 0 THEN 'Sunday'
                        WHEN 1 THEN 'Monday'
                        WHEN 2 THEN 'Tuesday'
                        WHEN 3 THEN 'Wednesday'
                        WHEN 4 THEN 'Thursday'
                        WHEN 5 THEN 'Friday'
                        WHEN 6 THEN 'Saturday'
                        ELSE ''
                    END AS Day_Name,
                    hour, subject, room
                FROM timetables
                WHERE (day = '{$day}')
                AND (subject LIKE '{$subject}%')
                AND (hour LIKE '%{$hour}%')
                AND (room LIKE '{$room}%')
                ORDER BY day, hour ASC;
                ";


        # Obtenemos la tabla como array haciendo una consulta a la base de datos
        $tableArray = obtainTableArray($sql);

    } else { # Si no especificamos el dia devolvemos el horario de toda la semana
        # Creamos una string con la consulta que vamos a hacer la base de datos
        # Primero pedimos las clases desde hoy al final de la semana
        $sql = "SELECT
                    CASE day
                        WHEN 0 THEN 'Sunday'
                        WHEN 1 THEN 'Monday'
                        WHEN 2 THEN 'Tuesday'
                        WHEN 3 THEN 'Wednesday'
                        WHEN 4 THEN 'Thursday'
                        WHEN 5 THEN 'Friday'
                        WHEN 6 THEN 'Saturday'
                        ELSE ''
                    END AS Day_Name,
                    hour, subject, room
                FROM timetables
                WHERE (day >= DAYOFWEEK(NOW()))
                AND (subject LIKE '{$subject}%')
                AND (hour LIKE '%{$hour}%')
                AND (room LIKE '{$room}%')
                ORDER BY day, hour ASC;
                ";

        # Obtenemos la tabla 1 como array haciendo una consulta a la base de datos
        $tableArray1 = obtainTableArray($sql);

        # Creamos una string con la consulta que vamos a hacer la base de datos
        # Ahora pedimos las clases restantes
        $sql = "SELECT
                CASE day
                    WHEN 0 THEN 'Sunday'
                    WHEN 1 THEN 'Monday'
                    WHEN 2 THEN 'Tuesday'
                    WHEN 3 THEN 'Wednesday'
                    WHEN 4 THEN 'Thursday'
                    WHEN 5 THEN 'Friday'
                    WHEN 6 THEN 'Saturday'
                    ELSE ''
                END AS Day_Name,
                hour, subject, room
                FROM timetables
                WHERE (day < DAYOFWEEK(NOW()))
                AND (subject LIKE '{$subject}%')
                AND (hour LIKE '%{$hour}%')
                AND (room LIKE '{$room}%')
                ORDER BY day, hour ASC;
                ";
        
        # Obtenemos la tabla 2 como array haciendo una consulta a la base de datos
        $tableArray2 = obtainTableArray($sql);

        # Fusionamos las dos tablas para conseguir el resultado que buscamos
        $tableArray = array_merge($tableArray1, $tableArray2);

    }

    # Codificamos la array como JSON y la enviamos
    echo json_encode($tableArray);
}


# Hace echo de las marks en formato JSON
function returnMarks(){
    # Definimos los argumentos
    $uid = valueOfArg("uid");
    $subject = valueOfArg("subject");
    $name = valueOfArg("name");
    $mark = valueOfArg("mark");

    # Creamos una string con la consulta que vamos a hacer la base de datos
    $sql = "SELECT subject, name, mark 
            FROM marks
            WHERE (student_uid = '{$uid}')
            AND (subject LIKE '{$subject}%')
            AND (name LIKE '{$name}%')
            AND (mark LIKE '{$mark}%')
            ORDER BY subject
            ";

    # Obtenemos la tabla como array haciendo una consulta a la base de datos
    $tableArray = obtainTableArray($sql);

    # Codificamos la array como JSON y la enviamos
    echo json_encode($tableArray);
}


#   Función encargada de obtener el valor de un argumento de una petición GET
#       $argument: argumento del que queremos obtener el valor
#
#   Retorna el valor del argumento si existe y si no retorna "" (String vacio)
function valueOfArg($argument){
    if(isset($_GET["{$argument}"])){
        return $_GET["{$argument}"];
    } else {
        return "";
    }
}


#   Funcion encargada de hacer consultas a la base de datos
#       $sql: String con la consulta que vamos a hacer a la base de datos
#
#   Retorna la el resultado de la consulta como array
function obtainTableArray($sql){
    # Hacemos la consexión con la base de datos mySQL
    global $db_hostname, $db_username, $db_password, $db_name;
    $conn = new mysqli($db_hostname, $db_username, $db_password, $db_name);
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    # Obtenemos la tabla enviando la consulta al servidor
    $result = $conn->query($sql);

    $tableArray = array();
    # Metemos la tabla SQL en una array
    while($row = mysqli_fetch_assoc($result))
    {
        $tableArray[] = $row;
    }

    # Devolvemos el resultado
    return $tableArray;
}
?>