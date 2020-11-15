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
        self.remove(self.LoginBox)
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

        # Creamos una caja que estara dentro de la ventana y en la que meteremos los componentes
        self.AppBox = Gtk.Grid()
        self.add(self.AppBox)

        self.createNameLabel()
        self.createMainEntry()
        self.createEntryButton()

        # Colocamos los elementos dentro de la caja y los mostramos
        self.AppBox.attach(self.NameLabel, 0, 0, 2, 1)
        self.AppBox.attach(self.MainEntry, 0, 1, 1, 1)
        self.AppBox.attach(self.EntryButton, 1, 1, 1, 1)
        self.mainTableExists = False
        self.show_all()

    def createNameLabel(self):
        text = "Welcome " + self.App.name
        self.NameLabel = Gtk.Label(label=text)
        self.NameLabel.set_margin_top(10)
        self.NameLabel.set_margin_bottom(10)

    # Creamos el entry donde hacer las busquedas
    def createMainEntry(self):
        self.MainEntry = Gtk.Entry()
        self.MainEntry.set_text("/marks?")
        self.MainEntry.set_margin_start(20)
        self.MainEntry.set_margin_top(10)
        self.MainEntry.set_margin_end(10)
        self.MainEntry.set_margin_bottom(20)
        self.MainEntry.set_property("width-request", 440)
        self.MainEntry.set_name("main_entry") # Le añadimos la id login_button para definir sus estilos en el CSS

    # Creamos el boton de busqueda
    def createEntryButton(self):
        self.EntryButton = Gtk.Button(label="Search")
        self.EntryButton.set_margin_start(10)
        self.EntryButton.set_margin_top(12)
        self.EntryButton.set_margin_end(20)
        self.EntryButton.set_margin_bottom(20)
        self.EntryButton.set_property("width-request", 100)
        self.EntryButton.set_name("entry_button") # Le añadimos la id login_button para definir sus estilos en el CSS
        self.EntryButton.connect("clicked", self.entryButton) # Al hacer click sobre el boton ejecutamos la función loginButton

    # Hacemos la petición al servidor y creamos la tabla con los datos recividos
    def entryButton(self, EntryButton):
        if(self.mainTableExists):
            self.AppBox.remove(self.MainTable)
        text = self.MainEntry.get_text()
        data_json = rawQuery(hostname, self.App.uid, text)
        data = data_json.json()
        self.createMainTable(data)

    # Crea la tabla de datos con el numero de filas y columnas especifico
    def createMainTable(self, data):
        # Primero obtenemos el numero de filas y columnas de la tabla
        columns = self.getTableColumns(data)
        rows = self.getTableRows(data)

        # Creamos la tabla
        self.MainTable = Gtk.Table(n_rows=rows, n_columns=columns, homogeneous=False)
        self.mainTableExists = True
        # Obtenemos la matriz de la data colocada
        table = self.getDataMatrix(data, rows, columns)
        
        for i in range(rows): 
            for j in range(columns): 
                print(table[i][j], end = " ") 
            print()

        # Hacemos que sea una matriz de labels en vez de strings
        for i in range(rows): 
            for j in range(columns): 
                table[i][j] = Gtk.Label(label=table[i][j])
                if(i==0):
                    style_context = table[i][j].get_style_context()
                    style_context.add_class("title")
                    table[i][j].set_text(table[i][j].get_text().upper())
                if(i%2==0 and i!=0):
                    style_context = table[i][j].get_style_context()
                    style_context.add_class("second_column")
                self.MainTable.attach(table[i][j], j, j+1, i, i+1)

        self.MainTable.set_margin_start(10)
        self.MainTable.set_margin_top(22)
        self.MainTable.set_margin_end(20)
        self.MainTable.set_margin_bottom(20)
        self.MainTable.set_property("width-request", 460)
        self.MainTable.set_row_spacings(10)
        self.AppBox.attach(self.MainTable, 0, 2, 2, 1)
        self.MainTable.set_name("main_table")
        self.show_all()

    # Devuelve el numero de columnas que tendra la tabla de datos
    def getTableColumns(self, json):
        i = 0
        for key in json[0].keys():
            i = i + 1
        return i
        
    # Devuelve el numero de filas que tendra la tabla de datos
    def getTableRows(self, json):
        return len(json) + 1

    def getDataMatrix(self, data, rows, columns):
        # Obtenemos las keys que son los valores de la primera fila 
        i = 0
        table = [[0 for x in range(columns)] for y in range(rows)]
        for key in data[0]:
            table[0][i] = key
            i = i + 1

        # Obtenemos los valores de las demás filas
        j = 1
        for d in data:
            i = 0
            for key in d.keys():
                table[j][i] = d[key]
                i = i + 1
            j = j + 1

        # Devolvemos la tabla
        return table

if __name__ == "__main__":
    App = App()