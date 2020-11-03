import requests
import json

hostname = "http://192.168.0.20:8000"

#   Le envia la query al servidor (una vez el usuario esta logeado)
#       hostname: dirección del servidor
#       uid: uid del usuario
#       query: query que queremos enviar al servidor       
#
#   Retorna la respuesta del servidor
def rawQuery(hostname, uid, query):
    payload = {
        "uid": uid
    }
    r = requests.get(hostname + query, params=payload)
    return r


#   Le envia el uid al servidor para loguearse
#       hostname: dirección del servidor
#       uid: uid del usuario
#
#   Retorna el nombre del estudiante si el uid es valido y "false" si no lo es
def login(hostname, uid):
    payload = {
        "uid": uid
    }
    r = requests.get(hostname + "/login", params=payload)
    if r.text != "false":
        return r.text
    else:
        return False    


#   Le envia los parametros al servidor para obtener las tasks (tareas)
#       hostname: dirección del servidor
#       uid: uid del usuario
#       date: fecha de entrega (YYYY-MM-DD)
#       subject: asignatura
#       name: nombre del trabajo
#
#   Retorna un string de JSON con las tareas ordenadas por fecha de entrega.
def getTasks(hostname, uid, date, subject, name):
    payload = {
        "uid": uid,
        "date": date,
        "subject": subject,
        "name": name
    }
    r = requests.get(hostname + "/tasks", params=payload)
    return r


#   Le envia los parametros al servidor para obtener las timetables
#       hostname: dirección del servidor
#       uid: uid del usuario
#       day: dia de la clase (Sun=0, Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6)
#       hour: hora de la clase (hh:mm)
#       subject: asignatura
#       room: aula
#
#   Retorna ...
def getTimetables(hostname, uid, day, hour, subject, room):
    payload = {
        "uid": uid,
        "day": day,
        "hour": hour,
        "subject": subject,
        "room": room
    }
    r = requests.get(hostname + "/timetables", params=payload)
    return r


#   Le envia los parametros al servidor para obtener las timetables
#       hostname: dirección del servidor
#       uid: uid del usuario
#       subject: asignatura
#       name: nombre del examen o trabajo
#       mark: nota
#
#   Retorna string de JSON ordenados alfabeticamente segun el subject
def getMarks(hostname, uid, subject, name, mark):
    payload = {
        "uid": uid,
        "subject": subject,
        "name": name,
        "mark": mark
    }
    r = requests.get(hostname + "/marks", params=payload)
    return r



if __name__ == "__main__":
    uid = "6918F9B3"

    r = login(hostname, "6918F9B3")
    print(r)

    #r = getMarks(hostname, uid, "RP", "Practica 1", "9")
    #r = rawQuery(hostname, uid, "/marks?subject=PSAVC")
    r = rawQuery(hostname, uid, )
    result = r.json()
    print(result)

