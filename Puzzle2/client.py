#=================
# Jesus Vico
# Clases principales: uidReader (Encargada de leer el uid) y LoginWindow (Encargada de renderizar la interfaz de login)
#=================

import threading

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GObject, Gdk

from rfid import Rfid

styles = "styles.css" # Nombre del archivo con los estilos en CSS

# Clase encargada de leer el uid
class UIDReader():
    
    def __init__(self, Window):
        self.Window = Window

        self.uid = False
        # Creamos el objeto Rfid
        self.rf = Rfid()
        # Creamos un thread que ejecuta la funcion uidReader, lo hacemos un demonio para que al cerrar el hilo principal este hilo tambien se cierre
        self.uid_thread = threading.Thread(target=self.uidThread, daemon=True)
        # Iniciamos el thread
        self.uid_thread.start()

    # Funcion encargada de crear el hilo
    def rerunThread(self):
        # Si el hilo que se encarga de leer el uid no existe, lo volvemos a crear
        if self.uid_thread.is_alive() is False:
            # Creamos un thread que ejecuta la funcion uidReader, lo hacemos un demonio para que al cerrar el hilo principal este hilo tambien se cierre
            self.uid_thread = threading.Thread(target=self.uidThread, daemon=True)
            # Iniciamos el thread
            self.uid_thread.start()
        
    # Creamos una funcion que sera un hilo y se encargara de leer el UID
    def uidThread(self):
        self.uid = self.rf.read_uid()
        print(self.uid)
        # Para modificar el valor del label, añadir el boton y mostrar el contenido debemos utilizar la funcion GLib.idle_add() 
        #   que nos permite modificar la interfaz grafica desde un thread auxiliar sin causar problemas
        GLib.idle_add(self.Window.setMainLabelText, self.uid)
        GLib.idle_add(self.Window.box.add, self.Window.ClearButton)
        GLib.idle_add(self.Window.show_all)

# Creamos la clase de la ventana de login
class LoginWindow(Gtk.Window):
    
    def __init__(self):
        # Creamos el objeto encargado de leer el uid
        self.uidReader = UIDReader(self)

        # Definimos la ventana, su titulo y su tamaño
        Gtk.Window.__init__(self, title="Login")
        Gtk.Window.set_default_size(self, 600, 200)

        # Creamos una caja que estara dentro de la ventana y en laque meteremos los componentes
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
        self.uidReader.rerunThread()

    # Creamos una funcion que sera un hilo y se encargara de leer el UID
    def uidReader(self):
        self.uid = self.rf.read_uid()
        print(self.uid)
        # Para modificar el valor del label, añadir el boton y mostrar el contenido debemos utilizar la funcion GLib.idle_add() 
        #   que nos permite modificar la interfaz grafica desde un thread auxiliar sin causar problemas
        GLib.idle_add(self.setMainLabelText, self.uid)
        GLib.idle_add(self.box.add, self.ClearButton)
        GLib.idle_add(self.show_all)

    # Creamos una funcion que ira dentro del GLib.idle_add() ya que necesitamos devolver False para que idle_add() no ejecute en bucle la funcion
    def setMainLabelText(self, uid):
        self.MainLabel.set_text("uid: " + self.uidReader.uid)
        return False

if __name__ == "__main__":

    #=================
    # CONFIGURACÓN DE LA VENTANA
    #=================

    # Creamos la ventana
    LogWin = LoginWindow()
    # Le indicamos al programa que al pulsar la X queremos que la ventana se cierre
    LogWin.connect("destroy", Gtk.main_quit)
    # Mostramos la ventana
    LogWin.show_all()
    # Iniciamos la interfaz Gtk
    Gtk.main()
