import threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GObject, Gdk
from rfid import Rfid
from connections import *

styles = "styles.css" # Nombre del archivo con los estilos en CSS
hostname = "http://192.168.0.20:8000"


#=================
# CLASE PRINCIPAL ENCARGADA DE GESTIONAR LA APLICACION
#=================
class App():

    def __init__(self):
        self.uid = False
        self.name = False

        self.Login = Login()


#=================
# CLASE SE ENCARGADA DE HACER EL LOGIN
#=================
class Login():

    def __init__(self, App):
        self.App = App

        self.uid = False
        # Creamos el objeto Rfid
        self.rf = Rfid()

    def loginWithRfid():
        # Creamos un thread que ejecuta la funcion uidReader, lo hacemos un demonio para que al cerrar el hilo principal este hilo tambien se cierre
        self.uid_thread = threading.Thread(target=self.loginThread, daemon=True)
        # Iniciamos el thread
        self.uid_thread.start()

    def loginThread():
        self.App.uid = self.rf.read_uid()
        print(self.App.uid)
        self.App.name = login(hostname, self.uid)
        print(self.App.name)



if __name__ == "__main__":

    uid = "6918F9B3"
    hostname = "http://192.168.0.20:8000"

    r = login(hostname, "6918F9B3")
    print(r)