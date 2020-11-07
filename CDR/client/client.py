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

        # Creamos la clase para loguearse y la ventana grafica de login y el manager
        self.Login = Login(self)
        self.MainWindow = MainWindow(self)

        # Mostramos la ventana
        self.MainWindow.show_all()
        # Iniciamos la interfaz Gtk
        Gtk.main()
    
    def login(self):
        self.Login.loginWithRfid()

    def validLogin(self):
        text = "Welcome " + self.name
        print(text)
        GLib.idle_add(self.MainWindow.displayValidLogin, text)

    def invalidLogin(self):
        text = "Invalid login"
        print(text)
        GLib.idle_add(self.MainWindow.displayInvalidLogin, text)

    def startManager(self):
        GLib.idle_add(self.MainWindow.managerWindow)


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
# MAIN WINDOW
#=================
class MainWindow(Gtk.Window):

    def __init__(self, App):
        self.App = App

        # Definimos que esta clase es la ventana
        Gtk.Window.__init__(self)

        # Le indicamos al programa que al pulsar la X queremos que GTK finalice
        self.connect("destroy", Gtk.main_quit)

        # Aplicamos los estilos CSS
        self.applyStyles(styles)

        self.loginWindow()

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

    #=================
    # LOGIN WINDOW FUNCTIONS
    #=================

    def loginWindow(self):

        # Definimos el titulo y el tamaño de la ventana
        self.set_title("Login")
        self.set_default_size(600, 200)

        # Creamos una caja que estara dentro de la ventana y en la que meteremos los componentes
        self.LoginBox = Gtk.VBox(spacing=0)
        self.add(self.LoginBox)

        # Creamos un label donde podremos ver el uid
        self.LoginMainLabel = Gtk.Label(label="Please, login with your university card")
        self.LoginMainLabel.width_chars = 100

        # Creamos el boton de clear y el boton de login les damos diferentes parametros
        self.createClearButton()
        self.createLoginButton()

        # Colocamos los elementos dentro de la caja
        self.LoginBox.add(self.LoginMainLabel)

        # Iniciamos el hilo encargado de loguear
        self.App.login()

    # Funcion encargada de crear el boton Clear
    def createClearButton(self):
        self.ClearButton = Gtk.Button(label="Clear")
        self.ClearButton.set_margin_start(20)
        self.ClearButton.set_margin_top(20)
        self.ClearButton.set_margin_end(20)
        self.ClearButton.set_margin_bottom(20)
        self.ClearButton.set_name("clear_button") # Le añadimos la id clear_button para definir sus estilos en el CSS
        self.ClearButton.connect("clicked", self.clearButton) # Al hacer click sobre el boton ejecutamos la función clearButton

    # Creamos la función que se ejecuta al pulsar el boton Clear
    def clearButton(self, ClearButton):
        self.LoginMainLabel.set_text("Please, login with your university card")
        self.LoginBox.remove(ClearButton)
        self.App.login()
    
    # Funcion encargada de crear el boton Login
    def createLoginButton(self):
        self.LoginButton = Gtk.Button(label="Login")
        self.LoginButton.set_margin_start(20)
        self.LoginButton.set_margin_top(20)
        self.LoginButton.set_margin_end(20)
        self.LoginButton.set_margin_bottom(20)
        self.LoginButton.set_name("login_button") # Le añadimos la id login_button para definir sus estilos en el CSS
        self.LoginButton.connect("clicked", self.loginButton) # Al hacer click sobre el boton ejecutamos la función loginButton

    # Creamos la función que se ejecuta al pulsar el boton Login
    def loginButton(self, LoginButton):
        self.LoginBox.remove(LoginButton)
        self.App.startManager()

    # Funcion encargada de mostrar el login invalido
    def displayInvalidLogin(self, text):
        self.LoginMainLabel.set_text(text)
        self.LoginBox.add(self.ClearButton)
        self.show_all()

    # Función encargada de mostrar el login valido
    def displayValidLogin(self, text):
        self.LoginMainLabel.set_text(text)
        self.LoginBox.add(self.LoginButton)
        self.show_all()

    #=================
    # MANAGER WINDOW FUNCTIONS
    #=================

    def managerWindow(self):
        # Definimos el titulo y el tamaño de la ventana
        self.set_title("Course Manager")
        self.resize(600, 600)
        self.remove(self.LoginBox)


if __name__ == "__main__":
    App = App()