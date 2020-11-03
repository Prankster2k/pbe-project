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

        # Creamos la clase para loguearse y la ventana grafica de login
        self.Login = Login(self)
        self.LoginWindow = LoginWindow(self)

        # Iniciamos el hilo encargado de loguear
        self.Login.loginWithRfid()

        # Le indicamos al programa que al pulsar la X queremos que la ventana se cierre
        self.LoginWindow.connect("destroy", Gtk.main_quit)
        # Mostramos la ventana
        self.LoginWindow.show_all()
        # Iniciamos la interfaz Gtk
        Gtk.main()
    
    def login(self):
        self.Login.loginWithRfid()

    def validLogin(self):
        text = "Welcome " + self.name
        print(text)
        GLib.idle_add(self.LoginWindow.setMainLabelText, text)

    def invalidLogin(self):
        text = "Invalid login"
        print(text)
        GLib.idle_add(self.LoginWindow.setMainLabelText, text)
        GLib.idle_add(self.LoginWindow.box.add, self.LoginWindow.ClearButton)
        GLib.idle_add(self.LoginWindow.show_all)


#=================
# CLASE SE ENCARGADA DE HACER EL LOGIN
#=================
class Login():

    def __init__(self, App):
        self.App = App

        self.uid = False
        # Creamos el objeto Rfid
        self.rf = Rfid()

    def loginWithRfid(self):
        # Creamos un thread que ejecuta la funcion uidReader, lo hacemos un demonio para que al cerrar el hilo principal este hilo tambien se cierre
        self.uid_thread = threading.Thread(target=self.loginThread, daemon=True)
        # Iniciamos el thread
        self.uid_thread.start()

    def loginThread(self):
        print("Introduce tu tarjeta")
        self.App.uid = self.rf.read_uid()
        print(self.App.uid)
        self.App.name = login(hostname, self.App.uid)
        if self.App.name:
            self.App.validLogin()
        else:
            self.App.invalidLogin()


#=================
# LOGIN WINDOW
#=================
class LoginWindow(Gtk.Window):

    def __init__(self, App):
        self.App = App

        # Definimos la ventana, su titulo y su tamaño
        Gtk.Window.__init__(self, title="Login")
        Gtk.Window.set_default_size(self, 600, 200)

        # Creamos una caja que estara dentro de la ventana y en la que meteremos los componentes
        self.box = Gtk.VBox(spacing=0)
        self.add(self.box)

        # Creamos un label donde podremos ver el uid
        self.MainLabel = Gtk.Label(label="Please, login with your university card")
        self.MainLabel.width_chars = 100

        # Creamos el boton de clear y le damos diferentes parametros
        self.createClearButton()

        # Colocamos los elementos dentro de la caja
        self.box.add(self.MainLabel)
        
        # Aplicamos los estilos CSS
        self.applyStyles(styles)

    # Función encargada de aplicar los estilos CSS del archivo fileName
    def applyStyles(self, fileName):
        with open(fileName, 'r') as file:
            css = file.read().replace('\n', '')
            css = css.encode()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    # Creamos una funcion que ira dentro del GLib.idle_add() ya que necesitamos devolver False para que idle_add() no ejecute en bucle la funcion
    def setMainLabelText(self, text):
        self.MainLabel.set_text(text)
        return False

    # Funcion encargada de crear el boton Clear
    def createClearButton(self):
        self.ClearButton = Gtk.Button(label="Clear")
        self.ClearButton.set_margin_start(20)
        self.ClearButton.set_margin_top(20)
        self.ClearButton.set_margin_end(20)
        self.ClearButton.set_margin_bottom(20)
        self.ClearButton.connect("clicked", self.clearButton) #Al hacer click sobre el boton ejecutamos la función clearButton

    # Creamos la función que se ejecuta al pulsar el boton
    def clearButton(self, ClearButton):
        self.MainLabel.set_text("Please, login with your university card")
        self.box.remove(ClearButton)
        self.App.login()

if __name__ == "__main__":
    App = App()