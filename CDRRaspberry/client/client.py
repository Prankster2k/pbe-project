import threading
import time
import requests

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GObject, Gdk

from rfid import Rfid


class App:

    def __init__(self):
        self.Window = Window(self)
        self.ServerPath = ServerPath(self)
        self.ReadUID = ReadUID(self)
        self.uid = False

    def login(self):
        self.ReadUID.readUID()

    def validLogin(self):
        print("Valido")
        GLib.idle_add(self.Window.validLogin, self.uid)

    def invalidLogin(self):
        print("Invalido")
        GLib.idle_add(self.Window.invalidLogin, self.uid)


class ServerPath:

    def __init__(self, App):
        self.App = App

    def serverValidateUID(self, uid):
        r = requests.get("http://192.168.0.20/auth?uid=" + uid)
        return r.text


class ReadUID:

    def __init__(self, App):
        self.App = App
        #self.rf = Rfid()
        self.uid = None

    def start(self):
        if not uid_thread.is_alive():
            uid_thread = threading.Thread(target=self.readUID, daemon=True)
            uid_thread.start()

    def readUID(self):
        print("Reading UID...")
        self.uid = input() #self.rf.read_uid()
        print(self.uid)
        self.App.uid = self.uid
        if self.App.ServerPath.serverValidateUID(self.uid) == "True":
            self.App.validLogin()
        else:
            self.App.invalidLogin()

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

    def loginButton(self, MainButton):
       print("Has entrado")

    def retryButton(self, MainButton):
        print("Retry")
        self.box.remove(MainButton)
        self.show_all()
        self.App.login()

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
        self.MainButton.connect("clicked", self.retryButton)
        self.MainButton_context = self.MainButton.get_style_context()
        self.MainButton_context.add_class("red_button")
        self.MainButton.set_label("Retry")
        self.box.pack_start(self.MainButton, False, False, 0)
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

    MainApp = App()

    uid_thread = threading.Thread(target=App.login, args=(App,), daemon=True)
    uid_thread.start()

    MainApp.Window.connect("destroy", Gtk.main_quit)
    MainApp.Window.show_all()
    Gtk.main()