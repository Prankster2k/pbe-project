import threading
import time
import requests

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GObject, Gdk

from rfid import Rfid


class App:

    def __init__(self):
        #self.Window = Window(self)
        self.ServerPath = ServerPath(self)
        self.ReadUID = ReadUID(self)
        self.uid = None

    def login(self):
        self.ReadUID.start()

    def validLogin(self):
        print("Valido")
        #GLib.idle_add(self.validLogin, self.uid)

    def invalidLogin(self):
        print("Invalido")
        #GLib.idle_add(self.invalidLogin, self.uid)

class ServerPath:

    def __init__(self, App):
        self.App = App

    def serverValidateUID(self, uid):
        r = requests.get("http://192.168.0.20/auth?uid=" + uid)
        print(r.text)
        return r.text


class ReadUID:

    def __init__(self, App):
        self.App = App
        #self.rf = Rfid()
        self.uid = None

    def start(self):
        self.uid_thread = threading.Thread(target=self.readUID)
        self.uid_thread.start()

    def readUID(self):
        print("Coloca una tarjeta NFC")
        self.uid = input()#self.rf.read_uid()
        print(self.uid)
        if self.App.ServerPath.serverValidateUID(self.uid) == "True":
            self.App.uid = self.uid
            self.App.validLogin()
        else:
            self.App.invalidLogin()


if __name__ == "__main__":

    App = App()
    App.login()