import threading
import requests
import time

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GObject, Gdk

from rfid import Rfid

class App:

    def __init__(self):
        self.uid = False
        self.LoginThread = LoginThread(self)
        self.Window = Window(self)

    def start(self):
        self.LoginThread.start()

class LoginThread:

    def __init__(self, App):
        self.App = App
        self.rf = Rfid()

    def start(self):
        thread = threading.Thread(target=self.validateUID, daemon=True)
        thread.start()

    def validateUID(self):
        self.validated = False

        print("Login...")
        while not self.validated:
            GLib.idle_add(self.App.Window.loginLabel)
            self.uid = self.rf.read_uid() #Leemos el UID
            self.App.uid = self.uid
            res = requests.get("http://192.168.0.20/auth?uid=" + self.uid) # Validamos el UID
            if res.text == "True":
                print("UID Valid")
                self.validated = True
                GLib.idle_add(self.App.Window.validLogin, self.uid)
            else:
                print("UID Invalid")
                GLib.idle_add(self.App.Window.invalidLogin, self.uid)
                time.sleep(3)
            
# Creamos la clase de la ventana de login
class Window(Gtk.Window):
    
    def __init__(self, App):
        self.App = App
        # Definimos la ventana, su titulo y su tamaño
        Gtk.Window.__init__(self, title="Course Manager")
        Gtk.Window.set_default_size(self, 600, 200)

        # Creamos una caja que estara dentro de la ventana y en laque meteremos los componentes
        self.box = Gtk.VBox(spacing=0)
        self.add(self.box)

        # Creamos un label donde podremos ver el uid
        self.MainLabel = Gtk.Label(label="Please, login with your university card")
        self.MainLabel.width_chars = 100

        # Creamos el boton de clear y le damos diferentes parametros
        self.MainButton = Gtk.Button(label="Login")
        self.MainButton.set_margin_start(20)
        self.MainButton.set_margin_top(20)
        self.MainButton.set_margin_end(20)
        self.MainButton.set_margin_bottom(20)
        self.MainButton.set_size_request(100, 80)

        # Colocamos los elementos dentro de la caja
        self.box.add(self.MainLabel)

        # Aplicamos los estilos de styles.css
        self.applyStyles('styles.css')

    def loginLabel(self):
        self.MainLabel.set_text("Please, login with your university card")

    def loginButton(self, MainButton):
       print("Has entrado")

    def validLogin(self, uid):
        self.MainLabel.set_text("uid: " + uid)
        self.MainButton.connect("clicked", self.loginButton)
        self.MainButton_context = self.MainButton.get_style_context()
        self.MainButton_context.add_class("green_button")
        self.box.pack_start(self.MainButton, False, False, 0)
        self.show_all()
        return False

    def invalidLogin(self, uid):
        self.MainLabel.set_text("Invalid UID = " + str(uid) + ", please use a valid authentificator")
        self.show_all()
        return False
    
    def applyStyles(self, fileName):
        with open(fileName, 'r') as file:
            css = file.read().replace('\n', '')
            css = css.encode()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__":
    App = App()
    App.start()
    App.Window.connect("destroy", Gtk.main_quit)
    App.Window.show_all()
    Gtk.main()

    
